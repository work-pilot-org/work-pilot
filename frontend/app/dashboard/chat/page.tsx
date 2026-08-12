"use client";

import { useState, useRef, useEffect } from "react";
import { aiRepository } from "@/repositories/aiRepository";
import { Sparkles, Send, Bot, Clock, Plus, Settings2, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface Message {
  id: string;
  role: "user" | "ai";
  content: string;
}

interface Conversation {
  id: string;
  title: string;
  date: string;
  messages: Message[];
}

export default function AIWorkspacePage() {
  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: "default",
      title: "New Conversation",
      date: new Date().toLocaleDateString(),
      messages: [
        {
          id: "1",
          role: "ai",
          content: "Hello. I'm WorkPilot AI. I can help you analyze organizational data, manage requests, or answer questions about company policies. What would you like to do?"
        }
      ]
    }
  ]);
  
  const [activeId, setActiveId] = useState<string>("default");
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const activeConversation = conversations.find(c => c.id === activeId);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeConversation?.messages, isTyping]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isTyping) return;
    const content = inputValue;
    setInputValue("");
    setIsTyping(true);
    
    // Add user message
    const userMsgId = Date.now().toString();
    setConversations(prev => prev.map(c => {
      if (c.id === activeId) {
        return {
          ...c,
          title: c.messages.length === 1 ? content.slice(0, 30) + "..." : c.title,
          messages: [...c.messages, { id: userMsgId, role: "user", content }]
        };
      }
      return c;
    }));
    
    try {
      const response = await aiRepository.chat({ message: content });
      
      setConversations(prev => prev.map(c => {
        if (c.id === activeId) {
          return {
            ...c,
            messages: [...c.messages, { id: (Date.now() + 1).toString(), role: "ai", content: response.data }]
          };
        }
        return c;
      }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || "Failed to communicate with AI.";
      setConversations(prev => prev.map(c => {
        if (c.id === activeId) {
          return {
            ...c,
            messages: [...c.messages, { id: (Date.now() + 1).toString(), role: "ai", content: errorMessage }]
          };
        }
        return c;
      }));
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const startNewConversation = () => {
    const newId = Date.now().toString();
    setConversations(prev => [{
      id: newId,
      title: "New Conversation",
      date: new Date().toLocaleDateString(),
      messages: [{
        id: "1",
        role: "ai",
        content: "How can I help you today?"
      }]
    }, ...prev]);
    setActiveId(newId);
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] max-w-[1600px] mx-auto overflow-hidden bg-surface border-x border-border shadow-sm">
      
      {/* Sidebar - Conversation History */}
      <div className="w-80 border-r border-border bg-surface-hover/30 flex flex-col hidden md:flex">
        <div className="p-4 border-b border-border flex items-center justify-between">
          <Button onClick={startNewConversation} className="w-full justify-start shadow-sm" variant="primary">
            <Plus className="w-4 h-4 mr-2" />
            New Chat
          </Button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-2 mt-2">Recent</div>
          {conversations.map(conv => (
            <button
              key={conv.id}
              onClick={() => setActiveId(conv.id)}
              className={`w-full text-left px-3 py-3 rounded-lg text-sm transition-colors group flex items-start gap-3 ${
                activeId === conv.id 
                  ? "bg-surface border border-border-strong shadow-sm" 
                  : "hover:bg-surface border border-transparent"
              }`}
            >
              <Clock className={`w-4 h-4 mt-0.5 shrink-0 ${activeId === conv.id ? "text-primary" : "text-muted-foreground"}`} />
              <div className="flex-1 overflow-hidden">
                <div className={`truncate font-medium ${activeId === conv.id ? "text-foreground" : "text-muted-foreground group-hover:text-foreground"}`}>
                  {conv.title}
                </div>
                <div className="text-xs text-muted-foreground mt-1">{conv.date}</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-surface relative">
        
        {/* Chat Header */}
        <div className="h-14 border-b border-border flex items-center justify-between px-6 bg-surface z-10 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-primary" />
            </div>
            <div>
              <h2 className="font-semibold text-foreground text-sm">WorkPilot Intelligence</h2>
              <p className="text-xs text-muted-foreground">Context-aware enterprise assistant</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="h-8 w-8 p-0 text-muted-foreground">
              <Settings2 className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-8 scroll-smooth">
          {activeConversation?.messages.map((msg) => {
            const isAi = msg.role === "ai";
            return (
              <div key={msg.id} className={`flex gap-4 max-w-4xl mx-auto ${isAi ? "" : "flex-row-reverse"}`}>
                <div className={`w-8 h-8 shrink-0 rounded-lg flex items-center justify-center shadow-sm ${
                  isAi ? "bg-primary/10 border border-primary/20" : "bg-muted border border-border"
                }`}>
                  {isAi ? <Bot className="w-4 h-4 text-primary" /> : <div className="w-4 h-4 rounded-full bg-foreground/20" />}
                </div>
                
                <div className={`flex flex-col gap-1 max-w-[80%] ${isAi ? "items-start" : "items-end"}`}>
                  <div className="text-xs font-medium text-muted-foreground px-1">
                    {isAi ? "WorkPilot AI" : "You"}
                  </div>
                  <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                    isAi 
                      ? "bg-surface border border-border-strong text-foreground rounded-tl-none" 
                      : "bg-foreground text-background rounded-tr-none"
                  }`}>
                    {msg.content}
                  </div>
                </div>
              </div>
            );
          })}
          
          {isTyping && (
            <div className="flex gap-4 max-w-4xl mx-auto">
              <div className="w-8 h-8 shrink-0 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center shadow-sm">
                <Bot className="w-4 h-4 text-primary" />
              </div>
              <div className="flex flex-col gap-1 items-start">
                <div className="text-xs font-medium text-muted-foreground px-1">WorkPilot AI</div>
                <div className="p-4 bg-surface border border-border-strong rounded-2xl rounded-tl-none shadow-sm flex gap-1 items-center h-[52px]">
                  <div className="w-1.5 h-1.5 bg-muted-foreground/50 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-1.5 h-1.5 bg-muted-foreground/50 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-1.5 h-1.5 bg-muted-foreground/50 rounded-full animate-bounce"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} className="h-4" />
        </div>

        {/* Input Area */}
        <div className="p-4 md:p-6 bg-surface border-t border-border">
          <div className="max-w-4xl mx-auto relative">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask WorkPilot anything about your organization..."
              className="w-full bg-surface-hover/50 border border-border-strong rounded-xl pl-4 pr-14 py-4 text-sm focus:outline-none focus:ring-1 focus:ring-primary focus:bg-surface resize-none shadow-sm transition-all placeholder:text-muted-foreground/70"
              rows={1}
              style={{ minHeight: '56px', maxHeight: '150px' }}
            />
            <Button 
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              size="sm"
              className="absolute right-2 bottom-2 h-10 w-10 p-0 rounded-lg shadow-sm"
            >
              <Send className="w-4 h-4 ml-0.5" />
            </Button>
          </div>
          <div className="text-center mt-3">
            <span className="text-[10px] text-muted-foreground">AI can make mistakes. Verify important organizational information.</span>
          </div>
        </div>
        
      </div>
    </div>
  );
}
