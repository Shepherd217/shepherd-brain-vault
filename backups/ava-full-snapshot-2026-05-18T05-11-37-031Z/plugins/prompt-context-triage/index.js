import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

// Simple keyword-based relevance scoring
function scoreRelevance(filePath, content, prompt) {
  const promptLower = prompt.toLowerCase();
  const contentLower = content.toLowerCase();
  const fileName = filePath.split("/").pop().toLowerCase();
  
  let score = 0;
  
  // Check filename matches
  if (promptLower.includes(fileName.replace(/\.(js|ts|jsx|tsx|py|json|md)$/, ""))) {
    score += 0.3;
  }
  
  // Check content keyword overlap
  const promptWords = promptLower.split(/\s+/).filter(w => w.length > 3);
  const contentWords = new Set(contentLower.split(/\s+/));
  let matches = 0;
  for (const word of promptWords) {
    if (contentWords.has(word)) matches++;
  }
  score += (matches / promptWords.length) * 0.7;
  
  return Math.min(1, score);
}

function listFiles(dir, maxDepth = 2, currentDepth = 0) {
  if (currentDepth >= maxDepth) return [];
  
  const files = [];
  try {
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const path = join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith(".") && entry.name !== "node_modules") {
        files.push(...listFiles(path, maxDepth, currentDepth + 1));
      } else if (entry.isFile() && entry.name.match(/\.(js|ts|jsx|tsx|py|json|md|yaml|yml)$/)) {
        files.push(path);
      }
    }
  } catch (_) {}
  
  return files;
}

export async function activate(context) {
  const { config, gateway } = context;
  const maxFiles = config?.maxContextFiles || 20;
  const threshold = config?.relevanceThreshold || 0.6;

  gateway.tools.register("analyze_prompt_needs", {
    description: "Analyze what files and context are likely needed based on the user prompt.",
    parameters: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The user's request/prompt" },
        workspaceDir: { type: "string", default: "." }
      },
      required: ["prompt"]
    },
    handler: async ({ prompt, workspaceDir = "." }) => {
      const files = listFiles(workspaceDir, 2);
      const scored = [];
      
      for (const file of files.slice(0, 50)) { // Limit scanning for speed
        try {
          const content = readFileSync(file, "utf-8").slice(0, 5000); // First 5KB only
          const score = scoreRelevance(file, content, prompt);
          if (score >= threshold) {
            scored.push({ file, score: Math.round(score * 100) / 100 });
          }
        } catch (_) {}
      }
      
      scored.sort((a, b) => b.score - a.score);
      
      return {
        prompt,
        filesScanned: files.length,
        relevantFiles: scored.slice(0, maxFiles),
        topFiles: scored.slice(0, 5).map(s => s.file),
        summary: `Found ${scored.length} relevant files out of ${files.length} scanned`
      };
    }
  });

  gateway.tools.register("triage_context", {
    description: "Given a list of context files, triage them by importance for the current prompt.",
    parameters: {
      type: "object",
      properties: {
        prompt: { type: "string" },
        files: { type: "array", items: { type: "string" } }
      },
      required: ["prompt", "files"]
    },
    handler: async ({ prompt, files }) => {
      const triaged = {
        essential: [],
        helpful: [],
        optional: []
      };
      
      for (const file of files) {
        try {
          const content = readFileSync(file, "utf-8").slice(0, 3000);
          const score = scoreRelevance(file, content, prompt);
          
          if (score >= 0.8) triaged.essential.push({ file, score });
          else if (score >= 0.5) triaged.helpful.push({ file, score });
          else triaged.optional.push({ file, score });
        } catch (_) {
          triaged.optional.push({ file, score: 0, error: "Could not read" });
        }
      }
      
      return {
        prompt,
        triaged,
        totalFiles: files.length,
        recommendation: `Include ${triaged.essential.length} essential files, consider ${triaged.helpful.length} helpful ones`
      };
    }
  });

  gateway.tools.register("suggest_context_files", {
    description: "Suggest what context files to include for a given task, with explanations.",
    parameters: {
      type: "object",
      properties: {
        task: { type: "string", description: "Description of the task" },
        workspaceDir: { type: "string", default: "." }
      },
      required: ["task"]
    },
    handler: async ({ task, workspaceDir = "." }) => {
      const files = listFiles(workspaceDir, 2);
      const scored = [];
      
      for (const file of files.slice(0, 50)) {
        try {
          const content = readFileSync(file, "utf-8").slice(0, 3000);
          const score = scoreRelevance(file, content, task);
          scored.push({ file, score: Math.round(score * 100) / 100 });
        } catch (_) {}
      }
      
      scored.sort((a, b) => b.score - a.score);
      const top = scored.slice(0, 10);
      
      return {
        task,
        suggestions: top.map(s => ({
          file: s.file,
          relevance: s.score,
          reason: s.score > 0.7 ? "Directly related to task" : 
                  s.score > 0.4 ? "Potentially relevant" : "Weak match"
        })),
        estimatedTokens: top.length * 800 // Rough estimate
      };
    }
  });

  return {
    name: "prompt-context-triage",
    version: "1.0.0"
  };
}
