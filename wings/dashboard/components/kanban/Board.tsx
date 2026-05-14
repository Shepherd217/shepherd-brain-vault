"use client";

import { useState, useEffect, useRef } from "react";
import { DragDropContext, Droppable } from "react-beautiful-dnd";
import type { DropResult } from "react-beautiful-dnd";
import { Column } from "./Column";
import { CreateTaskModal } from "../CreateTaskModal";
import { Button } from "@/components/ui/button";
import { RefreshCw, LayoutDashboard, Users, ChevronLeft, ChevronRight } from "lucide-react";
import type { Task, TaskStatus } from "@/types";

const COLUMNS: TaskStatus[] = ["backlog", "todo", "doing", "review", "done", "failed"];

const COLUMN_STYLES: Record<TaskStatus, { title: string; color: string; short: string }> = {
  backlog: { title: "📋 Backlog", color: "bg-slate-100 border-slate-200", short: "Backlog" },
  todo: { title: "🎯 Todo", color: "bg-blue-50 border-blue-200", short: "Todo" },
  doing: { title: "⚡ Doing", color: "bg-amber-50 border-amber-200", short: "Doing" },
  review: { title: "👀 Review", color: "bg-purple-50 border-purple-200", short: "Review" },
  done: { title: "✅ Done", color: "bg-green-50 border-green-200", short: "Done" },
  failed: { title: "❌ Failed", color: "bg-red-50 border-red-200", short: "Failed" },
};

interface KanbanBoardProps {
  onToggleSidebar?: () => void;
  sidebarOpen?: boolean;
}

export function KanbanBoard({ onToggleSidebar }: KanbanBoardProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [isMobile, setIsMobile] = useState(false);
  const [activeColumn, setActiveColumn] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

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

  function scrollToColumn(index: number) {
    if (scrollRef.current && isMobile) {
      const children = scrollRef.current.children;
      if (children[index]) {
        children[index].scrollIntoView({ behavior: "smooth", inline: "start", block: "nearest" });
        setActiveColumn(index);
      }
    }
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
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card px-4 py-3 md:px-6 md:py-4 flex-shrink-0">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2 md:gap-3 min-w-0">
            <LayoutDashboard className="h-5 w-5 md:h-6 md:w-6 text-primary flex-shrink-0" />
            <div className="min-w-0">
              <h1 className="text-base md:text-xl font-bold truncate">Shepherd Team</h1>
              <p className="text-[10px] md:text-xs text-muted-foreground hidden sm:block">
                {stats.total} tasks · {stats.doing} in progress · {stats.done} completed
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <span className="text-[10px] md:text-xs text-muted-foreground hidden md:inline">
              Updated {lastUpdate.toLocaleTimeString()}
            </span>
            <Button variant="outline" size="sm" onClick={fetchTasks} className="gap-1 md:gap-2 h-9 md:h-10">
              <RefreshCw className="h-3.5 w-3.5 md:h-4 md:w-4" />
              <span className="hidden sm:inline">Refresh</span>
            </Button>
            <div className="hidden md:block">
              <CreateTaskModal onTaskCreated={handleTaskCreated} />
            </div>
            {onToggleSidebar && (
              <Button variant="outline" size="sm" onClick={onToggleSidebar} className="md:hidden h-9 w-9 p-0">
                <Users className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>

        {/* Mobile column tabs */}
        {isMobile && (
          <div className="flex items-center gap-1 mt-2 overflow-x-auto pb-1 -mx-1 px-1">
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0 flex-shrink-0"
              onClick={() => scrollToColumn(Math.max(0, activeColumn - 1))}
              disabled={activeColumn === 0}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            {COLUMNS.map((col, i) => (
              <button
                key={col}
                onClick={() => scrollToColumn(i)}
                className={`flex-shrink-0 px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                  i === activeColumn
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                {COLUMN_STYLES[col].short}
                <span className="ml-1 opacity-70">{tasks.filter((t) => t.status === col).length}</span>
              </button>
            ))}
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0 flex-shrink-0"
              onClick={() => scrollToColumn(Math.min(COLUMNS.length - 1, activeColumn + 1))}
              disabled={activeColumn === COLUMNS.length - 1}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </header>

      {/* Board */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="flex-1 overflow-hidden">
          <div
            ref={scrollRef}
            className={`
              flex h-full gap-3 md:gap-4 p-3 md:p-4
              ${isMobile
                ? "overflow-x-auto snap-x snap-mandatory scroll-smooth"
                : "overflow-x-auto min-w-max"
              }
            `}
          >
            {COLUMNS.map((column, index) => (
              <div
                key={column}
                className={`
                  flex flex-col
                  ${isMobile ? "w-[85vw] snap-start flex-shrink-0" : "w-[300px] flex-shrink-0"}
                  md:w-[300px]
                `}
              >
                <Droppable droppableId={column}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      className={`flex flex-1 flex-col rounded-xl border-2 p-2 md:p-3 transition-colors min-h-0 ${
                        snapshot.isDraggingOver
                          ? "border-primary bg-accent/30"
                          : COLUMN_STYLES[column].color
                      }`}
                    >
                      <div className="mb-2 md:mb-3 flex items-center justify-between flex-shrink-0">
                        <h2 className="text-xs md:text-sm font-semibold">
                          {COLUMN_STYLES[column].title}
                        </h2>
                        <span className="rounded-full bg-background px-2 py-0.5 text-[10px] md:text-xs font-medium shadow-sm">
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

      {/* Mobile floating action buttons */}
      {isMobile && (
        <div className="fixed bottom-4 left-4 z-30">
          <CreateTaskModal onTaskCreated={handleTaskCreated} />
        </div>
      )}
    </div>
  );
}
