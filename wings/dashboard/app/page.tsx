"use client";

import { useState, useEffect } from "react";
import { KanbanBoard } from "@/components/kanban/Board";
import { AgentSidebar } from "@/components/AgentSidebar";
import { Button } from "@/components/ui/button";
import { Users, X } from "lucide-react";

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  return (
    <main className="flex h-screen overflow-hidden bg-background">
      {/* Main board area */}
      <div className="flex-1 flex flex-col min-w-0">
        <KanbanBoard
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          sidebarOpen={sidebarOpen}
        />
      </div>

      {/* Agent Sidebar - desktop always visible, mobile overlay */}
      <div
        className={`
          ${isMobile
            ? `fixed inset-y-0 right-0 z-50 w-[280px] transform transition-transform duration-300 ${sidebarOpen ? "translate-x-0" : "translate-x-full"}`
            : "w-64 border-l flex-shrink-0"
          }
          bg-card flex flex-col
        `}
      >
        {isMobile && sidebarOpen && (
          <div className="flex items-center justify-between p-3 border-b">
            <span className="font-semibold text-sm">Team Status</span>
            <Button variant="ghost" size="sm" onClick={() => setSidebarOpen(false)}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        )}
        <AgentSidebar />
      </div>

      {/* Mobile overlay backdrop */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Mobile floating sidebar toggle */}
      {isMobile && !sidebarOpen && (
        <Button
          className="fixed bottom-4 right-4 z-30 rounded-full h-14 w-14 shadow-lg"
          onClick={() => setSidebarOpen(true)}
        >
          <Users className="h-5 w-5" />
        </Button>
      )}
    </main>
  );
}
