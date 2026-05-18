#!/usr/bin/env node
/**
 * Emmaus Task Dispatcher
 * 
 * Reads the coordination board, checks task statuses and dependencies,
 * detects zombie/stale tasks, and reports what needs action.
 * 
 * Manual dispatch for now — auto-dispatch requires gateway integration.
 * 
 * Usage: node .coordination/board/emmaus/dispatcher.js [check|dispatch|reclaim|report]
 */

const fs = require('fs');
const path = require('path');

// Configuration
const BOARD_DIR = path.join(__dirname, 'tasks');
const LINKS_FILE = path.join(__dirname, 'links.md');
const AGENTS_DIR = path.join(__dirname, '..', '..', 'agents', 'emmaus-specialists');
const ZOMBIE_TIMEOUT_MS = 10 * 60 * 1000; // 10 minutes

// ANSI colors
const C = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
};

// Task status lifecycle
const STATUS_ORDER = ['triage', 'todo', 'ready', 'running', 'blocked', 'done', 'archived'];
const ACTIVE_STATUSES = ['triage', 'todo', 'ready', 'running', 'blocked'];

/**
 * Parse a task file into structured data
 */
function parseTask(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  
  const task = {
    id: path.basename(filePath, '.md').split('-')[0],
    file: filePath,
    title: '',
    status: 'unknown',
    assignee: 'unassigned',
    priority: 'medium',
    blockedBy: [],
    created: null,
    started: null,
    completed: null,
    comments: [],
    output: '',
    metadata: {},
  };
  
  let inComments = false;
  let inOutput = false;
  let inMetadata = false;
  let currentComment = null;
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // Title
    if (trimmed.startsWith('# Task')) {
      task.title = trimmed.replace('# Task ', '').trim();
    }
    
    // Status
    if (trimmed.startsWith('**Status:**')) {
      task.status = trimmed.replace('**Status:**', '').trim();
    }
    
    // Assignee
    if (trimmed.startsWith('**Assignee:**')) {
      task.assignee = trimmed.replace('**Assignee:**', '').trim();
    }
    
    // Priority
    if (trimmed.startsWith('**Priority:**')) {
      task.priority = trimmed.replace('**Priority:**', '').trim();
    }
    
    // Blocked by
    if (trimmed.startsWith('**Blocked by:**')) {
      const deps = trimmed.replace('**Blocked by:**', '').trim();
      if (deps && !deps.toLowerCase().includes('none') && !deps.toLowerCase().includes('soft')) {
        task.blockedBy = deps.split(',').map(d => d.trim()).filter(d => {
          const clean = d.replace(/\(.*?\)/g, '').trim();
          return clean && !clean.toLowerCase().includes('none');
        }).map(d => {
          // Extract just the task ID from strings like "001-theological-review" or "001"
          const match = d.match(/^(\d+)/);
          return match ? match[1].padStart(3, '0') : d.trim().substring(0, 3);
        });
      }
    }
    
    // Dates
    if (trimmed.startsWith('**Created:**')) {
      const dateStr = trimmed.replace('**Created:**', '').trim();
      if (dateStr && !dateStr.includes('pending')) {
        task.created = new Date(dateStr);
      }
    }
    if (trimmed.startsWith('**Started:**')) {
      const dateStr = trimmed.replace('**Started:**', '').trim();
      if (dateStr && !dateStr.includes('pending')) {
        task.started = new Date(dateStr);
      }
    }
    if (trimmed.startsWith('**Completed:**')) {
      const dateStr = trimmed.replace('**Completed:**', '').trim();
      if (dateStr && !dateStr.includes('pending')) {
        task.completed = new Date(dateStr);
      }
    }
    
    // Comments section
    if (trimmed === '## Comments') {
      inComments = true;
      inOutput = false;
      inMetadata = false;
      continue;
    }
    
    // Output section
    if (trimmed === '## Output') {
      inOutput = true;
      inComments = false;
      inMetadata = false;
      continue;
    }
    
    // Metadata section
    if (trimmed === '## Metadata') {
      inMetadata = true;
      inOutput = false;
      inComments = false;
      continue;
    }
    
    // Parse comments
    if (inComments && trimmed.startsWith('###')) {
      const match = trimmed.match(/###\s+(.+)\s+@\s+(.+)/);
      if (match) {
        if (currentComment) task.comments.push(currentComment);
        currentComment = { agent: match[1].trim(), timestamp: match[2].trim(), text: '' };
      }
    } else if (inComments && currentComment && trimmed) {
      currentComment.text += (currentComment.text ? '\n' : '') + trimmed;
    }
    
    // Parse metadata
    if (inMetadata && trimmed.startsWith('-')) {
      const metaMatch = trimmed.match(/^-\s+\*\*(\w+)\*\*:\s*(.+)$/);
      if (metaMatch) {
        task.metadata[metaMatch[1]] = metaMatch[2];
      }
    }
  }
  
  if (currentComment) task.comments.push(currentComment);
  
  return task;
}

