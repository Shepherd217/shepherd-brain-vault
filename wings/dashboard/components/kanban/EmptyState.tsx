"use client";

import { Inbox } from "lucide-react";

interface EmptyStateProps {
  columnTitle: string;
}

export function EmptyState({ columnTitle }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-8 px-4 text-center">
      <div className="h-10 w-10 rounded-lg bg-secondary/50 flex items-center justify-center mb-3">
        <Inbox className="h-5 w-5 text-muted-foreground/60" />
      </div>
      <p className="text-xs text-muted-foreground/60 font-medium">
        No tasks in {columnTitle}
      </p>
      <p className="text-[10px] text-muted-foreground/40 mt-1">
        Use the quick add below to create one
      </p>
    </div>
  );
}
