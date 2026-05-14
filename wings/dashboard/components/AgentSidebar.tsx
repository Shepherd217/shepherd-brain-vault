"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity, Cpu, Globe, User } from "lucide-react";
import type { Agent, AgentStatus } from "@/types";

const MOCK_AGENTS: Agent[] = [
  {
    id: "ava",
    name: "Ava",
    agentType: "openclaw",
    gatewayId: "default",
    gatewayType: "openclaw",
    gatewayUrl: "ws://localhost:18789",
    status: "working",
    currentTask: "2026-05-14-003",
    models: ["kimi/k2p6"],
    skills: ["research", "architecture", "coding"],
    surfaces: ["telegram"],
    createdAt: new Date("2026-05-12"),
    updatedAt: new Date(),
  },
  {
    id: "hermes",
    name: "Hermes",
    agentType: "hermes",
    gatewayId: "default",
    gatewayType: "hermes",
    gatewayUrl: "http://localhost:9119",
    status: "idle",
    currentTask: null,
    models: ["minimax2.7"],
    skills: ["infrastructure", "deployment", "devops"],
    surfaces: ["cli", "dashboard"],
    createdAt: new Date("2026-05-12"),
    updatedAt: new Date(),
  },
  {
    id: "eve",
    name: "Eve",
    agentType: "openclaw",
    gatewayId: "default",
    gatewayType: "openclaw",
    gatewayUrl: "ws://localhost:18789",
    status: "offline",
    currentTask: null,
    models: ["nemotron"],
    skills: ["memory", "audit", "knowledge"],
    surfaces: ["telegram"],
    createdAt: new Date("2026-05-13"),
    updatedAt: new Date(),
  },
];

const STATUS_COLORS: Record<AgentStatus, string> = {
  idle: "bg-green-500",
  working: "bg-amber-500",
  stalled: "bg-red-500",
  error: "bg-red-600",
  offline: "bg-gray-400",
};

const STATUS_LABELS: Record<AgentStatus, string> = {
  idle: "Idle",
  working: "Working",
  stalled: "Stalled",
  error: "Error",
  offline: "Offline",
};

export function AgentSidebar() {
  const [agents] = useState<Agent[]>(MOCK_AGENTS);
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-64 border-l bg-card flex flex-col">
      <div className="border-b p-4">
        <div className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">Team Status</h2>
        </div>
        <p className="mt-1 text-xs text-muted-foreground">
          {time.toLocaleTimeString()} · {agents.filter(a => a.status !== "offline").length} online
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {agents.map((agent) => (
          <Card key={agent.id} className="overflow-hidden">
            <CardHeader className="p-3 pb-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className={`h-2.5 w-2.5 rounded-full ${STATUS_COLORS[agent.status]}`} />
                  <span className="text-sm font-medium">{agent.name}</span>
                </div>
                <Badge variant="outline" className="text-xs">
                  {agent.agentType}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="p-3 pt-0 space-y-2">
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <User className="h-3.5 w-3.5" />
                <span>{STATUS_LABELS[agent.status]}</span>
              </div>
              {agent.currentTask && (
                <div className="flex items-center gap-2 text-xs">
                  <Cpu className="h-3.5 w-3.5 text-primary" />
                  <span className="truncate text-muted-foreground">
                    Task: {agent.currentTask}
                  </span>
                </div>
              )}
              <div className="flex flex-wrap gap-1 pt-1">
                {agent.models.map((model) => (
                  <Badge key={model} variant="secondary" className="text-[10px]">
                    <Globe className="mr-1 h-2.5 w-2.5" />
                    {model.split("/").pop()}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="border-t p-3">
        <p className="text-xs text-muted-foreground text-center">
          Shepherd Team v0.1.0
        </p>
      </div>
    </div>
  );
}
