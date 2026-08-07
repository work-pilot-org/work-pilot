"use client";

import { useState } from "react";
import { MessageSquare, X } from "lucide-react";
import { ChatPanel } from "./ChatPanel";

export function ChatLauncher() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {isOpen && (
        <div className="fixed bottom-20 right-6 z-50 w-[400px] h-[600px] bg-white rounded-xl shadow-2xl flex flex-col border border-gray-200 overflow-hidden">
          <ChatPanel onClose={() => setIsOpen(false)} />
        </div>
      )}
      
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 hover:shadow-xl transition-all flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600"
      >
        {isOpen ? <X className="w-6 h-6" /> : <MessageSquare className="w-6 h-6" />}
      </button>
    </>
  );
}
