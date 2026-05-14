import WebSocket from "ws";
import EventEmitter from "events";
import type { AgentAdapter, AdapterConfig, AdapterEventType, Agent, Session, Task } from "@/types";

export class OpenClawAdapter extends EventEmitter implements AgentAdapter {
  readonly type = "openclaw";
  readonly version = "1.0.0";

  private ws: WebSocket | null = null;
  private config: AdapterConfig | null = null;
  private reconnectAttempts = 0;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private isConnectedFlag = false;

  async connect(config: AdapterConfig): Promise<void> {
    this.config = config;
    return this.doConnect();
  }

  private doConnect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.config) {
        reject(new Error("No config provided"));
        return;
      }

      const url = this.config.url;
      console.log(`[OpenClawAdapter] Connecting to ${url}...`);

      try {
        this.ws = new WebSocket(url, {
          headers: this.config.authToken
            ? { Authorization: `Bearer ${this.config.authToken}` }
            : undefined,
        });

        this.ws.on("open", () => {
          console.log("[OpenClawAdapter] Connected");
          this.isConnectedFlag = true;
          this.reconnectAttempts = 0;
          this.startHeartbeat();
          this.emit("connected", { timestamp: new Date() });
          resolve();
        });

        this.ws.on("message", (data) => {
          try {
            const event = JSON.parse(data.toString());
            this.handleEvent(event);
          } catch (error) {
            console.error("[OpenClawAdapter] Failed to parse message:", error);
          }
        });

        this.ws.on("close", () => {
          this.isConnectedFlag = false;
          this.stopHeartbeat();
          this.emit("disconnected", { timestamp: new Date() });
          this.scheduleReconnect();
        });

        this.ws.on("error", (error) => {
          console.error("[OpenClawAdapter] WebSocket error:", error);
          this.emit("error", { error, timestamp: new Date() });
          if (!this.isConnectedFlag) {
            reject(error);
          }
        });
      } catch (error) {
        reject(error);
      }
    });
  }

  async disconnect(): Promise<void> {
    this.stopHeartbeat();
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnectedFlag = false;
  }

  isConnected(): boolean {
    return this.isConnectedFlag;
  }

  async health(): Promise<{ status: string; latency: number }> {
    const start = Date.now();
    // TODO: Implement actual health check
    return { status: this.isConnected() ? "ok" : "disconnected", latency: Date.now() - start };
  }

  async listAgents(): Promise<Agent[]> {
    // TODO: Query gateway for agent list
    return [];
  }

  async getAgent(id: string): Promise<Agent> {
    // TODO: Query gateway for agent details
    throw new Error("Not implemented");
  }

  async spawnTask(agentId: string, task: Task): Promise<Session> {
    // TODO: Use sessions_spawn equivalent
    console.log(`[OpenClawAdapter] Spawning task for agent ${agentId}:`, task.title);
    return {
      sessionKey: `session_${Date.now()}`,
      label: task.title,
      status: "running",
    };
  }

  async getSession(sessionKey: string): Promise<Session> {
    // TODO: Query session status
    return { sessionKey, label: "", status: "unknown" };
  }

  async steer(sessionKey: string, message: string): Promise<void> {
    // TODO: Send steer message
    console.log(`[OpenClawAdapter] Steering session ${sessionKey}: ${message}`);
  }

  async kill(sessionKey: string): Promise<void> {
    // TODO: Kill session
    console.log(`[OpenClawAdapter] Killing session ${sessionKey}`);
  }

  private handleEvent(event: unknown): void {
    if (typeof event !== "object" || event === null) return;
    const e = event as Record<string, unknown>;

    const eventType = e.type as AdapterEventType;
    if (!eventType) return;

    this.emit(eventType, {
      ...e,
      timestamp: new Date(),
    });
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: "heartbeat", timestamp: Date.now() }));
      }
    }, 30000);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= 10) {
      console.error("[OpenClawAdapter] Max reconnect attempts reached");
      return;
    }

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;

    console.log(`[OpenClawAdapter] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      this.emit("reconnecting", { attempt: this.reconnectAttempts });
      this.doConnect().catch((error) => {
        console.error("[OpenClawAdapter] Reconnect failed:", error);
      });
    }, delay);
  }
}

// Singleton instance
let adapter: OpenClawAdapter | null = null;

export function getOpenClawAdapter(): OpenClawAdapter {
  if (!adapter) {
    adapter = new OpenClawAdapter();
  }
  return adapter;
}
