"use client";

import { ChatHeader } from "./ChatHeader";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import { useState, useRef, useEffect } from "react";
import { aiRepository } from "@/repositories/aiRepository";
import toast from "react-hot-toast";

interface ChatPanelProps {
  onClose: () => void;
}

export interface Message {
  id: string;
  role: "user" | "ai";
  content: string;
}

export function ChatPanel({ onClose }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "ai",
      content: "Hello! I'm your WorkPilot AI assistant. How can I help you today?"
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async (content: string) => {
    const newMessage: Message = { id: Date.now().toString(), role: "user", content };
    setMessages(prev => [...prev, newMessage]);
    setIsTyping(true);
    
    try {
      const response = await aiRepository.chat({ message: content });
      
      setMessages(prev => [
        ...prev, 
        { id: (Date.now() + 1).toString(), role: "ai", content: response.data }
      ]);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || "Failed to communicate with AI.";
      setMessages(prev => [
        ...prev, 
        { id: (Date.now() + 1).toString(), role: "ai", content: errorMessage }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      <ChatHeader onClose={onClose} />
      <div className="flex-1 overflow-hidden relative">
        <ChatMessages messages={messages} isTyping={isTyping} />
      </div>
      <ChatInput onSend={handleSendMessage} disabled={isTyping} />
    </div>
  );
}
