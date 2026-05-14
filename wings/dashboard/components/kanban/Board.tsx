"use client";

import { useState, useEffect } from "react";
import { DragDropContext } from "react-beautiful-dnd";
import type { DropResult } from "react-beautiful-dnd";
import { Column } from "./Column";
import { MobileColumnView } from "./MobileColumnView";
import { CreateTaskModal } from "../CreateTaskModal";
import { Button } from "@/components/ui/button";
import { RefreshCw, LayoutDashboard } from "lucide-react";
import { usePersistentTasks } from "@/lib/usePersistentTasks";
import type { Task, TaskStatus } from "@/types";

const COLUMNS: TaskStatus[] = ["backlog", "todo", "doing", "review", "done", "failed"];

const COLUMN_STYLES: Record<TaskStatus, { title: string; color: string }> = {
  backlog: { title: "📋 Backlog", color: "bg-slate-800 border-slate-700" },
  todo: { title: "🎯 Todo", color: "bg-blue-950 border-blue-800" },
  doing: { title: "⚡ Doing", color: "bg-amber-950 border-amber-800" },
  review: { title: "👀 Review", color: "bg-purple-950 border-purple-800" },
  done: { title: "✅ Done", color: "bg-green-950 border-green-800" },
  failed: { title: "❌ Failed", color: "bg-red-950 border-red-800" },
};

interface KanbanBoardProps {
  onToggleSidebar?: () => void;
}

export function KanbanBoard({ onToggleSidebar }: KanbanBoardProps) {
  const { tasks, loaded, addTask, updateTask, refresh } = usePersistentTasks();
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  useEffect(() => {
    if (loaded) {
      setLastUpdate(new Date());
    }
  }, [loaded, tasks]);

  async function handleDragEnd(result: DropResult) {
    if (!result.destination) return;
    const taskId = result.draggableId;
    const newStatus = result.destination.droppableId as TaskStatus;
    await updateTask(taskId, { status: newStatus });
  }

  function handleTaskCreated(taskData: Partial<Task>) {
    addTask(taskData);
  }

  const stats = {
    total: tasks.length,
    doing: tasks.filter((t) => t.status === "doing").length,
    done: tasks.filter((t) => t.status === "done").length,
  };

  if (!loaded) {
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
    <div className="flex flex-col h-full bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2 min-w-0">
            <LayoutDashboard className="h-5 w-5 text-primary flex-shrink-0" />
            <div className="min-w-0">
              <h1 className="text-base font-bold truncate">Shepherd Team</h1>
              <p className="text-[10px] text-muted-foreground">
                {stats.total} tasks · {stats.doing} active · {stats.done} done
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <span className="text-[10px] text-muted-foreground hidden sm:inline">
              Updated {lastUpdate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            </span>
            <Button variant="outline" size="sm" onClick={refresh} className="gap-1 h-8">
              <RefreshCw className="h-3.5 w-3.5" />
            </Button>
            <div className="hidden md:block">
              <CreateTaskModal onTaskCreated={handleTaskCreated} />
            </div>
          </div>
        </div>
      </header>

      {/* Board */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="flex-1 overflow-hidden">
          {isMobile ? (
            <MobileColumnView tasks={tasks} />
          ) : (
            <div className="flex h-full gap-3 p-3 overflow-x-auto min-w-max">
              {COLUMNS.map((column) => (
                <div key={column} className="w-[280px] flex-shrink-0">
                  <Column
                    title={COLUMN_STYLES[column].title}
                    color={COLUMN_STYLES[column].color}
                    tasks={tasks.filter((t) => t.status === column)}
                    droppableId={column}
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      </DragDropContext>
    </div>
  );
}
