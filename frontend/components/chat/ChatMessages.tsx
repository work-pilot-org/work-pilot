"use client";

import { useEffect, useRef } from "react";
import { Message } from "./ChatPanel";
import { Sparkles, User } from "lucide-react";

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
    <div className="absolute inset-0 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
      {messages.map((msg) => {
        const isAi = msg.role === "ai";
        return (
          <div key={msg.id} className={`flex gap-3 max-w-[85%] ${isAi ? "mr-auto" : "ml-auto flex-row-reverse"}`}>
            <div className={`w-8 h-8 flex-shrink-0 rounded-full flex items-center justify-center ${isAi ? "bg-indigo-100" : "bg-gray-200"}`}>
              {isAi ? <Sparkles className="w-4 h-4 text-indigo-600" /> : <User className="w-4 h-4 text-gray-600" />}
            </div>
            <div className={`p-3 rounded-2xl text-sm ${isAi ? "bg-white border border-gray-200 text-gray-800 rounded-tl-none shadow-sm" : "bg-indigo-600 text-white rounded-tr-none shadow-sm"}`}>
              {msg.content}
            </div>
          </div>
        );
      })}
      
      {isTyping && (
        <div className="flex gap-3 max-w-[85%] mr-auto">
          <div className="w-8 h-8 flex-shrink-0 rounded-full bg-indigo-100 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="p-3 bg-white border border-gray-200 rounded-2xl rounded-tl-none shadow-sm flex gap-1 items-center">
            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
          </div>
        </div>
      )}
      <div ref={bottomRef} className="h-px" />
    </div>
  );
}
