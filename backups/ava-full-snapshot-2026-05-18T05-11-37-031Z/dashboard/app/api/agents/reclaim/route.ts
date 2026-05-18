import { NextResponse } from "next/server";
import { reclaimTasksFromZombies } from "@/lib/db";

export async function POST(request: Request) {
  try {
    const reclaimed = reclaimTasksFromZombies();

    return NextResponse.json({
      ok: true,
      reclaimed: reclaimed.map((t) => ({ id: t.id, title: t.title, owner: t.owner })),
      message:
        reclaimed.length > 0
          ? `Reclaimed ${reclaimed.length} task(s) from zombie agents`
          : "No zombie tasks to reclaim",
    });
  } catch (error) {
    return NextResponse.json({ error: "Reclaim failed" }, { status: 500 });
  }
}
