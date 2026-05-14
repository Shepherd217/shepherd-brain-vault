"use client";

import { useState, useEffect, useCallback } from "react";
import type { Task } from "@/types";

const STORAGE_KEY = "shepherd-dashboard-tasks";

function loadFromStorage(): Task[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return parsed.map((t: Task) => ({
      ...t,
      createdAt: new Date(t.createdAt),
      startedAt: t.startedAt ? new Date(t.startedAt) : null,
      completedAt: t.completedAt ? new Date(t.completedAt) : null,
    }));
  } catch {
    return [];
  }
}

function saveToStorage(tasks: Task[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  } catch {
    // Storage full or blocked
  }
}

export function usePersistentTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loaded, setLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = loadFromStorage();
    setTasks(stored);
    setLoaded(true);
  }, []);

  // Save to localStorage on every change
  useEffect(() => {
    if (loaded) {
      saveToStorage(tasks);
    }
  }, [tasks, loaded]);

  // Also try to sync with API (fire-and-forget)
  const syncWithApi = useCallback(async () => {
    try {
      const res = await fetch("/api/tasks");
      if (res.ok) {
        const data = await res.json();
        if (data.tasks?.length > 0) {
          // Merge API tasks with local tasks (local wins on conflict)
          const apiTasks = data.tasks as Task[];
          setTasks((prev) => {
            const localIds = new Set(prev.map((t) => t.id));
            const newTasks = apiTasks.filter((t) => !localIds.has(t.id));
            if (newTasks.length > 0) {
              const merged = [...prev, ...newTasks];
              saveToStorage(merged);
              return merged;
            }
            return prev;
          });
        }
      }
    } catch {
      // API unavailable, localStorage is primary
    }
  }, []);

  // Sync once on load
  useEffect(() => {
    if (loaded) {
      syncWithApi();
    }
  }, [loaded, syncWithApi]);

  const addTask = useCallback(
    async (taskData: Partial<Task>) => {
      const newTask: Task = {
        id: crypto.randomUUID(),
        title: taskData.title || "Untitled",
        description: taskData.description || null,
        status: (taskData.status as any) || "backlog",
        priority: (taskData.priority as any) || "medium",
        owner: taskData.owner || null,
        agentType: taskData.agentType || null,
        tags: taskData.tags || [],
        projectId: taskData.projectId || "shepherd",
        dependencies: taskData.dependencies || [],
        createdAt: new Date(),
        startedAt: null,
        completedAt: null,
        attempts: 0,
        maxRetries: taskData.maxRetries || 3,
        worktreeId: null,
        result: null,
        error: null,
        requiresReview: taskData.requiresReview || false,
        nextTask: null,
      };

      setTasks((prev) => {
        const updated = [...prev, newTask];
        saveToStorage(updated);
        return updated;
      });

      // Also send to API
      try {
        await fetch("/api/tasks", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(taskData),
        });
      } catch {
        // API may fail, localStorage has it
      }

      return newTask;
    },
    []
  );

  const updateTask = useCallback(
    async (id: string, updates: Partial<Task>) => {
      setTasks((prev) => {
        const updated = prev.map((t) =>
          t.id === id ? { ...t, ...updates } : t
        );
        saveToStorage(updated);
        return updated;
      });

      // Also send to API
      try {
        await fetch(`/api/tasks/${id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updates),
        });
      } catch {
        // API may fail
      }
    },
    []
  );

  const removeTask = useCallback((id: string) => {
    setTasks((prev) => {
      const updated = prev.filter((t) => t.id !== id);
      saveToStorage(updated);
      return updated;
    });
  }, []);

  return {
    tasks,
    loaded,
    addTask,
    updateTask,
    removeTask,
    refresh: syncWithApi,
  };
}
