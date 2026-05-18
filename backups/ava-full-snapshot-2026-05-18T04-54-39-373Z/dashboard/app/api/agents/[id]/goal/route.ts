import { NextResponse } from "next/server";
import { getAgentGoal, setAgentGoal, clearAgentGoal } from "@/lib/goals";
import { getTaskById } from "@/lib/db";

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const goal = getAgentGoal(params.id);
  if (!goal) {
    return NextResponse.json({ goal: null });
  }

  const task = getTaskById(goal.taskId);
  return NextResponse.json({
    goal: {
      ...goal,
      task: task || null,
    },
  });
}

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const { taskId, notes } = body;

    if (!taskId) {
      return NextResponse.json({ error: "taskId required" }, { status: 400 });
    }

    const task = getTaskById(taskId);
    if (!task) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 });
    }

    const goal = setAgentGoal(params.id, taskId, notes);

    return NextResponse.json({
      goal: {
        ...goal,
        task,
      },
    });
  } catch (error) {
    return NextResponse.json({ error: "Failed to set goal" }, { status: 500 });
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const cleared = clearAgentGoal(params.id);
  return NextResponse.json({ ok: cleared });
}
