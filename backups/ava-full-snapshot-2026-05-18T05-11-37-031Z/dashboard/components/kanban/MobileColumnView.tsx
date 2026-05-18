"use client";

import { useState } from "react";
import { Droppable } from "react-beautiful-dnd";
import { TaskCard } from "./TaskCard";
import { QuickAddCard } from "./QuickAddCard";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Task, TaskStatus } from "@/types";

const COLUMNS: TaskStatus[] = ["backlog", "todo", "doing", "review", "done", "failed"];

const COLUMN_CONFIG: Record<TaskStatus, { title: string; emoji: string; color: string }> = {
  backlog: { title: "Backlog", emoji: "📋", color: "bg-slate-800 border-slate-700" },
  todo: { title: "Todo", emoji: "🎯", color: "bg-blue-950 border-blue-800" },
  doing: { title: "Doing", emoji: "⚡", color: "bg-amber-950 border-amber-800" },
  review: { title: "Review", emoji: "👀", color: "bg-purple-950 border-purple-800" },
  done: { title: "Done", emoji: "✅", color: "bg-green-950 border-green-800" },
  failed: { title: "Failed", emoji: "❌", color: "bg-red-950 border-red-800" },
};

interface MobileColumnViewProps {
  tasks: Task[];
  onColumnChange?: (column: TaskStatus) => void;
  onTaskClick?: (task: Task) => void;
  onQuickAdd?: (column: string, title: string) => void;
}

export function MobileColumnView({ tasks, onColumnChange, onTaskClick, onQuickAdd }: MobileColumnViewProps) {
  const [activeColumn, setActiveColumn] = useState(0);
  const column = COLUMNS[activeColumn];
  const config = COLUMN_CONFIG[column];
  const columnTasks = tasks.filter((t) => t.status === column);

  function goToPrev() {
    if (activeColumn > 0) {
      const newIndex = activeColumn - 1;
      setActiveColumn(newIndex);
      onColumnChange?.(COLUMNS[newIndex]);
    }
  }

  function goToNext() {
    if (activeColumn < COLUMNS.length - 1) {
      const newIndex = activeColumn + 1;
      setActiveColumn(newIndex);
      onColumnChange?.(COLUMNS[newIndex]);
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Column selector */}
      <div className="flex items-center gap-1 px-3 py-2 border-b border-border bg-card/50">
        <Button
          variant="ghost"
          size="sm"
          className="h-7 w-7 p-0 flex-shrink-0"
          onClick={goToPrev}
          disabled={activeColumn === 0}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        
        <div className="flex-1 flex items-center justify-center gap-1 overflow-x-auto">
          {COLUMNS.map((col, i) => {
            const isActive = i === activeColumn;
            const count = tasks.filter((t) => t.status === col).length;
            return (
              <button
                key={col}
                onClick={() => {
                  setActiveColumn(i);
                  onColumnChange?.(col);
                }}
                className={`flex-shrink-0 px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                {COLUMN_CONFIG[col].emoji} {COLUMN_CONFIG[col].title}
                <span className="ml-1 opacity-70">{count}</span>
              </button>
            );
          })}
        </div>
        
        <Button
          variant="ghost"
          size="sm"
          className="h-7 w-7 p-0 flex-shrink-0"
          onClick={goToNext}
          disabled={activeColumn === COLUMNS.length - 1}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>

      {/* Single column */}
      <div className="flex-1 overflow-y-auto p-3">
        <Droppable droppableId={column}>
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className={`min-h-full rounded-xl border-2 p-3 transition-colors ${
                snapshot.isDraggingOver
                  ? "border-primary bg-accent/30"
                  : config.color
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold">
                  {config.emoji} {config.title}
                </h2>
                <span className="rounded-full bg-background px-2 py-0.5 text-xs font-medium">
                  {columnTasks.length}
                </span>
              </div>
              <div className="space-y-2">
                {columnTasks.map((task, index) => (
                  <TaskCard key={task.id} task={task} index={index} onClick={onTaskClick} />
                ))}
              </div>
              {provided.placeholder}
              <div className="mt-2 pt-2 border-t border-border/30">
                <QuickAddCard columnId={column} onAdd={(title) => onQuickAdd?.(column, title)} />
              </div>
            </div>
          )}
        </Droppable>
      </div>
    </div>
  );
}
