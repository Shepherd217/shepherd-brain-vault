"use client";

import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Activity, Clock, CheckCircle, AlertCircle } from "lucide-react";

interface AgentPresence {
  id: string;
  name: string;
  emoji: string;
  status: "idle" | "working" | "offline" | "error";
  currentTask: string | null;
  lastSeen: string;
}

const mockAgents: AgentPresence[] = [
  {
    id: "ava",
    name: "Ava",
    emoji: "🟡",
    status: "working",
    currentTask: "Building goal system",
    lastSeen: new Date().toISOString(),
  },
  {
    id: "hermes",
    name: "Hermes",
    emoji: "🟢",
    status: "idle",
    currentTask: null,
    lastSeen: new Date(Date.now() - 300000).toISOString(),
  },
  {
    id: "eve",
    name: "Eve",
    emoji: "🔵",
    status: "offline",
    currentTask: null,
    lastSeen: new Date(Date.now() - 3600000).toISOString(),
  },
];

export function AgentPresencePanel() {
  const [agents, setAgents] = useState<AgentPresence[]>(mockAgents);

  useEffect(() => {
    // Poll for real agent statuses
    const interval = setInterval(() => {
      // In real implementation, fetch from /api/agents/status
      setAgents((prev) =>
        prev.map((a) => ({
          ...a,
          lastSeen:
            a.status === "working"
              ? new Date().toISOString()
              : a.lastSeen,
        }))
      );
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  const statusConfig = {
    idle: { icon: Clock, color: "text-green-500", bg: "bg-green-50", label: "Idle" },
    working: { icon: Activity, color: "text-yellow-500", bg: "bg-yellow-50", label: "Working" },
    offline: { icon: AlertCircle, color: "text-gray-400", bg: "bg-gray-50", label: "Offline" },
    error: { icon: AlertCircle, color: "text-red-500", bg: "bg-red-50", label: "Error" },
  };

  return (
    <Card>
      <CardContent className="p-3">
        <div className="space-y-2">
          {agents.map((agent) => {
            const config = statusConfig[agent.status];
            const StatusIcon = config.icon;
            return (
              <div
                key={agent.id}
                className={`flex items-center gap-2 p-2 rounded-lg ${config.bg}`}
              >
                <StatusIcon className={`h-3.5 w-3.5 ${config.color}`} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1">
                    <span className="text-sm font-medium">{agent.emoji} {agent.name}</span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded-full bg-background ${config.color}`}>
                      {config.label}
                    </span>
                  </div>
                  {agent.currentTask && (
                    <p className="text-xs text-muted-foreground truncate">
                      {agent.currentTask}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
