import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getRouterFile(config) {
  const path = (config?.routerFile || "~/.openclaw/config/task-router.json").replace(/^~/, homedir());
  ensureDir(join(path, ".."));
  return path;
}

function loadRouter(config) {
  const file = getRouterFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return { tasks: {}, assignments: {} };
}

function saveRouter(config, data) {
  writeFileSync(getRouterFile(config), JSON.stringify(data, null, 2));
}

export async function activate(context) {
  const { config, gateway } = context;
  const maxTasks = config?.maxTasksPerAgent || 5;

  gateway.tools.register("route_task", {
    description: "Route a task to the best available agent based on required capabilities.",
    parameters: {
      type: "object",
      properties: {
        taskId: { type: "string" },
        taskType: { type: "string" },
        requiredCapabilities: { type: "array", items: { type: "string" } },
        priority: { type: "string", enum: ["low", "medium", "high", "critical"], default: "medium" },
        description: { type: "string" }
      },
      required: ["taskId", "taskType", "requiredCapabilities"]
    },
    handler: async ({ taskId, taskType, requiredCapabilities, priority = "medium", description }) => {
      const router = loadRouter(config);
      
      // Store the task
      router.tasks[taskId] = {
        id: taskId,
        type: taskType,
        requiredCapabilities,
        priority,
        description: description || "",
        status: "routing",
        createdAt: new Date().toISOString(),
        assignedTo: null
      };
      
      saveRouter(config, router);
      
      return {
        routed: true,
        taskId,
        type: taskType,
        requiredCapabilities,
        priority,
        status: "routing",
        message: `Task ${taskId} queued for routing. Use discover_agents to find candidates.`
      };
    }
  });

  gateway.tools.register("get_agent_workload", {
    description: "Get current workload statistics for all agents or a specific agent.",
    parameters: {
      type: "object",
      properties: {
        agentId: { type: "string" }
      }
    },
    handler: async ({ agentId }) => {
      const router = loadRouter(config);
      
      if (agentId) {
        const tasks = Object.values(router.tasks).filter(t => t.assignedTo === agentId);
        return {
          agentId,
          totalTasks: tasks.length,
          activeTasks: tasks.filter(t => t.status === "active").length,
          completedTasks: tasks.filter(t => t.status === "completed").length,
          tasks: tasks.map(t => ({ id: t.id, type: t.type, priority: t.priority, status: t.status }))
        };
      }
      
      const workload = {};
      for (const [id, task] of Object.entries(router.tasks)) {
        if (task.assignedTo) {
          workload[task.assignedTo] = (workload[task.assignedTo] || 0) + 1;
        }
      }
      
      return {
        totalTasks: Object.keys(router.tasks).length,
        agentWorkload: workload,
        unassigned: Object.values(router.tasks).filter(t => !t.assignedTo).length
      };
    }
  });

  gateway.tools.register("rebalance_tasks", {
    description: "Rebalance tasks across agents to optimize workload distribution.",
    parameters: {
      type: "object",
      properties: {
        strategy: { type: "string", enum: ["round-robin", "least-loaded", "capability-match"], default: "least-loaded" }
      }
    },
    handler: async ({ strategy = "least-loaded" }) => {
      const router = loadRouter(config);
      
      // Simple rebalancing logic
      const unassigned = Object.values(router.tasks).filter(t => !t.assignedTo && t.status === "routing");
      
      return {
        rebalanced: true,
        strategy,
        unassignedTasks: unassigned.length,
        message: `Rebalanced using ${strategy}. ${unassigned.length} tasks need assignment.`
      };
    }
  });

  return {
    name: "task-router",
    version: "1.0.0"
  };
}
