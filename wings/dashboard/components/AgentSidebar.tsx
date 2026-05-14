"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, CheckCircle, Clock, AlertCircle, PauseCircle } from "lucide-react";

interface Agent {
  id: string;
  name: string;
  type: string;
  status: "idle" | "working" | "offline" | "error" | "paused";
  currentTask: string | null;
  lastSeen: Date;
}

export function AgentSidebar() {
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: "ava",
      name: "Ava",
      type: "openclaw",
      status: "working",
      currentTask: "Building dashboard...",
      lastSeen: new Date(),
    },
    {
      id: "hermes",
      name: "Hermes",
      type: "hermes",
      status: "idle",
      currentTask: null,
      lastSeen: new Date(),
    },
    {
      id: "eve",
      name: "Eve",
      type: "openclaw",
      status: "offline",
      currentTask: null,
      lastSeen: new Date(Date.now() - 86400000),
    },
  ]);

  useEffect(() => {
    // Poll for real agent status updates via WebSocket in Phase 2
    const interval = setInterval(() => {
      setAgents((prev) =>
        prev.map((a) => ({
          ...a,
          lastSeen: a.status === "working" ? new Date() : a.lastSeen,
        }))
      );
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  const statusConfig = {
    idle: { icon: Clock, color: "text-green-500", bg: "bg-green-50", label: "Idle" },
    working: { icon: Activity, color: "text-yellow-500", bg: "bg-yellow-50", label: "Working" },
    offline: { icon: PauseCircle, color: "text-gray-400", bg: "bg-gray-50", label: "Offline" },
    error: { icon: AlertCircle, color: "text-red-500", bg: "bg-red-50", label: "Error" },
    paused: { icon: PauseCircle, color: "text-orange-500", bg: "bg-orange-50", label: "Paused" },
  };

  const activeAgents = agents.filter((a) => a.status === "working").length;

  return (
    <div className="flex flex-col h-full p-3 md:p-4 gap-3 overflow-y-auto">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-xs md:text-sm font-semibold flex items-center gap-2">
            <CheckCircle className="h-3.5 w-3.5 text-green-500" />
            Team Status
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="text-2xl md:text-3xl font-bold">{activeAgents}</div>
          <p className="text-xs text-muted-foreground">active now</p>
          <div className="mt-2 flex gap-2 text-[10px] md:text-xs">
            <span className="text-muted-foreground">{agents.length} total</span>
            <span className="text-muted-foreground">·</span>
            <span className="text-yellow-500">{agents.filter((a) => a.status === "working").length} working</span>
          </div>
        </CardContent>
      </Card>

      <div className="space-y-2">
        <h3 className="text-xs md:text-sm font-semibold text-muted-foreground uppercase tracking-wider">Agents</h3>
        {agents.map((agent) => {
          const config = statusConfig[agent.status];
          const StatusIcon = config.icon;
          return (
            <div
              key={agent.id}
              className={`rounded-lg border p-2 md:p-3 transition-colors hover:bg-accent/50 ${config.bg}`}
            >
              <div className="flex items-center gap-2 mb-1">
                <StatusIcon className={`h-3.5 w-3.5 ${config.color}`} />
                <span className="font-medium text-xs md:text-sm">{agent.name}</span>
                <span className={`ml-auto text-[10px] md:text-xs px-1.5 py-0.5 rounded-full bg-background font-medium ${config.color}`}>
                  {config.label}
                </span>
              </div>
              {agent.currentTask && (
                <p className="text-[10px] md:text-xs text-muted-foreground truncate">
                  {agent.currentTask}
                </p>
              )}
              <p className="text-[10px] text-muted-foreground mt-1">
                {agent.type} · {Math.round((Date.now() - agent.lastSeen.getTime()) / 60000)}m ago
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
