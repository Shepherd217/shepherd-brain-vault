"use client";

import { Droppable } from "react-beautiful-dnd";
import { TaskCard } from "./TaskCard";
import { QuickAddCard } from "./QuickAddCard";
import { EmptyState } from "./EmptyState";
import type { Task, TaskStatus } from "@/types";

interface ColumnProps {
  title: string;
  color: string;
  tasks: Task[];
  droppableId: TaskStatus;
  onTaskClick?: (task: Task) => void;
  onQuickAdd?: (title: string) => void;
}

export function Column({ title, color, tasks, droppableId, onTaskClick, onQuickAdd }: ColumnProps) {
  return (
    <Droppable droppableId={droppableId}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          className={`flex flex-col h-full rounded-xl border-2 p-3 transition-colors ${
            snapshot.isDraggingOver
              ? "border-primary bg-accent/30"
              : color
          }`}
        >
          <div className="flex items-center justify-between mb-3 flex-shrink-0">
            <h2 className="text-sm font-semibold">{title}</h2>
            <span className="rounded-full bg-background px-2 py-0.5 text-xs font-medium shadow-sm">
              {tasks.length}
            </span>
          </div>
          <div className="flex-1 overflow-y-auto min-h-0 space-y-2">
            {tasks.map((task, index) => (
              <TaskCard key={task.id} task={task} index={index} onClick={onTaskClick} />
            ))}
          </div>
          {provided.placeholder}
          <div className="mt-2 pt-2 border-t border-border/30">
            <QuickAddCard columnId={droppableId} onAdd={onQuickAdd || (() => {})} />
          </div>
        </div>
      )}
    </Droppable>
  );
}
