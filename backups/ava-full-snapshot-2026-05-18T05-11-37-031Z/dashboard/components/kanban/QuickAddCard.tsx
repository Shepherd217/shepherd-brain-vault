"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Plus, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface QuickAddCardProps {
  columnId: string;
  onAdd: (title: string) => void;
}

export function QuickAddCard({ columnId, onAdd }: QuickAddCardProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  function handleOpen() {
    setIsOpen(true);
    setTimeout(() => inputRef.current?.focus(), 50);
  }

  function handleClose() {
    setIsOpen(false);
    setTitle("");
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    onAdd(title.trim());
    setTitle("");
    inputRef.current?.focus();
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Escape") {
      handleClose();
    }
  }

  if (!isOpen) {
    return (
      <Button
        variant="ghost"
        size="sm"
        onClick={handleOpen}
        className={cn(
          "w-full justify-start gap-1.5 text-muted-foreground/60 hover:text-muted-foreground",
          "hover:bg-secondary/50 h-8 text-xs"
        )}
      >
        <Plus className="h-3.5 w-3.5" />
        Add task
      </Button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input
        ref={inputRef}
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="What needs to be done?"
        className={cn(
          "w-full rounded-md border bg-card px-3 py-2 text-sm",
          "border-border/60 text-foreground placeholder:text-muted-foreground/40",
          "focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary/50"
        )}
      />
      <div className="flex items-center gap-2">
        <Button type="submit" size="sm" className="h-7 text-xs" disabled={!title.trim()}>
          Create
        </Button>
        <Button type="button" variant="ghost" size="sm" onClick={handleClose} className="h-7 w-7 p-0">
          <X className="h-3.5 w-3.5" />
        </Button>
      </div>
    </form>
  );
}
