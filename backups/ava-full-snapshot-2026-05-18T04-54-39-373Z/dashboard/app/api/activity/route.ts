import { NextResponse } from "next/server";

// In-memory activity log (replaces SQLite for serverless)
const activities: any[] = [
  {
    id: "1",
    agent: "ava",
    type: "goal_set",
    content: "Set goal: Build mobile-friendly dashboard",
    timestamp: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    id: "2",
    agent: "ava",
    type: "task_created",
    content: "Created task: Implement snap-scroll columns",
    timestamp: new Date(Date.now() - 3000000).toISOString(),
  },
  {
    id: "3",
    agent: "ava",
    type: "deploy",
    content: "Deployed dashboard to Vercel",
    timestamp: new Date(Date.now() - 1800000).toISOString(),
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const agent = searchParams.get("agent");
  const limit = parseInt(searchParams.get("limit") || "50");

  let filtered = [...activities];
  if (agent) {
    filtered = filtered.filter((a) => a.agent === agent);
  }

  filtered.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  const limited = filtered.slice(0, limit);

  return NextResponse.json({ activities: limited });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const activity = {
      id: crypto.randomUUID(),
      agent: body.agent || "unknown",
      type: body.type || "update",
      content: body.content,
      timestamp: new Date().toISOString(),
    };

    activities.unshift(activity);
    // Keep only last 100
    if (activities.length > 100) activities.pop();

    return NextResponse.json({ activity }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Failed to log activity" }, { status: 500 });
  }
}