/**
 * Load all tasks from the board
 */
function loadTasks() {
  const tasks = [];
  
  if (!fs.existsSync(BOARD_DIR)) {
    console.log(`${C.red}Board directory not found: ${BOARD_DIR}${C.reset}`);
    return tasks;
  }
  
  const files = fs.readdirSync(BOARD_DIR).filter(f => f.endsWith('.md'));
  
  for (const file of files) {
    const task = parseTask(path.join(BOARD_DIR, file));
    tasks.push(task);
  }
  
  // Sort by ID
  tasks.sort((a, b) => parseInt(a.id) - parseInt(b.id));
  
  return tasks;
}

/**
 * Check if a task's dependencies are all done
 */
function dependenciesMet(task, allTasks) {
  if (!task.blockedBy || task.blockedBy.length === 0) return true;
  
  for (const depId of task.blockedBy) {
    const dep = allTasks.find(t => t.id === depId.padStart(3, '0'));
    if (!dep) {
      console.log(`  ${C.yellow}⚠ Dependency not found: ${depId}${C.reset}`);
      return false;
    }
    if (dep.status !== 'done' && dep.status !== 'archived') {
      return false;
    }
  }
  
  return true;
}

/**
 * Check for zombie tasks (running too long)
 */
function checkZombies(tasks) {
  const now = new Date();
  const zombies = [];
  
  for (const task of tasks) {
    if (task.status === 'running' && task.started) {
      const elapsed = now - task.started;
      if (elapsed > ZOMBIE_TIMEOUT_MS) {
        zombies.push({
          ...task,
          elapsedMinutes: Math.floor(elapsed / 60000),
        });
      }
    }
  }
  
  return zombies;
}

/**
 * Check for tasks that can be promoted
 */
function checkPromotions(tasks) {
  const promotions = [];
  
  for (const task of tasks) {
    if (task.status === 'todo' && dependenciesMet(task, tasks)) {
      promotions.push({
        ...task,
        reason: 'All dependencies completed',
      });
    }
  }
  
  return promotions;
}

/**
 * Check for tasks ready to dispatch
 */
function checkReady(tasks) {
  return tasks.filter(t => t.status === 'ready');
}

/**
 * Check for blocked tasks
 */
function checkBlocked(tasks) {
  return tasks.filter(t => t.status === 'blocked');
}

/**
 * Print board status report
 */
