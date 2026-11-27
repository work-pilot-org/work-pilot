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
  const [conversations, setConversations] = useState<any[]>([]);
  
  const [activeId, setActiveId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const activeConversation = conversations.find(c => c.id === activeId);

  useEffect(() => {
    // Load conversations on mount
    aiRepository.getConversations().then(data => {
      setConversations(data);
      if (data.length > 0) {
        setActiveId(data[0].id);
      }
    }).catch(console.error);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeConversation?.messages, isTyping]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isTyping) return;
    const content = inputValue;
    setInputValue("");
    setIsTyping(true);
    
    // Optimistic user message update
    const userMsgId = Date.now().toString();
    const newUserMsg = { id: userMsgId, role: "user", content, created_at: new Date().toISOString() };
    
    if (activeId) {
      setConversations(prev => prev.map(c => {
        if (c.id === activeId) {
          return { ...c, messages: [...c.messages, newUserMsg] };
        }
        return c;
      }));
    } else {
      // Temporary state while backend creates it
      const tempId = "temp-" + Date.now();
      setActiveId(tempId);
      setConversations(prev => [{ id: tempId, title: "New Conversation", date: "Today", messages: [newUserMsg] }, ...prev]);
    }
    
    try {
      const response = await aiRepository.chat({ 
        message: content,
        conversation_id: activeId && !activeId.startsWith("temp-") ? activeId : undefined
      });
      
      const newAiMsg = { id: (Date.now() + 1).toString(), role: "ai", content: response.data, created_at: new Date().toISOString() };
      
      // Refresh all conversations to get updated title/list
      const latestConvs = await aiRepository.getConversations();
      setConversations(latestConvs);
      if (response.conversation_id) {
          setActiveId(response.conversation_id);
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || "Failed to communicate with AI.";
      const errorMsg = { id: (Date.now() + 1).toString(), role: "ai", content: errorMessage, created_at: new Date().toISOString() };
      setConversations(prev => prev.map(c => {
        if (c.id === activeId || (c.id.startsWith("temp-") && activeId?.startsWith("temp-"))) {
          return { ...c, messages: [...c.messages, errorMsg] };
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
    setActiveId(null);
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] max-w-screen-2xl mx-auto overflow-hidden bg-background">
      
      {/* Sidebar - Conversation History */}
      <div className="w-72 border-r border-border/50 bg-surface flex flex-col hidden md:flex">
        <div className="p-4 border-b border-border/40">
          <Button onClick={startNewConversation} className="w-full justify-start shadow-[var(--shadow-sm)]" variant="primary">
            <Plus className="w-4 h-4 mr-2" />
            New Chat
          </Button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-2 px-3 mt-4">Recent Conversations</div>
          {conversations.map(conv => (
            <button
              key={conv.id}
              onClick={() => setActiveId(conv.id)}
              className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors group flex items-start gap-3 ${
                activeId === conv.id 
                  ? "bg-surface-hover/80 border border-border/60 shadow-[var(--shadow-subtle)]" 
                  : "hover:bg-surface-hover/40 border border-transparent"
              }`}
            >
              <Clock className={`w-4 h-4 mt-0.5 shrink-0 ${activeId === conv.id ? "text-primary" : "text-muted-foreground/50 group-hover:text-muted-foreground"}`} />
              <div className="flex-1 overflow-hidden">
                <div className={`truncate font-medium text-[13px] ${activeId === conv.id ? "text-foreground" : "text-muted-foreground group-hover:text-foreground"}`}>
                  {conv.title}
                </div>
                <div className="text-[11px] text-muted-foreground/70 mt-0.5">{conv.date}</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative bg-background">
        
        {/* Chat Header */}
        <div className="h-16 border-b border-border/40 flex items-center justify-between px-8 bg-background/80 backdrop-blur-md z-10 shrink-0">
          <div className="flex items-center gap-4">
            <div className="w-9 h-9 rounded-xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center shrink-0">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h2 className="font-semibold text-foreground text-[14px]">WorkPilot AI</h2>
              <p className="text-[12px] text-muted-foreground">Your intelligent workplace assistant</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="h-9 px-3 text-muted-foreground border-border/50 hover:bg-surface hover:text-foreground shadow-none">
              <Settings2 className="w-4 h-4 mr-2" />
              Settings
            </Button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 md:px-8 py-8 space-y-10 scroll-smooth">
          {!activeConversation && !isTyping && (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-6 max-w-md mx-auto">
              <div className="w-16 h-16 rounded-2xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center mb-2">
                <Sparkles className="w-8 h-8" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold tracking-tight text-foreground">How can I help you today?</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Ask me about your organization's data, request time off, or query IT issues. I have context on your current projects.
                </p>
              </div>
              
              {/* Subtle suggestions */}
              <div className="grid grid-cols-2 gap-3 w-full mt-4">
                <button onClick={() => setInputValue("What are my pending tasks?")} className="p-4 text-left border border-border/50 rounded-xl hover:border-primary/30 hover:bg-surface-hover/30 transition-all text-sm font-medium text-muted-foreground hover:text-foreground">
                  View my pending tasks
                </button>
                <button onClick={() => setInputValue("Check my leave balance")} className="p-4 text-left border border-border/50 rounded-xl hover:border-primary/30 hover:bg-surface-hover/30 transition-all text-sm font-medium text-muted-foreground hover:text-foreground">
                  Check leave balance
                </button>
              </div>
            </div>
          )}
          
          {activeConversation?.messages.map((msg: Message) => {
            const isAi = msg.role === "ai";
            
            if (!isAi) {
              return (
                <div key={msg.id} className="flex justify-end max-w-3xl mx-auto">
                  <div className="bg-surface border border-border/60 px-5 py-3.5 rounded-2xl max-w-[85%] text-sm text-foreground shadow-[var(--shadow-subtle)] whitespace-pre-wrap leading-relaxed">
                    {msg.content}
                  </div>
                </div>
              );
            }

            return (
              <div key={msg.id} className="flex gap-5 max-w-3xl mx-auto items-start w-full">
                <div className="w-9 h-9 rounded-xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center shrink-0 mt-0.5">
                  <Sparkles className="w-4 h-4" />
                </div>
                
                <div className="flex flex-col gap-1.5 min-w-0 flex-1">
                  <div className="text-[11px] font-bold text-muted-foreground uppercase tracking-widest px-0.5">
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
            <div className="flex gap-5 max-w-3xl mx-auto items-start w-full">
              <div className="w-9 h-9 rounded-xl bg-primary/5 text-primary ring-1 ring-primary/10 flex items-center justify-center shrink-0 mt-0.5">
                <Sparkles className="w-4 h-4" />
              </div>
              <div className="flex flex-col gap-1.5 min-w-0 flex-1">
                <div className="text-[11px] font-bold text-muted-foreground uppercase tracking-widest px-0.5">WorkPilot AI</div>
                <div className="flex gap-1.5 items-center h-6 px-1">
                  <div className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} className="h-8" />
        </div>

        {/* Input Area */}
        <div className="p-6 pt-2 bg-gradient-to-t from-background via-background to-transparent pb-8">
          <div className="max-w-3xl mx-auto relative bg-surface border border-border-strong rounded-2xl shadow-[var(--shadow-sm)] focus-within:ring-1 focus-within:ring-primary/20 focus-within:border-primary/40 transition-all duration-200">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask WorkPilot anything about your workspace..."
              className="w-full bg-transparent p-5 pb-12 text-sm focus:outline-none resize-none placeholder:text-muted-foreground/60 text-foreground leading-relaxed"
              rows={1}
              style={{ minHeight: '120px', maxHeight: '200px' }}
            />
            <div className="absolute bottom-3 left-3 right-3 flex justify-between items-center bg-surface">
              <div className="flex items-center gap-2">
                {/* Placeholder for attachments/tools if needed in future */}
              </div>
              <Button 
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isTyping}
                size="sm"
                variant="primary"
                className="h-9 px-4 rounded-xl shadow-sm font-semibold tracking-wide"
              >
                <span className="mr-2">Send</span>
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <div className="text-center mt-4">
            <span className="text-[11px] font-medium text-muted-foreground/70">
              WorkPilot AI is an automated assistant. Verify important organizational actions.
            </span>
          </div>
        </div>
        
      </div>
    </div>
  );
}
