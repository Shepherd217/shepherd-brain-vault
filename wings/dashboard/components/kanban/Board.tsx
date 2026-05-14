"use client";

import { useState, useEffect } from "react";
import { DragDropContext, Droppable } from "react-beautiful-dnd";
import type { DropResult } from "react-beautiful-dnd";
import { Column } from "./Column";
import type { Task, TaskStatus } from "@/types";

const COLUMNS: TaskStatus[] = ["backlog", "todo", "doing", "review", "done", "failed"];

const COLUMN_TITLES: Record<TaskStatus, string> = {
  backlog: "📋 Backlog",
  todo: "🎯 Todo",
  doing: "⚡ Doing",
  review: "👀 Review",
  done: "✅ Done",
  failed: "❌ Failed",
};

export function KanbanBoard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  async function fetchTasks() {
    try {
      const res = await fetch("/api/tasks");
      const data = await res.json();
      setTasks(data.tasks || []);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    } finally {
      setLoading(false);
    }
  }

  async function handleDragEnd(result: DropResult) {
    if (!result.destination) return;

    const taskId = result.draggableId;
    const newStatus = result.destination.droppableId as TaskStatus;

    // Optimistic update
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t))
    );

    try {
      const res = await fetch(`/api/tasks/${taskId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!res.ok) {
        // Revert on error
        fetchTasks();
      }
    } catch {
      fetchTasks();
    }
  }

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-lg text-muted-foreground">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-background p-4">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Shepherd Team Dashboard</h1>
        <button
          onClick={() => {
            /* TODO: Create task modal */
          }}
          className="rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/90"
        >
          + New Task
        </button>
      </div>

      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="flex h-[calc(100vh-100px)] gap-4 overflow-x-auto">
          {COLUMNS.map((column) => (
            <div key={column} className="flex min-w-[280px] flex-1 flex-col">
              <Droppable droppableId={column}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className={`flex flex-1 flex-col rounded-lg border bg-card p-3 ${
                      snapshot.isDraggingOver ? "border-primary bg-accent/50" : ""
                    }`}
                  >
                    <h2 className="mb-3 text-sm font-semibold text-muted-foreground">
                      {COLUMN_TITLES[column]}
                      <span className="ml-2 rounded-full bg-muted px-2 py-0.5 text-xs">
                        {tasks.filter((t) => t.status === column).length}
                      </span>
                    </h2>
                    <Column
                      tasks={tasks.filter((t) => t.status === column)}
                    />
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </div>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
}
