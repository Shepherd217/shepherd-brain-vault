"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Plus, X } from "lucide-react";
import type { Task } from "@/types";

interface CreateTaskModalProps {
  onTaskCreated: (task: Task) => void;
}

export function CreateTaskModal({ onTaskCreated }: CreateTaskModalProps) {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [owner, setOwner] = useState("");
  const [agentType, setAgentType] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  function addTag() {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()]);
      setTagInput("");
    }
  }

  function removeTag(tag: string) {
    setTags(tags.filter((t) => t !== tag));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() || undefined,
          priority,
          owner: owner.trim() || undefined,
          agentType: agentType || undefined,
          tags,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        onTaskCreated(data.task);
        setOpen(false);
        resetForm();
      }
    } catch (error) {
      console.error("Failed to create task:", error);
    } finally {
      setLoading(false);
    }
  }

  function resetForm() {
    setTitle("");
    setDescription("");
    setPriority("medium");
    setOwner("");
    setAgentType("");
    setTags([]);
    setTagInput("");
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          className={`gap-2 ${isMobile ? "rounded-full h-14 w-14 p-0 shadow-lg" : ""}`}
          size={isMobile ? "icon" : "default"}
        >
          <Plus className="h-5 w-5" />
          {!isMobile && <span>New Task</span>}
        </Button>
      </DialogTrigger>
      <DialogContent className={isMobile ? "w-[95vw] max-w-[95vw] h-[90vh] max-h-[90vh] p-4 gap-2" : "sm:max-w-[500px]"}>
        <DialogHeader className={isMobile ? "pb-2" : ""}>
          <DialogTitle>Create New Task</DialogTitle>
          <DialogDescription>
            Add a task to the Shepherd Team Dashboard
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-3 md:space-y-4 overflow-y-auto flex-1">
          <div className="space-y-1.5 md:space-y-2">
            <label className="text-sm font-medium">Title</label>
            <Input
              placeholder="Task title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="h-11 md:h-10"
            />
          </div>

          <div className="space-y-1.5 md:space-y-2">
            <label className="text-sm font-medium">Description</label>
            <Textarea
              placeholder="What needs to be done?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={isMobile ? 3 : 3}
              className="min-h-[80px]"
            />
          </div>

          <div className="grid grid-cols-2 gap-3 md:gap-4">
            <div className="space-y-1.5 md:space-y-2">
              <label className="text-sm font-medium">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="flex h-11 md:h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>

            <div className="space-y-1.5 md:space-y-2">
              <label className="text-sm font-medium">Owner</label>
              <Input
                placeholder="ava, hermes, eve..."
                value={owner}
                onChange={(e) => setOwner(e.target.value)}
                className="h-11 md:h-10"
              />
            </div>
          </div>

          <div className="space-y-1.5 md:space-y-2">
            <label className="text-sm font-medium">Agent Type</label>
            <select
              value={agentType}
              onChange={(e) => setAgentType(e.target.value)}
              className="flex h-11 md:h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              <option value="">Select type...</option>
              <option value="openclaw">OpenClaw</option>
              <option value="hermes">Hermes</option>
              <option value="human">Human</option>
            </select>
          </div>

          <div className="space-y-1.5 md:space-y-2">
            <label className="text-sm font-medium">Tags</label>
            <div className="flex gap-2">
              <Input
                placeholder="Add tag..."
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addTag();
                  }
                }}
                className="h-11 md:h-10"
              />
              <Button type="button" variant="outline" onClick={addTag} className="h-11 md:h-10">
                Add
              </Button>
            </div>
            <div className="flex flex-wrap gap-1">
              {tags.map((tag) => (
                <Badge key={tag} variant="secondary" className="gap-1 text-sm py-1 px-2">
                  {tag}
                  <X
                    className="h-3 w-3 cursor-pointer"
                    onClick={() => removeTag(tag)}
                  />
                </Badge>
              ))}
            </div>
          </div>
        </form>
        <DialogFooter className={isMobile ? "pt-2 gap-2" : ""}>
          <Button type="button" variant="outline" onClick={() => setOpen(false)} className="h-11 md:h-10">
            Cancel
          </Button>
          <Button type="submit" disabled={loading || !title.trim()} onClick={handleSubmit} className="h-11 md:h-10">
            {loading ? "Creating..." : "Create Task"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
