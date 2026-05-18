import { existsSync, writeFileSync, readFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function getServersFile(config) {
  const path = (config?.serversFile || "~/.openclaw/config/mcp-servers.json").replace(/^~/, homedir());
  ensureDir(join(path, ".."));
  return path;
}

function loadServers(config) {
  const file = getServersFile(config);
  try {
    if (existsSync(file)) {
      return JSON.parse(readFileSync(file, "utf-8"));
    }
  } catch (_) {}
  return { servers: [] };
}

function saveServers(config, data) {
  writeFileSync(getServersFile(config), JSON.stringify(data, null, 2));
}

// Simulated MCP tool discovery (in real implementation, would use MCP protocol)
const MOCK_MCP_TOOLS = {
  "weather": [
    { name: "get_forecast", description: "Get weather forecast for a location", parameters: { location: "string", days: "number" } },
    { name: "get_current", description: "Get current weather", parameters: { location: "string" } }
  ],
  "calculator": [
    { name: "calculate", description: "Perform mathematical calculation", parameters: { expression: "string" } }
  ],
  "search": [
    { name: "web_search", description: "Search the web", parameters: { query: "string", limit: "number" } }
  ]
};

export async function activate(context) {
  const { config, gateway } = context;
  const timeoutMs = config?.timeoutMs || 30000;

  gateway.tools.register("add_mcp_server", {
    description: "Register an MCP server endpoint for tool discovery.",
    parameters: {
      type: "object",
      properties: {
        name: { type: "string", description: "Server name" },
        url: { type: "string", description: "MCP server URL" },
        auth: { type: "object", description: "Authentication config" }
      },
      required: ["name", "url"]
    },
    handler: async ({ name, url, auth }) => {
      const registry = loadServers(config);
      const existing = registry.servers.findIndex(s => s.name === name);
      const server = { name, url, auth: auth || {}, addedAt: new Date().toISOString() };
      
      if (existing >= 0) {
        registry.servers[existing] = server;
      } else {
        registry.servers.push(server);
      }
      
      saveServers(config, registry);
      return { ok: true, name, url, action: existing >= 0 ? "updated" : "added" };
    }
  });

  gateway.tools.register("list_mcp_servers", {
    description: "List all registered MCP servers.",
    parameters: { type: "object", properties: {} },
    handler: async () => {
      const registry = loadServers(config);
      return {
        total: registry.servers.length,
        servers: registry.servers.map(s => ({ name: s.name, url: s.url, addedAt: s.addedAt }))
      };
    }
  });

  gateway.tools.register("discover_mcp_tools", {
    description: "Discover available tools from an MCP server.",
    parameters: {
      type: "object",
      properties: {
        serverName: { type: "string", description: "Server to discover tools from" }
      },
      required: ["serverName"]
    },
    handler: async ({ serverName }) => {
      // In real implementation, would make MCP protocol call to server
      const tools = MOCK_MCP_TOOLS[serverName] || [];
      return {
        server: serverName,
        toolsFound: tools.length,
        tools: tools
      };
    }
  });

  gateway.tools.register("call_mcp_tool", {
    description: "Call a tool on an MCP server.",
    parameters: {
      type: "object",
      properties: {
        serverName: { type: "string" },
        toolName: { type: "string" },
        parameters: { type: "object" }
      },
      required: ["serverName", "toolName", "parameters"]
    },
    handler: async ({ serverName, toolName, parameters }) => {
      // In real implementation, would make MCP protocol call
      // This is a simulation bridge
      return {
        simulated: true,
        server: serverName,
        tool: toolName,
        parameters,
        result: `Simulated execution of ${toolName} on ${serverName}`,
        note: "This is a mock implementation. Real MCP protocol integration requires WebSocket/SSE transport."
      };
    }
  });

  return {
    name: "mcp-tool-bridge",
    version: "1.0.0"
  };
}