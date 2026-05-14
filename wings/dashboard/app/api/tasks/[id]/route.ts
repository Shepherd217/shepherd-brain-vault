import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { tasks } from "@/lib/db/schema";
import { eq } from "drizzle-orm";
import { z } from "zod";
import type { TaskStatus } from "@/types";

const updateSchema = z.object({
  title: z.string().min(1).max(200).optional(),
  description: z.string().optional(),
  status: z.enum(["backlog", "todo", "doing", "review", "done", "failed"]).optional(),
  priority: z.enum(["low", "medium", "high", "critical"]).optional(),
  owner: z.string().optional(),
  agentType: z.enum(["openclaw", "hermes", "human"]).optional(),
  tags: z.array(z.string()).optional(),
  result: z.string().optional(),
  error: z.string().optional(),
});

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
  const task = await db.select().from(tasks).where(eq(tasks.id, params.id)).get();
  
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
    const parsed = updateSchema.parse(body);
    
    const existing = await db.select().from(tasks).where(eq(tasks.id, params.id)).get();
    if (!existing) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 });
    }
    
    // Validate status transition
    if (parsed.status && parsed.status !== existing.status) {
      const currentStatus = existing.status as TaskStatus;
      const newStatus = parsed.status;
      
      if (!validTransitions[currentStatus]?.includes(newStatus)) {
        return NextResponse.json(
          { error: `Invalid transition: ${currentStatus} → ${newStatus}` },
          { status: 400 }
        );
      }
    }
    
    const updates: Record<string, unknown> = { ...parsed };
    
    if (parsed.tags) {
      updates.tags = JSON.stringify(parsed.tags);
    }
    
    // Auto-set timestamps
    if (parsed.status === "doing" && existing.status !== "doing") {
      updates.startedAt = new Date();
    }
    if ((parsed.status === "done" || parsed.status === "failed") && 
        existing.status !== "done" && existing.status !== "failed") {
      updates.completedAt = new Date();
    }
    if (parsed.status === "failed") {
      updates.attempts = existing.attempts + 1;
    }
    
    await db.update(tasks).set(updates).where(eq(tasks.id, params.id));
    
    const updated = await db.select().from(tasks).where(eq(tasks.id, params.id)).get();
    return NextResponse.json({ task: updated });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ error: error.errors }, { status: 400 });
    }
    return NextResponse.json({ error: "Failed to update task" }, { status: 500 });
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const existing = await db.select().from(tasks).where(eq(tasks.id, params.id)).get();
  if (!existing) {
    return NextResponse.json({ error: "Task not found" }, { status: 404 });
  }
  
  await db.delete(tasks).where(eq(tasks.id, params.id));
  return NextResponse.json({ ok: true });
}
