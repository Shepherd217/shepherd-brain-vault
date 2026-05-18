import { NextResponse } from "next/server";
import type { Task, TaskStatus } from "@/types";
import { getTaskById, updateTask, deleteTask } from "@/lib/db";

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
  const task = getTaskById(params.id);
  
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
    const existing = getTaskById(params.id);
    
    if (!existing) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 });
    }
    
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
    
    const updated = updateTask(params.id, updates);
    
    return NextResponse.json({ task: updated });
  } catch (error) {
    return NextResponse.json({ error: "Failed to update task" }, { status: 500 });
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const ok = deleteTask(params.id);
  if (!ok) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }
  
  return NextResponse.json({ ok: true });
}
