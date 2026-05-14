"use client";

import { useState, useEffect } from "react";
import { KanbanBoard } from "@/components/kanban/Board";
import { AgentSidebar } from "@/components/AgentSidebar";
import { ActivityFeed } from "@/components/ActivityFeed";
import { CommandBar } from "@/components/CommandBar";
import { AgentPresencePanel } from "@/components/AgentPresence";
import { Button } from "@/components/ui/button";
import { Users, X, MessageSquare, Activity } from "lucide-react";

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activityPanelOpen, setActivityPanelOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

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
        body: JSON.stringify({
          agent: "nathan",
          type: "goal_set",
          content: `Set goal: ${goal}`,
        }),
      });
      // TODO: Send to relay for agent to pick up
    } catch (error) {
      console.error("Failed to set goal:", error);
    }
  }

  return (
    <main className="flex h-screen overflow-hidden bg-background">
      {/* Main board area */}
      <div className="flex-1 flex flex-col min-w-0">
        <KanbanBoard
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          sidebarOpen={sidebarOpen}
        />

        {/* Command Bar at bottom */}
        <CommandBar onSendMessage={handleSendMessage} onSetGoal={handleSetGoal} />
      </div>

      {/* Right Panel: Agent Sidebar + Activity */}
      <div
        className={`
          ${isMobile
            ? `fixed inset-y-0 right-0 z-50 w-[300px] transform transition-transform duration-300 ${sidebarOpen ? "translate-x-0" : "translate-x-full"}`
            : "w-72 border-l flex-shrink-0"
          }
          bg-card flex flex-col
        `}
      >
        {isMobile && sidebarOpen && (
          <div className="flex items-center justify-between p-3 border-b">
            <span className="font-semibold text-sm">Team Hub</span>
            <Button variant="ghost" size="sm" onClick={() => setSidebarOpen(false)}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-3 space-y-3">
          <AgentPresencePanel />
          <ActivityFeed />
        </div>
      </div>

      {/* Mobile overlay backdrop */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Mobile floating buttons */}
      {isMobile && !sidebarOpen && (
        <div className="fixed bottom-20 right-4 z-30 flex flex-col gap-2">
          <Button
            className="rounded-full h-12 w-12 shadow-lg"
            onClick={() => setActivityPanelOpen(!activityPanelOpen)}
          >
            <Activity className="h-5 w-5" />
          </Button>
          <Button
            className="rounded-full h-14 w-14 shadow-lg"
            onClick={() => setSidebarOpen(true)}
          >
            <Users className="h-5 w-5" />
          </Button>
        </div>
      )}
    </main>
  );
}