function printReport(tasks) {
  console.log(`\n${C.bold}${C.cyan}═══════════════════════════════════════════════${C.reset}`);
  console.log(`${C.bold}${C.cyan}  EMMAUS TASK BOARD — STATUS REPORT${C.reset}`);
  console.log(`${C.bold}${C.cyan}═══════════════════════════════════════════════${C.reset}\n`);
  
  // Summary by status
  const byStatus = {};
  for (const status of STATUS_ORDER) {
    byStatus[status] = tasks.filter(t => t.status === status);
  }
  
  console.log(`${C.bold}📊 Summary:${C.reset}`);
  for (const status of STATUS_ORDER) {
    const count = byStatus[status]?.length || 0;
    const color = status === 'done' ? C.green : 
                  status === 'running' ? C.blue :
                  status === 'blocked' ? C.red :
                  status === 'ready' ? C.cyan :
                  status === 'todo' ? C.yellow : C.reset;
    if (count > 0 || status !== 'archived') {
      console.log(`  ${color}${status.toUpperCase().padEnd(10)}${C.reset}: ${count} tasks`);
    }
  }
  
  // Active tasks detail
  console.log(`\n${C.bold}📋 Active Tasks:${C.reset}`);
  for (const task of tasks.filter(t => ACTIVE_STATUSES.includes(t.status))) {
    const statusColor = task.status === 'running' ? C.blue :
                       task.status === 'blocked' ? C.red :
                       task.status === 'ready' ? C.cyan :
                       task.status === 'todo' ? C.yellow : C.reset;
    const priorityColor = task.priority === 'high' ? C.red :
                         task.priority === 'medium' ? C.yellow : C.reset;
    
    console.log(`  [${task.id}] ${statusColor}${task.status.padEnd(8)}${C.reset} ${priorityColor}${task.priority.padEnd(6)}${C.reset} ${task.assignee.padEnd(20)} ${task.title}`);
    
    if (task.blockedBy.length > 0) {
      const depsDone = task.blockedBy.map(dep => {
        const depTask = tasks.find(t => t.id === dep.padStart(3, '0'));
        return depTask?.status === 'done' ? `${C.green}${dep}${C.reset}` : `${C.yellow}${dep}${C.reset}`;
      }).join(', ');
      console.log(`       └─ depends on: ${depsDone}`);
    }
  }
  
  // Zombies
  const zombies = checkZombies(tasks);
  if (zombies.length > 0) {
    console.log(`\n${C.bold}${C.red}🧟 ZOMBIE TASKS (running > ${ZOMBIE_TIMEOUT_MS / 60000} min):${C.reset}`);
    for (const task of zombies) {
      console.log(`  [${task.id}] ${task.title} — running for ${task.elapsedMinutes} min`);
      console.log(`       └─ ${C.yellow}Action: Reclaim and re-dispatch${C.reset}`);
    }
  }
  
  // Promotions
  const promotions = checkPromotions(tasks);
  if (promotions.length > 0) {
    console.log(`\n${C.bold}${C.green}⬆️  READY TO PROMOTE (todo → ready):${C.reset}`);
    for (const task of promotions) {
      console.log(`  [${task.id}] ${task.title}`);
      console.log(`       └─ ${C.cyan}Action: Change status to 'ready'${C.reset}`);
    }
  }
  
  // Ready to dispatch
  const ready = checkReady(tasks);
  if (ready.length > 0) {
    console.log(`\n${C.bold}${C.cyan}🚀 READY TO DISPATCH:${C.reset}`);
    for (const task of ready) {
      console.log(`  [${task.id}] ${task.title} → ${task.assignee}`);
      console.log(`       └─ ${C.cyan}Action: Dispatch agent${C.reset}`);
    }
  }
  
  // Blocked
  const blocked = checkBlocked(tasks);
  if (blocked.length > 0) {
    console.log(`\n${C.bold}${C.red}🚫 BLOCKED TASKS:${C.reset}`);
    for (const task of blocked) {
      console.log(`  [${task.id}] ${task.title}`);
      if (task.metadata.blocked_reason) {
        console.log(`       └─ ${C.red}Reason: ${task.metadata.blocked_reason}${C.reset}`);
      }
      console.log(`       └─ ${C.yellow}Action: Investigate and unblock${C.reset}`);
    }
  }
  
  // Done
  const done = tasks.filter(t => t.status === 'done');
  if (done.length > 0) {
    console.log(`\n${C.bold}${C.green}✅ COMPLETED:${C.reset}`);
    for (const task of done) {
      console.log(`  [${task.id}] ${task.title}`);
    }
  }
  
  console.log(`\n${C.bold}${C.cyan}═══════════════════════════════════════════════${C.reset}\n`);
}

