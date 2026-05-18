"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, GitCommit, MessageSquare, Rocket, CheckCircle, Clock } from "lucide-react";

interface ActivityItem {
  id: string;
  agent: string;
  type: string;
  content: string;
  timestamp: string;
}

const typeIcons: Record<string, any> = {
  goal_set: Activity,
  goal_complete: CheckCircle,
  task_created: GitCommit,
  task_moved: GitCommit,
  deploy: Rocket,
  message: MessageSquare,
  update: Clock,
};

const typeColors: Record<string, string> = {
  goal_set: "text-blue-500",
  goal_complete: "text-green-500",
  task_created: "text-purple-500",
  task_moved: "text-yellow-500",
  deploy: "text-orange-500",
  message: "text-cyan-500",
  update: "text-gray-500",
};

export function ActivityFeed() {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchActivities();
    const interval = setInterval(fetchActivities, 3000);
    return () => clearInterval(interval);
  }, []);

  async function fetchActivities() {
    try {
      const res = await fetch("/api/activity?limit=20");
      const data = await res.json();
      setActivities(data.activities || []);
    } catch (error) {
      console.error("Failed to fetch activities:", error);
    } finally {
      setLoading(false);
    }
  }

  function formatTime(timestamp: string) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diff < 60) return "Just now";
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  }

  const agentEmojis: Record<string, string> = {
    ava: "🟡",
    hermes: "🟢",
    eve: "🔵",
    nathan: "👤",
  };

  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold flex items-center gap-2">
          <Activity className="h-4 w-4 text-primary" />
          Live Activity Feed
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <div
          ref={scrollRef}
          className="space-y-2 max-h-[400px] overflow-y-auto pr-1"
        >
          {loading ? (
            <div className="text-sm text-muted-foreground text-center py-4">
              Loading activity...
            </div>
          ) : activities.length === 0 ? (
            <div className="text-sm text-muted-foreground text-center py-4">
              No activity yet. Agents will appear here when they work.
            </div>
          ) : (
            activities.map((activity) => {
              const Icon = typeIcons[activity.type] || Clock;
              const color = typeColors[activity.type] || "text-gray-500";
              const emoji = agentEmojis[activity.agent] || "⚪";

              return (
                <div
                  key={activity.id}
                  className="flex items-start gap-2 p-2 rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <Icon className={`h-3.5 w-3.5 mt-0.5 flex-shrink-0 ${color}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs leading-relaxed">
                      <span className="font-medium">{emoji} {activity.agent}</span>{" "}
                      {activity.content}
                    </p>
                    <p className="text-[10px] text-muted-foreground mt-0.5">
                      {formatTime(activity.timestamp)}
                    </p>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </CardContent>
    </Card>
  );
}
