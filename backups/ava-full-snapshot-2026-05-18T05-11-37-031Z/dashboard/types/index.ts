export type TaskStatus = "backlog" | "todo" | "doing" | "review" | "done" | "failed";
export type Priority = "low" | "medium" | "high" | "critical";
export type AgentType = "openclaw" | "hermes" | "human";
export type AgentStatus = "idle" | "working" | "stalled" | "error" | "offline";

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: Priority;
  owner: string | null;
  agentType: AgentType | null;
  tags: string[];
  projectId: string;
  dependencies: string[];
  createdAt: Date;
  startedAt: Date | null;
  completedAt: Date | null;
  attempts: number;
  maxRetries: number;
  worktreeId: string | null;
  result: string | null;
  error: string | null;
  requiresReview: boolean;
  nextTask: NextTaskConfig | null;
}

export interface NextTaskConfig {
  title: string;
  description?: string;
  owner: string;
  agentType: AgentType;
  tags?: string[];
}

export interface Agent {
  id: string;
  name: string;
  agentType: AgentType;
  gatewayId: string;
  gatewayType: "openclaw" | "hermes";
  gatewayUrl: string;
  status: AgentStatus;
  currentTask: string | null;
  models: string[];
  skills: string[];
  surfaces: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Worktree {
  id: string;
  taskId: string;
  repoPath: string;
  worktreePath: string;
  branch: string;
  baseBranch: string;
  port: number | null;
  envFile: string | null;
  status: "creating" | "active" | "cleaning" | "archived";
  cleanupPolicy: "auto-clean" | "keep-if-dirty" | "never";
  createdAt: Date;
  lastActivity: Date;
}

export interface DashboardEvent {
  id: string;
  type: DashboardEventType;
  timestamp: Date;
  source: string;
  payload: unknown;
  taskId?: string;
  agentId?: string;
}

export type DashboardEventType =
  | "task_created"
  | "task_claimed"
  | "task_status_changed"
  | "task_completed"
  | "task_failed"
  | "agent_connected"
  | "agent_disconnected"
  | "agent_status_changed"
  | "worktree_created"
  | "worktree_cleaned"
  | "approval_requested"
  | "approval_granted"
  | "approval_denied"
  | "error";

// Adapter types
export interface AdapterConfig {
  id: string;
  name: string;
  url: string;
  authToken?: string;
  options?: Record<string, unknown>;
}

export type AdapterEventType =
  | "connected"
  | "disconnected"
  | "agent_online"
  | "agent_offline"
  | "agent_status_change"
  | "task_start"
  | "task_progress"
  | "task_complete"
  | "task_error"
  | "heartbeat"
  | "error";

export interface AgentAdapter {
  readonly type: string;
  readonly version: string;
  connect(config: AdapterConfig): Promise<void>;
  disconnect(): Promise<void>;
  health(): Promise<{ status: string; latency: number }>;
  listAgents(): Promise<Agent[]>;
  getAgent(id: string): Promise<Agent>;
  spawnTask(agentId: string, task: Task): Promise<Session>;
  getSession(sessionKey: string): Promise<Session>;
  steer(sessionKey: string, message: string): Promise<void>;
  kill(sessionKey: string): Promise<void>;
  on(event: AdapterEventType, callback: (data: unknown) => void): void;
  off(event: AdapterEventType, callback: (data: unknown) => void): void;
}

export interface Session {
  sessionKey: string;
  label: string;
  status: string;
}

export interface TaskSpawnConfig {
  task: string;
  label?: string;
  model?: string;
  runTimeoutSeconds?: number;
  sandbox?: "inherit" | "require";
  lightContext?: boolean;
}

export type OpenClawEventType =
  | "connected"
  | "disconnected"
  | "reconnecting"
  | "task_spawned"
  | "task_progress"
  | "task_completed"
  | "agent_status_change"
  | "heartbeat"
  | "error";

export interface OpenClawEvent {
  type: OpenClawEventType;
  timestamp: Date;
  payload: unknown;
  sessionKey?: string;
}
