import { NextResponse } from "next/server";
import { getAgentById, upsertAgent } from "@/lib/db";
import type { Agent } from "@/types";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { id, name, agentType, gatewayId, gatewayType, gatewayUrl, models, skills, surfaces, currentTask } = body;

    if (!id || !name) {
      return NextResponse.json({ error: "id and name required" }, { status: 400 });
    }

    const now = new Date();
    const existing = getAgentById(id);

    const agent: Agent = {
      id,
      name,
      agentType: agentType || existing?.agentType || "openclaw",
      gatewayId: gatewayId || existing?.gatewayId || "",
      gatewayType: gatewayType || existing?.gatewayType || "openclaw",
      gatewayUrl: gatewayUrl || existing?.gatewayUrl || "",
      status: "idle",
      currentTask: currentTask !== undefined ? currentTask : existing?.currentTask || null,
      models: models || existing?.models || [],
      skills: skills || existing?.skills || [],
      surfaces: surfaces || existing?.surfaces || [],
      createdAt: existing?.createdAt || now,
      updatedAt: now,
    };

    // Determine status based on currentTask
    if (currentTask) {
      agent.status = "working";
    } else if (existing?.status === "error") {
      agent.status = "error";
    } else {
      agent.status = "idle";
    }

    upsertAgent(agent);

    return NextResponse.json({ agent });
  } catch (error) {
    return NextResponse.json({ error: "Heartbeat failed" }, { status: 500 });
  }
}
