"use client";

import { KanbanBoard } from "@/components/kanban/Board";
import { AgentSidebar } from "@/components/AgentSidebar";

export default function Home() {
  return (
    <main className="flex h-screen overflow-hidden">
      <div className="flex-1 overflow-hidden">
        <KanbanBoard />
      </div>
      <AgentSidebar />
    </main>
  );
}
