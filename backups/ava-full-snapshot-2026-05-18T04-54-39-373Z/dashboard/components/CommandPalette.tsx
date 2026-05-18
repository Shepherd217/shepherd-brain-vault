"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Task } from "@/types";
import { Search, Command, ArrowRight, Hash, User, Tag, AlertCircle } from "lucide-react";

interface CommandPaletteProps {
  tasks: Task[];
  isOpen: boolean;
  onClose: () => void;
  onSelectTask: (task: Task) => void;
  onCreateTask: (title: string) => void;
}

export function CommandPalette({ tasks, isOpen, onClose, onSelectTask, onCreateTask }: CommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  // Reset when opening
  useEffect(() => {
    if (isOpen) {
      setQuery("");
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  // Build results
  const results = query.trim()
    ? tasks.filter((t) =>
        t.title.toLowerCase().includes(query.toLowerCase()) ||
        t.id.toLowerCase().includes(query.toLowerCase()) ||
        t.owner?.toLowerCase().includes(query.toLowerCase()) ||
        t.tags.some((tag) => tag.toLowerCase().includes(query.toLowerCase()))
      )
    : tasks.slice(0, 10);

  const canCreate = query.trim() && !results.some((t) => t.title.toLowerCase() === query.toLowerCase());

  const totalItems = results.length + (canCreate ? 1 : 0);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (!isOpen) return;

      if (e.key === "Escape") {
        onClose();
        return;
      }

      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.min(prev + 1, totalItems - 1));
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.max(prev - 1, 0));
      }
      if (e.key === "Enter") {
        e.preventDefault();
        if (selectedIndex < results.length) {
          onSelectTask(results[selectedIndex]);
          onClose();
        } else if (canCreate) {
          onCreateTask(query.trim());
          onClose();
        }
      }
    },
    [isOpen, selectedIndex, totalItems, results, canCreate, query, onClose, onSelectTask, onCreateTask]
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl p-0 gap-0 overflow-hidden bg-card border-border">
        {/* Search input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
          <Search className="h-5 w-5 text-muted-foreground" />
          <Input
            ref={inputRef}
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="Search tasks or type to create..."
            className="border-0 bg-transparent text-base focus-visible:ring-0 focus-visible:ring-offset-0 px-0"
          />
          <kbd className="hidden sm:inline-flex items-center gap-1 px-2 py-1 rounded bg-secondary text-[10px] font-mono text-muted-foreground">
            <Command className="h-3 w-3" /> K
          </kbd>
        </div>

        {/* Results */}
        <div className="max-h-[400px] overflow-y-auto py-2">
          {results.length === 0 && !canCreate && (
            <div className="px-4 py-8 text-center text-muted-foreground text-sm">
              No tasks found
            </div>
          )}

          {results.map((task, index) => (
            <button
              key={task.id}
              onClick={() => {
                onSelectTask(task);
                onClose();
              }}
              onMouseEnter={() => setSelectedIndex(index)}
              className={cn(
                "w-full px-4 py-2.5 flex items-center gap-3 text-left transition-colors",
                selectedIndex === index ? "bg-accent" : "hover:bg-accent/50"
              )}
            >
              <div className="flex-shrink-0">
                <Hash className="h-4 w-4 text-muted-foreground" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{task.title}</p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-[10px] text-muted-foreground font-mono">
                    {task.id.slice(0, 8).toUpperCase()}
                  </span>
                  {task.owner && (
                    <span className="flex items-center gap-0.5 text-[10px] text-muted-foreground">
                      <User className="h-2.5 w-2.5" /> {task.owner}
                    </span>
                  )}
                  <Badge
                    variant="secondary"
                    className={cn(
                      "text-[9px] px-1 py-0 h-4 border-0",
                      task.priority === "critical" && "bg-red-500/20 text-red-400",
                      task.priority === "high" && "bg-amber-500/20 text-amber-400",
                      task.priority === "medium" && "bg-blue-500/20 text-blue-400",
                      task.priority === "low" && "bg-slate-500/20 text-slate-400"
                    )}
                  >
                    {task.priority}
                  </Badge>
                  <span className="text-[9px] text-muted-foreground">{task.status}</span>
                </div>
              </div>
              {selectedIndex === index && (
                <ArrowRight className="h-4 w-4 text-primary flex-shrink-0" />
              )}
            </button>
          ))}

          {/* Create new option */}
          {canCreate && (
            <button
              onClick={() => {
                onCreateTask(query.trim());
                onClose();
              }}
              onMouseEnter={() => setSelectedIndex(results.length)}
              className={cn(
                "w-full px-4 py-2.5 flex items-center gap-3 text-left transition-colors border-t border-border",
                selectedIndex === results.length ? "bg-accent" : "hover:bg-accent/50"
              )}
            >
              <div className="flex-shrink-0">
                <AlertCircle className="h-4 w-4 text-primary" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium">Create "{query.trim()}"</p>
                <p className="text-[10px] text-muted-foreground">New task in backlog</p>
              </div>
              {selectedIndex === results.length && (
                <ArrowRight className="h-4 w-4 text-primary flex-shrink-0" />
              )}
            </button>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-4 py-2 border-t border-border bg-secondary/30">
          <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
            <span className="flex items-center gap-1">
              <kbd className="px-1 py-0.5 rounded bg-secondary font-mono">↑↓</kbd> navigate
            </span>
            <span className="flex items-center gap-1">
              <kbd className="px-1 py-0.5 rounded bg-secondary font-mono">↵</kbd> select
            </span>
            <span className="flex items-center gap-1">
              <kbd className="px-1 py-0.5 rounded bg-secondary font-mono">esc</kbd> close
            </span>
          </div>
          <span className="text-[10px] text-muted-foreground">
            {results.length} result{results.length !== 1 ? "s" : ""}
          </span>
        </div>
      </DialogContent>
    </Dialog>
  );
}
