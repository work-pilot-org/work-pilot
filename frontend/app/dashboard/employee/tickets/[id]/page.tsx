"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { itRepository } from "@/repositories/itRepository";
import { TicketResponse } from "@/types/it";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ArrowLeft } from "lucide-react";

export default function TicketDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [ticket, setTicket] = useState<TicketResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTicket = async () => {
      try {
        setIsLoading(true);
        const data = await itRepository.getTicketById(id);
        setTicket(data);
      } catch (err: any) {
        setError(err.message || "Failed to load ticket");
      } finally {
        setIsLoading(false);
      }
    };
    if (id) loadTicket();
  }, [id]);

  if (isLoading) return <LoadingState message="Loading ticket details..." />;
  if (error) return <ErrorState message={error} />;
  if (!ticket) return <ErrorState message="Ticket not found." />;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <Button variant="ghost" onClick={() => router.push("/dashboard/employee/tickets")} className="mb-4">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to My Tickets
      </Button>

      <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
        <div className="p-6 border-b border-border flex items-center justify-between bg-surface-hover/30">
          <div>
            <h2 className="text-xl font-bold text-foreground">{ticket.title}</h2>
            <p className="text-sm font-mono text-muted-foreground mt-1">{ticket.ticket_number}</p>
          </div>
          <div className="flex gap-2">
            <Badge variant={ticket.priority === 'CRITICAL' || ticket.priority === 'HIGH' ? 'destructive' : ticket.priority === 'MEDIUM' ? 'warning' : 'secondary'}>
              {ticket.priority}
            </Badge>
            <Badge variant={ticket.status === 'RESOLVED' || ticket.status === 'CLOSED' ? 'success' : ticket.status === 'IN_PROGRESS' ? 'warning' : 'secondary'}>
              {ticket.status}
            </Badge>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-2">Description</h3>
            <div className="bg-background border border-border rounded-lg p-4 text-sm text-foreground whitespace-pre-wrap">
              {ticket.description}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-2">Category</h3>
              <p className="text-sm text-muted-foreground">{ticket.category}</p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-2">Created</h3>
              <p className="text-sm text-muted-foreground">{new Date(ticket.created_at).toLocaleString()}</p>
            </div>
            {ticket.resolution && (
              <div className="col-span-2 mt-4">
                <h3 className="text-sm font-semibold text-success uppercase tracking-wider mb-2">Resolution</h3>
                <div className="bg-success/10 border border-success/20 rounded-lg p-4 text-sm text-foreground whitespace-pre-wrap">
                  {ticket.resolution}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
