const { promises: fs } = require("fs");
const path = require("path");

const STATUS_DIR = path.join(process.cwd(), ".coordination", "status");
const STATUS_FILE = path.join(STATUS_DIR, "agents.json");

async function ensureDir() {
  await fs.mkdir(STATUS_DIR, { recursive: true });
}

async function reportStatus(agentId, status) {
  await ensureDir();
  let data = {};
  try {
    const existing = await fs.readFile(STATUS_FILE, "utf8");
    data = JSON.parse(existing);
  } catch {}

  data[agentId] = {
    ...status,
    lastUpdated: new Date().toISOString(),
  };

  await fs.writeFile(STATUS_FILE, JSON.stringify(data, null, 2));
}

async function getAllStatuses() {
  try {
    const data = await fs.readFile(STATUS_FILE, "utf8");
    return JSON.parse(data);
  } catch {
    return {};
  }
}

async function getAgentStatus(agentId) {
  const all = await getAllStatuses();
  return all[agentId] || null;
}

module.exports = {
  reportStatus,
  getAllStatuses,
  getAgentStatus,
};
