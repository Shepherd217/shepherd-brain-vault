"use client";

import { useState, useEffect } from "react";
import { DragDropContext } from "react-beautiful-dnd";
import type { DropResult } from "react-beautiful-dnd";
import { Column } from "./Column";
import { MobileColumnView } from "./MobileColumnView";
import { TaskDetailPanel } from "../TaskDetailPanel";
import { CommandPalette } from "../CommandPalette";
import { Button } from "@/components/ui/button";
import { RefreshCw, LayoutDashboard, Command as CmdIcon } from "lucide-react";
import { usePersistentTasks } from "@/lib/usePersistentTasks";
import type { Task, TaskStatus } from "@/types";

const COLUMNS: TaskStatus[] = ["backlog", "todo", "doing", "review", "done", "failed"];

const COLUMN_STYLES: Record<TaskStatus, { title: string; color: string }> = {
  backlog: { title: "📋 Backlog", color: "bg-slate-900/50 border-slate-800" },
  todo: { title: "🎯 Todo", color: "bg-blue-950/30 border-blue-900" },
  doing: { title: "⚡ Doing", color: "bg-amber-950/30 border-amber-900" },
  review: { title: "👀 Review", color: "bg-purple-950/30 border-purple-900" },
  done: { title: "✅ Done", color: "bg-green-950/30 border-green-900" },
  failed: { title: "❌ Failed", color: "bg-red-950/30 border-red-900" },
};

export function KanbanBoard() {
  const { tasks, loaded, addTask, updateTask, removeTask, refresh } = usePersistentTasks();
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [isMobile, setIsMobile] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [commandOpen, setCommandOpen] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  // Cmd+K shortcut
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandOpen((prev) => !prev);
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
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

  function handleQuickAdd(columnId: string, title: string) {
    addTask({
      title,
      status: columnId as TaskStatus,
      priority: "medium",
    });
  }

  function handleTaskClick(task: Task) {
    setSelectedTask(task);
  }

  function handleTaskUpdate(id: string, updates: Partial<Task>) {
    updateTask(id, updates);
    // Update selected task if it's the one being edited
    if (selectedTask?.id === id) {
      setSelectedTask((prev) => (prev ? { ...prev, ...updates } : null));
    }
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
    <>
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
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCommandOpen(true)}
                className="hidden md:flex gap-1.5 h-8 text-xs text-muted-foreground hover:text-foreground"
              >
                <CmdIcon className="h-3.5 w-3.5" />
                <span>Cmd+K</span>
              </Button>
              <span className="text-[10px] text-muted-foreground hidden sm:inline">
                Updated {lastUpdate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </span>
              <Button variant="outline" size="sm" onClick={refresh} className="gap-1 h-8">
                <RefreshCw className="h-3.5 w-3.5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Board */}
        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="flex-1 overflow-hidden">
            {isMobile ? (
              <MobileColumnView tasks={tasks} onTaskClick={handleTaskClick} onQuickAdd={handleQuickAdd} />
            ) : (
              <div className="flex h-full gap-3 p-3 overflow-x-auto min-w-max">
                {COLUMNS.map((column) => (
                  <div key={column} className="w-[300px] flex-shrink-0">
                    <Column
                      title={COLUMN_STYLES[column].title}
                      color={COLUMN_STYLES[column].color}
                      tasks={tasks.filter((t) => t.status === column)}
                      droppableId={column}
                      onTaskClick={handleTaskClick}
                      onQuickAdd={(title) => handleQuickAdd(column, title)}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        </DragDropContext>
      </div>

      {/* Task Detail Panel */}
      <TaskDetailPanel
        task={selectedTask}
        onClose={() => setSelectedTask(null)}
        onUpdate={handleTaskUpdate}
        onDelete={(id) => {
          removeTask(id);
          setSelectedTask(null);
        }}
      />

      {/* Command Palette */}
      <CommandPalette
        tasks={tasks}
        isOpen={commandOpen}
        onClose={() => setCommandOpen(false)}
        onSelectTask={handleTaskClick}
        onCreateTask={(title) => addTask({ title, status: "backlog", priority: "medium" })}
      />
    </>
  );
}
