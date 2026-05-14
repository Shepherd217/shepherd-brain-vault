import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";
import { relations } from "drizzle-orm";

export const tasks = sqliteTable("tasks", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  description: text("description"),
  status: text("status", { enum: ["backlog", "todo", "doing", "review", "done", "failed"] })
    .notNull()
    .default("backlog"),
  priority: text("priority", { enum: ["low", "medium", "high", "critical"] })
    .notNull()
    .default("medium"),
  owner: text("owner"),
  agentType: text("agent_type", { enum: ["openclaw", "hermes", "human"] }),
  tags: text("tags").notNull().default("[]"),
  projectId: text("project_id").notNull().default("shepherd"),
  dependencies: text("dependencies").notNull().default("[]"),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull().$defaultFn(() => new Date()),
  startedAt: integer("started_at", { mode: "timestamp" }),
  completedAt: integer("completed_at", { mode: "timestamp" }),
  attempts: integer("attempts").notNull().default(0),
  maxRetries: integer("max_retries").notNull().default(3),
  worktreeId: text("worktree_id"),
  result: text("result"),
  error: text("error"),
  requiresReview: integer("requires_review", { mode: "boolean" }).notNull().default(false),
  nextTask: text("next_task"),
});

export const taskRelations = relations(tasks, ({ one, many }) => ({
  // Self-referential for dependencies handled in app logic
}));

export const agents = sqliteTable("agents", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  agentType: text("agent_type", { enum: ["openclaw", "hermes", "human"] }).notNull(),
  gatewayId: text("gateway_id").notNull(),
  gatewayType: text("gateway_type", { enum: ["openclaw", "hermes"] }).notNull(),
  gatewayUrl: text("gateway_url").notNull(),
  status: text("status", { enum: ["idle", "working", "stalled", "error", "offline"] })
    .notNull()
    .default("offline"),
  currentTask: text("current_task"),
  models: text("models").notNull().default("[]"),
  skills: text("skills").notNull().default("[]"),
  surfaces: text("surfaces").notNull().default("[]"),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull().$defaultFn(() => new Date()),
  updatedAt: integer("updated_at", { mode: "timestamp" }).notNull().$defaultFn(() => new Date()),
});

export const worktrees = sqliteTable("worktrees", {
  id: text("id").primaryKey(),
  taskId: text("task_id").notNull().unique(),
  repoPath: text("repo_path").notNull(),
  worktreePath: text("worktree_path").notNull(),
  branch: text("branch").notNull(),
  baseBranch: text("base_branch").notNull().default("main"),
  port: integer("port"),
  envFile: text("env_file"),
  status: text("status", { enum: ["creating", "active", "cleaning", "archived"] })
    .notNull()
    .default("creating"),
  cleanupPolicy: text("cleanup_policy", { enum: ["auto-clean", "keep-if-dirty", "never"] })
    .notNull()
    .default("auto-clean"),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull().$defaultFn(() => new Date()),
  lastActivity: integer("last_activity", { mode: "timestamp" }).notNull().$defaultFn(() => new Date()),
});

export const events = sqliteTable("events", {
  id: text("id").primaryKey(),
  type: text("type").notNull(),
  timestamp: integer("timestamp", { mode: "timestamp" }).notNull().$defaultFn(() => new Date()),
  source: text("source").notNull(),
  payload: text("payload").notNull(),
  taskId: text("task_id"),
  agentId: text("agent_id"),
});
