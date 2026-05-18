import { NextResponse } from "next/server";
import { getAgents, detectZombies, reclaimTasksFromZombies } from "@/lib/db";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const runReclaim = searchParams.get("reclaim") === "true";

    // Run zombie detection and reclaim
    const zombies = detectZombies();
    const reclaimed = runReclaim ? reclaimTasksFromZombies() : [];

    const agents = getAgents();

    return NextResponse.json({
      agents,
      zombies: zombies.map((z) => ({ id: z.id, name: z.name })),
      reclaimed: reclaimed.map((t) => ({ id: t.id, title: t.title })),
    });
  } catch (error) {
    return NextResponse.json({ error: "Failed to get agent status" }, { status: 500 });
  }
}
