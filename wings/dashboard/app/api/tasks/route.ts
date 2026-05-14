import { NextResponse } from "next/server";
import type { Task, TaskStatus } from "@/types";

// In-memory task store for serverless demo (replaces SQLite)
const tasks: Task[] = [];

const validTransitions: Record<TaskStatus, TaskStatus[]> = {
  backlog: ["todo"],
  todo: ["doing"],
  doing: ["review", "done", "failed"],
  review: ["done", "doing", "failed"],
  done: [],
  failed: ["todo"],
};

function canTransition(from: TaskStatus, to: TaskStatus): boolean {
  return validTransitions[from]?.includes(to) ?? false;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  
  const status = searchParams.get("status");
  const owner = searchParams.get("owner");
  const tag = searchParams.get("tag");
  const projectId = searchParams.get("projectId") ?? "shepherd";
  
  let filtered = tasks.filter(t => t.projectId === projectId);
  
  if (status) {
    filtered = filtered.filter(t => t.status === status);
  }
  if (owner) {
    filtered = filtered.filter(t => t.owner === owner);
  }
  if (tag) {
    filtered = filtered.filter(t => t.tags.includes(tag));
  }
  
  return NextResponse.json({ tasks: filtered });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    const task: Task = {
      id: crypto.randomUUID(),
      title: body.title,
      description: body.description || null,
      status: "backlog",
      priority: body.priority || "medium",
      owner: body.owner || null,
      agentType: body.agentType || null,
      tags: body.tags || [],
      projectId: body.projectId || "shepherd",
      dependencies: body.dependencies || [],
      createdAt: new Date(),
      startedAt: null,
      completedAt: null,
      attempts: 0,
      maxRetries: body.maxRetries || 3,
      worktreeId: null,
      result: null,
      error: null,
      requiresReview: body.requiresReview || false,
      nextTask: null,
    };
    
    tasks.push(task);
    
    return NextResponse.json({ task }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Failed to create task" }, { status: 500 });
  }
}
