"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { itRepository } from "@/repositories/itRepository";
import { TicketResponse } from "@/types/it";
import { Laptop, AlertCircle, Clock, CheckCircle2, Ticket, ShieldAlert } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";

export function ITDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const data = await itRepository.getTickets();
        setTickets(data);
      } catch (err: unknown) {
        setError("Failed to load IT dashboard data.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading IT Operations..." className="py-20" />;
  if (error) return <ErrorState message={error} />;

  const activeTickets = tickets.filter(t => t.status !== "RESOLVED" && t.status !== "CLOSED");
  const urgentTickets = activeTickets.filter(t => t.priority === "URGENT" || t.priority === "HIGH");
  const unassignedCount = activeTickets.filter(t => !t.assigned_to).length;

  return (
    <div className="flex flex-col h-full space-y-6 max-w-7xl mx-auto pb-12">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-surface border border-border-strong rounded-xl p-6 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Laptop className="w-6 h-6 text-primary" />
            IT Service Desk, {user?.name || "Admin"}
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm" onClick={() => router.push('/dashboard/it/tickets')}>
            <Ticket className="w-4 h-4 mr-2" />
            View Queue
          </Button>
        </div>
      </div>
      
      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Active Tickets</span>
            <AlertCircle className="w-4 h-4 text-warning" />
          </div>
          <div className="text-3xl font-bold text-foreground">{activeTickets.length}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm border-l-4 border-l-destructive">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">High/Urgent</span>
            <ShieldAlert className="w-4 h-4 text-destructive" />
          </div>
          <div className="text-3xl font-bold text-foreground">{urgentTickets.length}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Unassigned</span>
            <Clock className="w-4 h-4 text-muted-foreground" />
          </div>
          <div className="text-3xl font-bold text-foreground">{unassignedCount}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Resolved (Total)</span>
            <CheckCircle2 className="w-4 h-4 text-success" />
          </div>
          <div className="text-3xl font-bold text-foreground">{tickets.length - activeTickets.length}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4">
        {/* Quick Links Panel */}
        <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Operations Center</h3>
          <div className="grid grid-cols-2 gap-4">
            <button onClick={() => router.push('/dashboard/it/tickets')} className="flex flex-col items-center justify-center p-6 bg-surface-hover/50 rounded-lg border border-border hover:border-primary transition-colors gap-3">
              <Ticket className="w-6 h-6 text-primary" />
              <span className="text-sm font-medium text-foreground">Ticket Queue</span>
            </button>
            <button onClick={() => router.push('/dashboard/it/assets')} className="flex flex-col items-center justify-center p-6 bg-surface-hover/50 rounded-lg border border-border hover:border-primary transition-colors gap-3">
              <Laptop className="w-6 h-6 text-primary" />
              <span className="text-sm font-medium text-foreground">Hardware Assets</span>
            </button>
          </div>
        </div>

        {/* Priority Attention */}
        <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-6 flex flex-col">
          <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-destructive" /> Needs Attention
          </h3>
          {urgentTickets.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-sm text-muted-foreground border-2 border-dashed border-border rounded-lg">
              No urgent tickets in the queue.
            </div>
          ) : (
            <div className="space-y-4 flex-1 overflow-auto max-h-[300px] pr-2">
              {urgentTickets.slice(0, 5).map(ticket => (
                <div key={ticket.id} className="flex items-center gap-4 p-3 rounded-lg border border-destructive/30 bg-destructive/5">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{ticket.title}</p>
                    <p className="text-xs text-muted-foreground truncate">{ticket.category} • {ticket.status}</p>
                  </div>
                  <Button variant="outline" size="sm" className="shadow-sm h-8 border-destructive/30 text-destructive hover:bg-destructive/10" onClick={() => router.push(`/dashboard/it/tickets`)}>
                    Resolve
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
