"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import type { Task } from "@/types";

const STORAGE_KEY = "shepherd-dashboard-tasks";
const POLL_INTERVAL_MS = 5000;

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
  const [isOnline, setIsOnline] = useState(true);
  const lastSyncRef = useRef<number>(0);

  // Load from API (primary), fallback to localStorage
  const fetchTasks = useCallback(async () => {
    try {
      const res = await fetch("/api/tasks");
      if (res.ok) {
        const data = await res.json();
        const apiTasks = (data.tasks as Task[]).map((t) => ({
          ...t,
          createdAt: new Date(t.createdAt),
          startedAt: t.startedAt ? new Date(t.startedAt) : null,
          completedAt: t.completedAt ? new Date(t.completedAt) : null,
        }));
        setTasks(apiTasks);
        saveToStorage(apiTasks);
        setIsOnline(true);
        lastSyncRef.current = Date.now();
        return;
      }
    } catch {
      // API unavailable
    }
    // Fallback to localStorage
    const stored = loadFromStorage();
    setTasks(stored);
    setIsOnline(false);
  }, []);

  useEffect(() => {
    fetchTasks().then(() => setLoaded(true));
  }, [fetchTasks]);

  // Real-time polling
  useEffect(() => {
    if (!loaded) return;
    const interval = setInterval(fetchTasks, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [loaded, fetchTasks]);

  const addTask = useCallback(
    async (taskData: Partial<Task>) => {
      const tempTask: Task = {
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

      // Optimistic UI
      setTasks((prev) => {
        const updated = [...prev, tempTask];
        saveToStorage(updated);
        return updated;
      });

      // Send to API
      try {
        const res = await fetch("/api/tasks", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(taskData),
        });
        if (res.ok) {
          const data = await res.json();
          // Replace temp with server task
          setTasks((prev) =>
            prev.map((t) => (t.id === tempTask.id ? data.task : t))
          );
          setIsOnline(true);
        }
      } catch {
        setIsOnline(false);
      }

      return tempTask;
    },
    []
  );

  const updateTask = useCallback(
    async (id: string, updates: Partial<Task>) => {
      // Optimistic UI
      setTasks((prev) => {
        const updated = prev.map((t) =>
          t.id === id ? { ...t, ...updates } : t
        );
        saveToStorage(updated);
        return updated;
      });

      // Send to API
      try {
        const res = await fetch(`/api/tasks/${id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updates),
        });
        if (res.ok) {
          setIsOnline(true);
        }
      } catch {
        setIsOnline(false);
      }
    },
    []
  );

  const claimTask = useCallback(
    async (id: string, agentId: string, agentName: string) => {
      return updateTask(id, {
        owner: agentId,
        status: "doing",
        agentType: "openclaw",
      });
    },
    [updateTask]
  );

  const removeTask = useCallback(async (id: string) => {
    setTasks((prev) => {
      const updated = prev.filter((t) => t.id !== id);
      saveToStorage(updated);
      return updated;
    });

    try {
      await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    } catch {
      // Will be cleaned up on next sync
    }
  }, []);

  return {
    tasks,
    loaded,
    isOnline,
    lastSync: lastSyncRef.current,
    addTask,
    updateTask,
    claimTask,
    removeTask,
    refresh: fetchTasks,
  };
}
