import { NextResponse } from "next/server";

// In-memory messages (replaces SQLite for serverless)
const messages: any[] = [];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const from = searchParams.get("from");
  const to = searchParams.get("to");
  const limit = parseInt(searchParams.get("limit") || "50");

  let filtered = [...messages];
  if (from) {
    filtered = filtered.filter((m) => m.from === from);
  }
  if (to) {
    filtered = filtered.filter((m) => m.to === to || m.to === "broadcast");
  }

  filtered.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  const limited = filtered.slice(0, limit);

  return NextResponse.json({ messages: limited });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const message = {
      id: crypto.randomUUID(),
      from: body.from || "unknown",
      to: body.to || "broadcast",
      content: body.content,
      type: body.type || "message",
      taskId: body.taskId || null,
      timestamp: new Date().toISOString(),
    };

    messages.unshift(message);
    // Keep only last 200
    if (messages.length > 200) messages.pop();

    return NextResponse.json({ message }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Failed to send message" }, { status: 500 });
  }
}
