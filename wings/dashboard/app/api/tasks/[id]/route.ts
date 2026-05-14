import { NextResponse } from "next/server";
import type { Task, TaskStatus } from "@/types";

// Shared in-memory store (same as route.ts)
declare global {
  var __tasks: Task[] | undefined;
}

const tasks = globalThis.__tasks ?? [];
if (!globalThis.__tasks) {
  globalThis.__tasks = tasks;
}

const validTransitions: Record<TaskStatus, TaskStatus[]> = {
  backlog: ["todo"],
  todo: ["doing"],
  doing: ["review", "done", "failed"],
  review: ["done", "doing", "failed"],
  done: [],
  failed: ["todo"],
};

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const task = tasks.find(t => t.id === params.id);
  
  if (!task) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }
  
  return NextResponse.json({ task });
}

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    
    const existingIndex = tasks.findIndex(t => t.id === params.id);
    if (existingIndex === -1) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 });
    }
    
    const existing = tasks[existingIndex];
    
    // Validate status transition
    if (body.status && body.status !== existing.status) {
      const currentStatus = existing.status as TaskStatus;
      const newStatus = body.status as TaskStatus;
      
      if (!validTransitions[currentStatus]?.includes(newStatus)) {
        return NextResponse.json(
          { error: `Invalid transition: ${currentStatus} → ${newStatus}` },
          { status: 400 }
        );
      }
    }
    
    const updates: Partial<Task> = {};
    if (body.title !== undefined) updates.title = body.title;
    if (body.description !== undefined) updates.description = body.description;
    if (body.status !== undefined) updates.status = body.status;
    if (body.priority !== undefined) updates.priority = body.priority;
    if (body.owner !== undefined) updates.owner = body.owner;
    if (body.agentType !== undefined) updates.agentType = body.agentType;
    if (body.tags !== undefined) updates.tags = body.tags;
    if (body.result !== undefined) updates.result = body.result;
    if (body.error !== undefined) updates.error = body.error;
    
    // Auto-set timestamps
    if (body.status === "doing" && existing.status !== "doing") {
      updates.startedAt = new Date();
    }
    if ((body.status === "done" || body.status === "failed") && 
        existing.status !== "done" && existing.status !== "failed") {
      updates.completedAt = new Date();
    }
    if (body.status === "failed") {
      updates.attempts = (existing.attempts || 0) + 1;
    }
    
    tasks[existingIndex] = { ...existing, ...updates };
    
    return NextResponse.json({ task: tasks[existingIndex] });
  } catch (error) {
    return NextResponse.json({ error: "Failed to update task" }, { status: 500 });
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const existingIndex = tasks.findIndex(t => t.id === params.id);
  if (existingIndex === -1) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }
  
  tasks.splice(existingIndex, 1);
  return NextResponse.json({ ok: true });
}
