import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { tasks } from "@/lib/db/schema";
import { eq, and, like, inArray } from "drizzle-orm";
import { nanoid } from "nanoid";
import { z } from "zod";
import type { TaskStatus } from "@/types";

const createTaskSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
  priority: z.enum(["low", "medium", "high", "critical"]).default("medium"),
  owner: z.string().optional(),
  agentType: z.enum(["openclaw", "hermes", "human"]).optional(),
  tags: z.array(z.string()).default([]),
  projectId: z.string().default("shepherd"),
  dependencies: z.array(z.string()).default([]),
  maxRetries: z.number().int().min(0).max(10).default(3),
  requiresReview: z.boolean().default(false),
});

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
  
  let query = db.select().from(tasks).where(eq(tasks.projectId, projectId));
  
  // Note: In production, build where clauses properly with Drizzle
  const allTasks = await db.select().from(tasks);
  
  let filtered = allTasks.filter(t => t.projectId === projectId);
  
  if (status) {
    filtered = filtered.filter(t => t.status === status);
  }
  if (owner) {
    filtered = filtered.filter(t => t.owner === owner);
  }
  if (tag) {
    filtered = filtered.filter(t => {
      try {
        const tags = JSON.parse(t.tags);
        return tags.includes(tag);
      } catch {
        return false;
      }
    });
  }
  
  return NextResponse.json({ tasks: filtered });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const parsed = createTaskSchema.parse(body);
    
    const task = {
      id: nanoid(),
      ...parsed,
      tags: JSON.stringify(parsed.tags),
      dependencies: JSON.stringify(parsed.dependencies),
      status: "backlog" as TaskStatus,
      attempts: 0,
      createdAt: new Date(),
    };
    
    await db.insert(tasks).values(task);
    
    return NextResponse.json({ task }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ error: error.errors }, { status: 400 });
    }
    return NextResponse.json({ error: "Failed to create task" }, { status: 500 });
  }
}
