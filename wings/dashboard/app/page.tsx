"use client";

import { useState, useEffect } from "react";
import { KanbanBoard } from "@/components/kanban/Board";
import { AgentSidebar } from "@/components/AgentSidebar";
import { ActivityFeed } from "@/components/ActivityFeed";
import { CommandBar } from "@/components/CommandBar";
import { AgentPresencePanel } from "@/components/AgentPresence";
import { BottomNav } from "@/components/BottomNav";
import { CreateTaskModal } from "@/components/CreateTaskModal";

export default function Home() {
  const [activeTab, setActiveTab] = useState("board");
  const [isMobile, setIsMobile] = useState(false);
  const [createTaskOpen, setCreateTaskOpen] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  async function handleSendMessage(msg: string, to: string) {
    try {
      await fetch("/api/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from: "nathan", to, content: msg, type: "message" }),
      });
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  }

  async function handleSetGoal(goal: string) {
    try {
      await fetch("/api/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent: "nathan", type: "goal_set", content: `Set goal: ${goal}` }),
      });
    } catch (error) {
      console.error("Failed to set goal:", error);
    }
  }

  return (
    <main className="flex h-screen overflow-hidden bg-background">
      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0">
        {isMobile ? (
          <>
            {/* Mobile: Tab-based view */}
            <div className="flex-1 overflow-hidden">
              {activeTab === "board" && (
                <KanbanBoard />
              )}
              {activeTab === "activity" && (
                <div className="h-full p-3 overflow-y-auto">
                  <ActivityFeed />
                </div>
              )}
              {activeTab === "team" && (
                <div className="h-full p-3 overflow-y-auto space-y-3">
                  <AgentPresencePanel />
                  <CommandBar onSendMessage={handleSendMessage} onSetGoal={handleSetGoal} />
                </div>
              )}
            </div>
            <BottomNav
              activeTab={activeTab}
              onTabChange={setActiveTab}
              onCreateTask={() => setCreateTaskOpen(true)}
            />
          </>
        ) : (
          <>
            {/* Desktop: Full layout */}
            <KanbanBoard />
          </>
        )}
      </div>

      {/* Desktop sidebar */}
      {!isMobile && (
        <div className="w-72 border-l border-border flex-shrink-0 bg-card overflow-y-auto">
          <div className="p-3 space-y-3">
            <AgentPresencePanel />
            <ActivityFeed />
            <CommandBar onSendMessage={handleSendMessage} onSetGoal={handleSetGoal} />
          </div>
        </div>
      )}

      {/* Create Task Modal */}
      <CreateTaskModal
        open={createTaskOpen}
        onOpenChange={setCreateTaskOpen}
        onTaskCreated={() => setCreateTaskOpen(false)}
      />
    </main>
  );
}
