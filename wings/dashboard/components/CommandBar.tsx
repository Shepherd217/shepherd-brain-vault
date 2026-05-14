"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Target } from "lucide-react";

interface CommandBarProps {
  onSendMessage?: (msg: string, to: string) => void;
  onSetGoal?: (goal: string) => void;
}

export function CommandBar({ onSendMessage, onSetGoal }: CommandBarProps) {
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<"message" | "goal">("message");
  const [target, setTarget] = useState("broadcast");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;

    if (mode === "goal" && onSetGoal) {
      onSetGoal(input.trim());
    } else if (onSendMessage) {
      onSendMessage(input.trim(), target);
    }

    setInput("");
  }

  return (
    <div className="border-t bg-card p-3 md:p-4">
      <div className="flex items-center gap-2 mb-2">
        <button
          onClick={() => setMode("message")}
          className={`text-xs px-2 py-1 rounded ${
            mode === "message" ? "bg-primary text-primary-foreground" : "bg-muted"
          }`}
        >
          💬 Message
        </button>
        <button
          onClick={() => setMode("goal")}
          className={`text-xs px-2 py-1 rounded ${
            mode === "goal" ? "bg-primary text-primary-foreground" : "bg-muted"
          }`}
        >
          🎯 Goal
        </button>
        {mode === "message" && (
          <select
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            className="text-xs bg-muted rounded px-2 py-1"
          >
            <option value="broadcast">All Agents</option>
            <option value="ava">Ava</option>
            <option value="hermes">Hermes</option>
            <option value="eve">Eve</option>
          </select>
        )}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          placeholder={
            mode === "goal"
              ? "/goal Build feature X and deploy..."
              : "Send message to agents..."
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 h-10 md:h-10"
        />
        <Button
          type="submit"
          disabled={!input.trim()}
          className="h-10 w-10 p-0 md:w-auto md:px-4"
        >
          {mode === "goal" ? (
            <Target className="h-4 w-4" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </Button>
      </form>
    </div>
  );
}
