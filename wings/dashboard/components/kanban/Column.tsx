"use client";

import { TaskCard } from "./TaskCard";
import type { Task } from "@/types";

interface ColumnProps {
  tasks: Task[];
}

export function Column({ tasks }: ColumnProps) {
  return (
    <div className="flex flex-1 flex-col gap-1 overflow-y-auto">
      {tasks.map((task, index) => (
        <TaskCard key={task.id} task={task} index={index} />
      ))}
    </div>
  );
}