/**
 * Generate dispatch commands for ready tasks
 */
function generateDispatch(tasks) {
  const ready = checkReady(tasks);
  
  if (ready.length === 0) {
    console.log(`${C.yellow}No tasks ready for dispatch.${C.reset}`);
    return;
  }
  
  console.log(`\n${C.bold}${C.cyan}🚀 DISPATCH COMMANDS:${C.reset}\n`);
  
  for (const task of ready) {
    const agentName = task.assignee.replace('emmaus-', '');
    const profilePath = path.join(AGENTS_DIR, `${agentName}.md`);
    const hasProfile = fs.existsSync(profilePath);
    
    console.log(`${C.bold}[${task.id}] ${task.title}${C.reset}`);
    console.log(`  Assignee: ${task.assignee}`);
    console.log(`  Profile: ${hasProfile ? `${C.green}✓ Found` : `${C.red}✗ Missing`} ${profilePath}${C.reset}`);
    console.log(`  Task file: ${task.file}`);
    
    if (hasProfile) {
      console.log(`\n  ${C.cyan}Suggested spawn command:${C.reset}`);
      console.log(`  sessions_spawn({`);
      console.log(`    task: "Read profile at ${profilePath} and task at ${task.file}. Execute to completion. Update task file with status, output, and metadata.",`);
      console.log(`    label: "${task.assignee}",`);
      console.log(`    mode: "run",`);
      console.log(`    context: "fork",`);
      console.log(`    taskName: "${task.assignee}-${task.id}"`);
      console.log(`  })`);
    }
    
    console.log('');
  }
}

/**
 * Check command — full status report
 */
function cmdCheck() {
  const tasks = loadTasks();
  printReport(tasks);
}

/**
 * Dispatch command — show what to dispatch
 */
function cmdDispatch() {
  const tasks = loadTasks();
  printReport(tasks);
  generateDispatch(tasks);
}

/**
 * Reclaim command — show zombie tasks
 */
function cmdReclaim() {
  const tasks = loadTasks();
  const zombies = checkZombies(tasks);
  
  if (zombies.length === 0) {
    console.log(`${C.green}No zombie tasks detected.${C.reset}`);
    return;
  }
  
  console.log(`\n${C.bold}${C.red}🧟 ZOMBIE TASKS:${C.reset}\n`);
  
  for (const task of zombies) {
    console.log(`${C.bold}[${task.id}] ${task.title}${C.reset}`);
    console.log(`  Status: ${C.blue}running${C.reset} (stuck for ${task.elapsedMinutes} min)`);
    console.log(`  Assignee: ${task.assignee}`);
    console.log(`  File: ${task.file}`);
    console.log(`\n  ${C.yellow}To reclaim manually:${C.reset}`);
    console.log(`  1. Read ${task.file} — check if agent actually finished`);
    console.log(`  2. If finished: update status to 'done', add completion timestamp`);
    console.log(`  3. If stuck: update status to 'blocked', add blocked_reason`);
    console.log(`  4. Re-dispatch if needed`);
    console.log('');
  }
}

/**
 * Main
 */
function main() {
  const command = process.argv[2] || 'check';
  
  console.log(`${C.bold}${C.magenta}🛤️  EMMAUS TASK DISPATCHER${C.reset} v1.0\n`);
  
  switch (command) {
    case 'check':
      cmdCheck();
      break;
    case 'dispatch':
      cmdDispatch();
      break;
    case 'reclaim':
      cmdReclaim();
      break;
    case 'report':
      cmdCheck();
      break;
    default:
      console.log(`${C.yellow}Unknown command: ${command}${C.reset}`);
      console.log(`\nUsage: node dispatcher.js [check|dispatch|reclaim|report]`);
      console.log(`  check    — Full status report (default)`);
      console.log(`  dispatch — Show ready tasks and dispatch commands`);
      console.log(`  reclaim  — Show zombie tasks to reclaim`);
      console.log(`  report   — Same as check`);
      process.exit(1);
  }
}

main();
