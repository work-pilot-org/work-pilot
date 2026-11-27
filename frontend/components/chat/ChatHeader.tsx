"use client";

import { X, Sparkles } from "lucide-react";

interface ChatHeaderProps {
  onClose: () => void;
}

export function ChatHeader({ onClose }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between px-4 py-3 bg-background border-b border-border/40 shadow-[var(--shadow-subtle)] z-10">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center shrink-0">
          <Sparkles className="w-4 h-4" />
        </div>
        <div>
          <h2 className="text-[13px] font-semibold text-foreground leading-tight">WorkPilot AI</h2>
          <p className="text-[10px] text-muted-foreground font-medium uppercase tracking-widest mt-0.5">Online</p>
        </div>
      </div>
      <button 
        onClick={onClose}
        className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-surface-hover rounded-lg transition-colors"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
