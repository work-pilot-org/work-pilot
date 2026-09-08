"use client";

import { useEffect, useState } from "react";
import { itRepository } from "@/repositories/itRepository";
import { TicketResponse, CreateTicketRequest } from "@/types/it";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Plus, Ticket, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export function MyTickets() {
  const router = useRouter();
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isCreating, setIsCreating] = useState(false);
  const [newTicket, setNewTicket] = useState<CreateTicketRequest>({
    title: "",
    description: "",
    category: "OTHER",
    priority: "MEDIUM",
    source: "WEB",
  });

  const loadTickets = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await itRepository.getMyTickets();
      setTickets(data);
    } catch (err: any) {
      setError(err.message || "Failed to load tickets");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTickets();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      await itRepository.createTicket(newTicket);
      setIsCreating(false);
      setNewTicket({
        title: "",
        description: "",
        category: "OTHER",
        priority: "MEDIUM",
        source: "WEB",
      });
      await loadTickets();
    } catch (err: any) {
      alert(err.message || "Failed to create ticket");
      setIsLoading(false);
    }
  };

  if (isLoading && !isCreating && tickets.length === 0) return <LoadingState message="Loading your tickets..." />;
  if (error && tickets.length === 0) return <ErrorState message={error} />;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">My Tickets</h2>
          <p className="text-muted-foreground mt-1">View and manage your IT support requests.</p>
        </div>
        <Button onClick={() => setIsCreating(true)} disabled={isCreating}>
          <Plus className="w-4 h-4 mr-2" /> New Request
        </Button>
      </div>

      {isCreating && (
        <form onSubmit={handleCreate} className="bg-surface border border-border rounded-xl p-6 shadow-sm space-y-4">
          <h3 className="text-lg font-semibold mb-4">Create New Request</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Title</label>
              <input
                required
                type="text"
                value={newTicket.title}
                onChange={(e) => setNewTicket({ ...newTicket, title: e.target.value })}
                className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                placeholder="Brief description of the issue"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Description</label>
              <textarea
                required
                value={newTicket.description}
                onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
                className="w-full p-3 rounded-md border border-border bg-background text-sm min-h-[100px]"
                placeholder="Detailed explanation..."
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">Category</label>
                <select
                  value={newTicket.category}
                  onChange={(e) => setNewTicket({ ...newTicket, category: e.target.value as any })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                >
                  <option value="HARDWARE">Hardware</option>
                  <option value="SOFTWARE">Software</option>
                  <option value="NETWORK">Network</option>
                  <option value="ACCESS">Access</option>
                  <option value="ONBOARDING">Onboarding</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">Priority</label>
                <select
                  value={newTicket.priority}
                  onChange={(e) => setNewTicket({ ...newTicket, priority: e.target.value as any })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                >
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>
            </div>
          </div>
          
          <div className="flex justify-end gap-3 mt-6">
            <Button variant="outline" type="button" onClick={() => setIsCreating(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Submitting..." : "Submit Request"}
            </Button>
          </div>
        </form>
      )}

      {!isCreating && tickets.length === 0 && (
        <div className="bg-surface border border-border rounded-xl p-12 text-center text-muted-foreground flex flex-col items-center">
          <Ticket className="w-12 h-12 mb-4 text-muted" />
          <p className="text-lg font-medium text-foreground">No Tickets Found</p>
          <p className="mt-2 text-sm">You haven't submitted any support requests yet.</p>
        </div>
      )}

      {!isCreating && tickets.length > 0 && (
        <div className="bg-surface border border-border rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-surface-hover border-b border-border text-xs uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-6 py-4 font-medium">Ticket ID</th>
                <th className="px-6 py-4 font-medium w-full">Title</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Priority</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {tickets.map((ticket) => (
                <tr key={ticket.id} className="hover:bg-surface-hover/50 transition-colors">
                  <td className="px-6 py-4 font-mono text-xs">{ticket.ticket_number}</td>
                  <td className="px-6 py-4 font-medium text-foreground">
                    <div className="truncate max-w-[300px]">{ticket.title}</div>
                    <div className="text-xs text-muted-foreground font-normal mt-1">{ticket.category}</div>
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant={
                      ticket.status === 'RESOLVED' || ticket.status === 'CLOSED' ? 'success' :
                      ticket.status === 'IN_PROGRESS' ? 'warning' : 'secondary'
                    }>
                      {ticket.status}
                    </Badge>
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant={
                      ticket.priority === 'CRITICAL' || ticket.priority === 'HIGH' ? 'destructive' :
                      ticket.priority === 'MEDIUM' ? 'warning' : 'secondary'
                    }>
                      {ticket.priority}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button variant="ghost" size="sm" onClick={() => router.push(`/dashboard/employee/tickets/${ticket.id}`)}>
                      View <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
