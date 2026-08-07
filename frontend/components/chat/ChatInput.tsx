"use client";

import { useState } from "react";
import { SendHorizontal } from "lucide-react";

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
    <div className="p-4 bg-white border-t border-gray-200 z-10">
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask WorkPilot..."
          disabled={disabled}
          className="w-full bg-gray-50 border border-gray-200 rounded-full py-3 pl-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || disabled}
          className="absolute right-2 p-2 text-indigo-600 hover:bg-indigo-50 rounded-full disabled:opacity-50 disabled:hover:bg-transparent transition-colors"
        >
          <SendHorizontal className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
}
