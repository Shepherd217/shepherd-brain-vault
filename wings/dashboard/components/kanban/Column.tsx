"use client";

import { TaskCard } from "./TaskCard";
import type { Task } from "@/types";

interface ColumnProps {
  tasks: Task[];
}

export function Column({ tasks }: ColumnProps) {
  return (
    <div className="flex flex-1 flex-col gap-2 overflow-y-auto min-h-0 pb-4">
      {tasks.map((task, index) => (
        <TaskCard key={task.id} task={task} index={index} />
      ))}
    </div>
  );
}
