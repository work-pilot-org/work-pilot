"use client";

import { useEffect, useRef } from "react";
import { Message } from "./ChatPanel";
import { Sparkles } from "lucide-react";

interface ChatMessagesProps {
  messages: Message[];
  isTyping: boolean;
}

export function ChatMessages({ messages, isTyping }: ChatMessagesProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="absolute inset-0 overflow-y-auto p-4 space-y-6 bg-background">
      {messages.map((msg) => {
        const isAi = msg.role === "ai";
        if (!isAi) {
          return (
            <div key={msg.id} className="flex justify-end ml-auto">
              <div className="bg-surface border border-border/60 px-4 py-3 rounded-2xl max-w-[85%] text-sm text-foreground shadow-[var(--shadow-subtle)] whitespace-pre-wrap leading-relaxed">
                {msg.content}
              </div>
            </div>
          );
        }

        return (
          <div key={msg.id} className="flex gap-3 max-w-[90%] mr-auto items-start">
            <div className="w-8 h-8 rounded-xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center shrink-0 mt-0.5">
              <Sparkles className="w-3.5 h-3.5" />
            </div>
            <div className="flex flex-col gap-1.5 min-w-0 flex-1">
              <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest px-0.5">
                WorkPilot AI
              </div>
              <div className="text-sm leading-relaxed text-foreground whitespace-pre-wrap">
                {msg.content}
              </div>
            </div>
          </div>
        );
      })}
      
      {isTyping && (
        <div className="flex gap-3 max-w-[90%] mr-auto items-start">
          <div className="w-8 h-8 rounded-xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center shrink-0 mt-0.5">
            <Sparkles className="w-3.5 h-3.5" />
          </div>
          <div className="flex flex-col gap-1.5 min-w-0 flex-1">
            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest px-0.5">
              WorkPilot AI
            </div>
            <div className="flex gap-1.5 items-center h-5 px-1">
              <div className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce"></div>
            </div>
          </div>
        </div>
      )}
      <div ref={bottomRef} className="h-4" />
    </div>
  );
}
