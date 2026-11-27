"use client";

import { useState } from "react";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  return (
    <div className="p-4 bg-background border-t border-border/40 z-10">
      <form onSubmit={handleSubmit} className="relative flex items-center bg-surface border border-border-strong rounded-xl shadow-[var(--shadow-subtle)] focus-within:ring-1 focus-within:ring-primary/20 focus-within:border-primary/40 transition-all">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask WorkPilot..."
          disabled={disabled}
          className="w-full bg-transparent py-3 pl-4 pr-12 text-sm focus:outline-none placeholder:text-muted-foreground/60 text-foreground disabled:opacity-50"
        />
        <Button
          type="submit"
          disabled={!input.trim() || disabled}
          size="sm"
          variant="primary"
          className="absolute right-1.5 p-0 w-8 h-8 rounded-lg shadow-none"
        >
          <Send className="w-4 h-4 ml-0.5" />
        </Button>
      </form>
    </div>
  );
}
