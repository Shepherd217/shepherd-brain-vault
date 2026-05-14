"use client";

import { useState, useEffect } from "react";
import { DragDropContext, Droppable } from "react-beautiful-dnd";
import type { DropResult } from "react-beautiful-dnd";
import { Column } from "./Column";
import { CreateTaskModal } from "../CreateTaskModal";
import { Button } from "@/components/ui/button";
import { RefreshCw, LayoutDashboard } from "lucide-react";
import type { Task, TaskStatus } from "@/types";

const COLUMNS: TaskStatus[] = ["backlog", "todo", "doing", "review", "done", "failed"];

const COLUMN_STYLES: Record<TaskStatus, { title: string; color: string }> = {
  backlog: { title: "📋 Backlog", color: "bg-slate-100 border-slate-200" },
  todo: { title: "🎯 Todo", color: "bg-blue-50 border-blue-200" },
  doing: { title: "⚡ Doing", color: "bg-amber-50 border-amber-200" },
  review: { title: "👀 Review", color: "bg-purple-50 border-purple-200" },
  done: { title: "✅ Done", color: "bg-green-50 border-green-200" },
  failed: { title: "❌ Failed", color: "bg-red-50 border-red-200" },
};

export function KanbanBoard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000);
    return () => clearInterval(interval);
  }, []);

  async function fetchTasks() {
    try {
      const res = await fetch("/api/tasks");
      const data = await res.json();
      setTasks(data.tasks || []);
      setLastUpdate(new Date());
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

    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t))
    );

    try {
      const res = await fetch(`/api/tasks/${taskId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!res.ok) fetchTasks();
    } catch {
      fetchTasks();
    }
  }

  function handleTaskCreated(newTask: Task) {
    setTasks((prev) => [...prev, newTask]);
  }

  const stats = {
    total: tasks.length,
    doing: tasks.filter((t) => t.status === "doing").length,
    done: tasks.filter((t) => t.status === "done").length,
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-3">
          <RefreshCw className="h-8 w-8 animate-spin text-primary" />
          <p className="text-lg text-muted-foreground">Loading Shepherd Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b bg-card px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <LayoutDashboard className="h-6 w-6 text-primary" />
            <div>
              <h1 className="text-xl font-bold">Shepherd Team Dashboard</h1>
              <p className="text-xs text-muted-foreground">
                {stats.total} tasks · {stats.doing} in progress · {stats.done} completed
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-muted-foreground">
              Updated {lastUpdate.toLocaleTimeString()}
            </span>
            <Button variant="outline" size="sm" onClick={fetchTasks} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
            <CreateTaskModal onTaskCreated={handleTaskCreated} />
          </div>
        </div>
      </header>

      {/* Board */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="flex-1 overflow-x-auto p-4">
          <div className="flex h-full gap-4 min-w-max">
            {COLUMNS.map((column) => (
              <div key={column} className="flex w-[300px] flex-col">
                <Droppable droppableId={column}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      className={`flex flex-1 flex-col rounded-xl border-2 p-3 transition-colors ${
                        snapshot.isDraggingOver
                          ? "border-primary bg-accent/30"
                          : COLUMN_STYLES[column].color
                      }`}
                    >
                      <div className="mb-3 flex items-center justify-between">
                        <h2 className="text-sm font-semibold">
                          {COLUMN_STYLES[column].title}
                        </h2>
                        <span className="rounded-full bg-background px-2.5 py-0.5 text-xs font-medium shadow-sm">
                          {tasks.filter((t) => t.status === column).length}
                        </span>
                      </div>
                      <Column tasks={tasks.filter((t) => t.status === column)} />
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            ))}
          </div>
        </div>
      </DragDropContext>
    </div>
  );
}
