"use client";

import { useState } from "react";
import { Draggable } from "react-beautiful-dnd";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Task, Priority } from "@/types";
import { MessageSquare, Calendar, AlertCircle } from "lucide-react";

const PRIORITY_CONFIG: Record<Priority, { color: string; label: string; bar: string }> = {
  low: { color: "text-slate-400", label: "Low", bar: "bg-slate-500" },
  medium: { color: "text-blue-400", label: "Medium", bar: "bg-blue-500" },
  high: { color: "text-amber-400", label: "High", bar: "bg-amber-500" },
  critical: { color: "text-red-400", label: "Critical", bar: "bg-red-500" },
};

interface TaskCardProps {
  task: Task;
  index: number;
  onClick?: (task: Task) => void;
}

export function TaskCard({ task, index, onClick }: TaskCardProps) {
  const priority = PRIORITY_CONFIG[task.priority];
  const [isHovered, setIsHovered] = useState(false);

  // Generate task ID like SHE-001
  const shortId = task.id.slice(0, 8).toUpperCase();

  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          onClick={() => onClick?.(task)}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          className={cn(
            "group relative rounded-lg border bg-card p-3 cursor-pointer transition-all duration-200",
            "hover:border-primary/50 hover:shadow-md",
            snapshot.isDragging && "shadow-xl ring-2 ring-primary/30 rotate-1 scale-[1.02]",
            !snapshot.isDragging && "border-border/60"
          )}
          style={{
            ...provided.draggableProps.style,
          }}
        >
          {/* Priority indicator bar on left */}
          <div className={cn("absolute left-0 top-2 bottom-2 w-[3px] rounded-full", priority.bar)} />

          <div className="pl-2">
            {/* Top row: ID + Priority */}
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">
                {shortId}
              </span>
              <span className={cn("text-[10px] font-medium uppercase tracking-wider", priority.color)}>
                {priority.label}
              </span>
            </div>

            {/* Title */}
            <h3 className="text-sm font-medium text-foreground leading-snug mb-2 line-clamp-2">
              {task.title}
            </h3>

            {/* Tags */}
            {task.tags.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {task.tags.slice(0, 3).map((tag) => (
                  <Badge
                    key={tag}
                    variant="secondary"
                    className="text-[10px] px-1.5 py-0 h-4 bg-secondary/50 text-muted-foreground border-0"
                  >
                    {tag}
                  </Badge>
                ))}
                {task.tags.length > 3 && (
                  <Badge
                    variant="secondary"
                    className="text-[10px] px-1.5 py-0 h-4 bg-secondary/50 text-muted-foreground border-0"
                  >
                    +{task.tags.length - 3}
                  </Badge>
                )}
              </div>
            )}

            {/* Bottom row: Owner + metadata */}
            <div className="flex items-center justify-between pt-1 border-t border-border/40">
              <div className="flex items-center gap-1.5">
                {task.owner ? (
                  <div className="flex items-center gap-1">
                    <div className="h-4 w-4 rounded-full bg-primary/20 flex items-center justify-center">
                      <span className="text-[8px] font-bold text-primary">
                        {task.owner.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span className="text-[11px] text-muted-foreground">{task.owner}</span>
                  </div>
                ) : (
                  <span className="text-[11px] text-muted-foreground/50">Unassigned</span>
                )}
              </div>

              <div className="flex items-center gap-2 text-muted-foreground/50">
                {task.description && (
                  <MessageSquare className="h-3 w-3" />
                )}
                <Calendar className="h-3 w-3" />
                <span className="text-[10px]">
                  {new Date(task.createdAt).toLocaleDateString(undefined, { month: "short", day: "numeric" })}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </Draggable>
  );
}
