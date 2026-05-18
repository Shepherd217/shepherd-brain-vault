import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getProfilesFile(config) {
  const path = (config?.profilesFile || "~/.openclaw/config/agent-profiles.json").replace(/^~/, homedir());
  ensureDir(join(path, ".."));
  return path;
}

function loadProfiles(config) {
  const file = getProfilesFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return { profiles: {} };
}

function saveProfiles(config, data) {
  writeFileSync(getProfilesFile(config), JSON.stringify(data, null, 2));
}

// Predefined specialization profiles
const DEFAULT_PROFILES = {
  "coder": {
    name: "Code Specialist",
    description: "Excels at writing, reviewing, and debugging code",
    capabilities: ["javascript", "typescript", "python", "react", "nodejs", "git"],
    preferredTasks: ["coding", "debugging", "refactoring", "code-review"],
    strengths: ["fast-iteration", "syntax-precision", "test-writing"]
  },
  "architect": {
    name: "System Architect",
    description: "Designs systems, schemas, and infrastructure",
    capabilities: ["system-design", "database", "api-design", "infrastructure", "scaling"],
    preferredTasks: ["architecture", "schema-design", "planning", "review"],
    strengths: ["big-picture", "tradeoff-analysis", "documentation"]
  },
  "ops": {
    name: "DevOps Engineer",
    description: "Handles deployment, monitoring, and infrastructure",
    capabilities: ["docker", "kubernetes", "ci-cd", "monitoring", "aws", "terraform"],
    preferredTasks: ["deployment", "infrastructure", "monitoring", "maintenance"],
    strengths: ["reliability", "automation", "troubleshooting"]
  },
  "writer": {
    name: "Content Writer",
    description: "Creates documentation, copy, and content",
    capabilities: ["writing", "editing", "documentation", "markdown", "seo"],
    preferredTasks: ["documentation", "copywriting", "blog-posts", "readme"],
    strengths: ["clarity", "tone-matching", "audience-awareness"]
  }
};

export async function activate(context) {
  const { config, gateway } = context;

  gateway.tools.register("define_profile", {
    description: "Define or update an agent specialization profile.",
    parameters: {
      type: "object",
      properties: {
        profileId: { type: "string" },
        name: { type: "string" },
        description: { type: "string" },
        capabilities: { type: "array", items: { type: "string" } },
        preferredTasks: { type: "array", items: { type: "string" } },
        strengths: { type: "array", items: { type: "string" } }
      },
      required: ["profileId", "name"]
    },
    handler: async ({ profileId, name, description, capabilities = [], preferredTasks = [], strengths = [] }) => {
      const profiles = loadProfiles(config);
      profiles.profiles[profileId] = {
        id: profileId,
        name,
        description: description || "",
        capabilities,
        preferredTasks,
        strengths,
        updatedAt: new Date().toISOString()
      };
      saveProfiles(config, profiles);
      return { defined: true, profileId, name, capabilities: capabilities.length };
    }
  });

  gateway.tools.register("match_agent_to_task", {
    description: "Match the best agent profile to a given task based on capabilities.",
    parameters: {
      type: "object",
      properties: {
        taskType: { type: "string" },
        requiredCapabilities: { type: "array", items: { type: "string" } },
        description: { type: "string" }
      },
      required: ["taskType"]
    },
    handler: async ({ taskType, requiredCapabilities = [], description }) => {
      const profiles = loadProfiles(config);
      
      // Merge with defaults
      const allProfiles = { ...DEFAULT_PROFILES, ...profiles.profiles };
      
      const matches = [];
      for (const [id, profile] of Object.entries(allProfiles)) {
        const capabilityScore = requiredCapabilities.length > 0
          ? requiredCapabilities.filter(c => profile.capabilities.includes(c)).length / requiredCapabilities.length
          : 0.5;
        
        const taskMatch = profile.preferredTasks?.includes(taskType) ? 1 : 0;
        const totalScore = (capabilityScore * 0.7) + (taskMatch * 0.3);
        
        matches.push({
          profileId: id,
          name: profile.name,
          score: Math.round(totalScore * 100) / 100,
          capabilities: profile.capabilities,
          matchedCapabilities: requiredCapabilities.filter(c => profile.capabilities.includes(c))
        });
      }
      
      matches.sort((a, b) => b.score - a.score);
      
      return {
        taskType,
        bestMatch: matches[0] || null,
        allMatches: matches.slice(0, 5),
        requiredCapabilities
      };
    }
  });

  gateway.tools.register("list_profiles", {
    description: "List all available agent specialization profiles.",
    parameters: { type: "object", properties: {} },
    handler: async () => {
      const profiles = loadProfiles(config);
      const allProfiles = { ...DEFAULT_PROFILES, ...profiles.profiles };
      
      return {
        total: Object.keys(allProfiles).length,
        defaultProfiles: Object.keys(DEFAULT_PROFILES).length,
        customProfiles: Object.keys(profiles.profiles).length,
        profiles: Object.entries(allProfiles).map(([id, p]) => ({
          id,
          name: p.name,
          capabilities: p.capabilities.length,
          description: p.description?.slice(0, 100)
        }))
      };
    }
  });

  return {
    name: "agent-specialization",
    version: "1.0.0"
  };
}