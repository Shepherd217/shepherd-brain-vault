import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getMeshFile(config) {
  const path = (config?.meshFile || "~/.openclaw/config/agent-mesh.json").replace(/^~/, homedir());
  ensureDir(join(path, ".."));
  return path;
}

function loadMesh(config) {
  const file = getMeshFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return { agents: {}, messages: [] };
}

function saveMesh(config, data) {
  writeFileSync(getMeshFile(config), JSON.stringify(data, null, 2));
}

export async function activate(context) {
  const { config, gateway } = context;
  const timeoutMs = config?.heartbeatTimeoutMs || 300000;

  gateway.tools.register("register_agent", {
    description: "Register an agent in the mesh with capabilities and specialization.",
    parameters: {
      type: "object",
      properties: {
        agentId: { type: "string" },
        name: { type: "string" },
        capabilities: { type: "array", items: { type: "string" } },
        specialization: { type: "string" },
        channel: { type: "string" },
        model: { type: "string" }
      },
      required: ["agentId", "name"]
    },
    handler: async ({ agentId, name, capabilities = [], specialization, channel, model }) => {
      const mesh = loadMesh(config);
      mesh.agents[agentId] = {
        id: agentId,
        name,
        capabilities,
        specialization: specialization || "general",
        channel: channel || "unknown",
        model: model || "unknown",
        registeredAt: new Date().toISOString(),
        lastHeartbeat: new Date().toISOString(),
        status: "active",
        currentTask: null
      };
      saveMesh(config, mesh);
      return { registered: true, agentId, name, specialization };
    }
  });

  gateway.tools.register("discover_agents", {
    description: "Discover all active agents in the mesh with their capabilities.",
    parameters: {
      type: "object",
      properties: {
        capability: { type: "string", description: "Filter by capability" },
        specialization: { type: "string" }
      }
    },
    handler: async ({ capability, specialization }) => {
      const mesh = loadMesh(config);
      let agents = Object.values(mesh.agents);
      
      // Filter out stale agents
      const now = Date.now();
      agents = agents.filter(a => {
        const lastHeartbeat = new Date(a.lastHeartbeat).getTime();
        return (now - lastHeartbeat) < timeoutMs;
      });
      
      if (capability) {
        agents = agents.filter(a => a.capabilities.includes(capability));
      }
      if (specialization) {
        agents = agents.filter(a => a.specialization === specialization);
      }
      
      return {
        totalAgents: agents.length,
        agents: agents.map(a => ({
          id: a.id,
          name: a.name,
          specialization: a.specialization,
          capabilities: a.capabilities,
          status: a.status,
          currentTask: a.currentTask
        }))
      };
    }
  });

  gateway.tools.register("send_agent_message", {
    description: "Send a message to another agent in the mesh.",
    parameters: {
      type: "object",
      properties: {
        fromAgent: { type: "string" },
        toAgent: { type: "string" },
        message: { type: "string" },
        messageType: { type: "string", enum: ["task", "question", "response", "broadcast"], default: "task" }
      },
      required: ["fromAgent", "toAgent", "message"]
    },
    handler: async ({ fromAgent, toAgent, message, messageType = "task" }) => {
      const mesh = loadMesh(config);
      mesh.messages.push({
        from: fromAgent,
        to: toAgent,
        message,
        type: messageType,
        timestamp: new Date().toISOString(),
        read: false
      });
      // Keep last 100 messages
      if (mesh.messages.length > 100) mesh.messages = mesh.messages.slice(-100);
      saveMesh(config, mesh);
      return { sent: true, from: fromAgent, to: toAgent, type: messageType };
    }
  });

  gateway.tools.register("get_agent_status", {
    description: "Get detailed status of a specific agent or all agents.",
    parameters: {
      type: "object",
      properties: {
        agentId: { type: "string" }
      }
    },
    handler: async ({ agentId }) => {
      const mesh = loadMesh(config);
      if (agentId) {
        const agent = mesh.agents[agentId];
        if (!agent) return { error: `Agent ${agentId} not found` };
        const messages = mesh.messages.filter(m => m.to === agentId && !m.read);
        return { agent, unreadMessages: messages.length, messages };
      }
      return {
        totalAgents: Object.keys(mesh.agents).length,
        activeAgents: Object.values(mesh.agents).filter(a => a.status === "active").length,
        agents: Object.values(mesh.agents).map(a => ({
          id: a.id,
          name: a.name,
          status: a.status,
          specialization: a.specialization,
          currentTask: a.currentTask
        }))
      };
    }
  });

  return {
    name: "agent-mesh",
    version: "1.0.0"
  };
}
