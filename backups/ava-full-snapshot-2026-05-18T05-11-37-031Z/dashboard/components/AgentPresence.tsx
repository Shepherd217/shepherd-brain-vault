"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Activity, Clock, CheckCircle, AlertCircle, RotateCcw } from "lucide-react";

interface AgentPresence {
  id: string;
  name: string;
  emoji: string;
  status: "idle" | "working" | "stalled" | "error" | "offline";
  currentTask: string | null;
  lastSeen: string;
  gatewayType: string;
}

export function AgentPresencePanel() {
  const [agents, setAgents] = useState<AgentPresence[]>([]);
  const [reclaimed, setReclaimed] = useState<{ id: string; title: string }[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAgents = useCallback(async () => {
    try {
      const res = await fetch("/api/agents/status?reclaim=true");
      const data = await res.json();
      if (data.agents) {
        setAgents(
          data.agents.map((a: any) => ({
            ...a,
            emoji: a.gatewayType === "openclaw" ? "🟡" : a.gatewayType === "hermes" ? "🟢" : "🔵",
            lastSeen: a.updatedAt,
          }))
        );
      }
      if (data.reclaimed) {
        setReclaimed(data.reclaimed);
      }
    } catch (_) {
      // silent fail
    } finally {
      setLoading(false);
    }
  }, []);

  const handleReclaim = async () => {
    try {
      const res = await fetch("/api/agents/reclaim", { method: "POST" });
      const data = await res.json();
      if (data.reclaimed) {
        setReclaimed(data.reclaimed);
      }
      fetchAgents();
    } catch (_) {}
  };

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 30000);
    return () => clearInterval(interval);
  }, [fetchAgents]);

  const statusConfig = {
    idle: { icon: Clock, color: "text-green-500", bg: "bg-green-50", label: "Idle" },
    working: { icon: Activity, color: "text-yellow-500", bg: "bg-yellow-50", label: "Working" },
    stalled: { icon: AlertCircle, color: "text-orange-500", bg: "bg-orange-50", label: "Stalled" },
    error: { icon: AlertCircle, color: "text-red-500", bg: "bg-red-50", label: "Error" },
    offline: { icon: AlertCircle, color: "text-gray-400", bg: "bg-gray-50", label: "Offline" },
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">Agents</h3>
        <button
          onClick={handleReclaim}
          className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800"
          title="Reclaim tasks from zombie agents"
        >
          <RotateCcw className="h-3 w-3" />
          Reclaim
        </button>
      </div>

      {reclaimed.length > 0 && (
        <div className="text-xs bg-blue-50 text-blue-700 p-2 rounded">
          Reclaimed {reclaimed.length} task(s) from zombies
        </div>
      )}

      <Card>
        <CardContent className="p-3">
          {loading && agents.length === 0 ? (
            <div className="text-xs text-muted-foreground">Loading agents...</div>
          ) : agents.length === 0 ? (
            <div className="text-xs text-muted-foreground">No agents connected</div>
          ) : (
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
                        <span className="text-sm font-medium">
                          {agent.emoji} {agent.name}
                        </span>
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
          )}
        </CardContent>
      </Card>
    </div>
  );
}
