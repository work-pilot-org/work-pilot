"use client";

import { X, Sparkles } from "lucide-react";

interface ChatHeaderProps {
  onClose: () => void;
}

export function ChatHeader({ onClose }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200 shadow-sm z-10">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-indigo-600" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-gray-900">WorkPilot AI</h2>
          <p className="text-[10px] text-green-600 font-medium uppercase tracking-wider">Online</p>
        </div>
      </div>
      <button 
        onClick={onClose}
        className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  );
}
