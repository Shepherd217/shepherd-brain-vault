"use client";

import { Draggable } from "react-beautiful-dnd";
import type { Task } from "@/types";

interface TaskCardProps {
  task: Task;
  index: number;
}

export function TaskCard({ task, index }: TaskCardProps) {
  const priorityColors: Record<string, string> = {
    low: "bg-blue-100 text-blue-800",
    medium: "bg-yellow-100 text-yellow-800",
    high: "bg-orange-100 text-orange-800",
    critical: "bg-red-100 text-red-800",
  };

  const tags = task.tags || [];

  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={`mb-2 md:mb-3 rounded-lg border bg-popover p-3 md:p-3 shadow-sm transition-shadow active:scale-[0.98] ${
            snapshot.isDragging ? "shadow-lg ring-2 ring-primary" : "hover:shadow-md"
          }`}
        >
          <div className="mb-2 flex items-start justify-between gap-2">
            <h3 className="text-sm md:text-sm font-medium leading-snug">{task.title}</h3>
            <span
              className={`rounded-full px-2 py-0.5 text-[10px] md:text-xs flex-shrink-0 ${
                priorityColors[task.priority] || "bg-gray-100"
              }`}
            >
              {task.priority}
            </span>
          </div>

          {task.description && (
            <p className="mb-2 text-xs text-muted-foreground line-clamp-2 leading-relaxed">
              {task.description}
            </p>
          )}

          <div className="flex flex-wrap gap-1">
            {tags.map((tag: string) => (
              <span
                key={tag}
                className="rounded bg-muted px-1.5 py-0.5 text-[10px] md:text-xs text-muted-foreground"
              >
                {tag}
              </span>
            ))}
          </div>

          {task.owner && (
            <div className="mt-2 flex items-center gap-1 text-[10px] md:text-xs text-muted-foreground">
              <span className="rounded-full bg-primary/10 px-2 py-0.5">
                @{task.owner}
              </span>
              {task.agentType && (
                <span className="text-[10px] md:text-xs">({task.agentType})</span>
              )}
            </div>
          )}
        </div>
      )}
    </Draggable>
  );
}
