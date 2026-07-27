"use client";

import { useEffect, useState } from "react";
import { itRepository } from "@/repositories/itRepository";
import { TicketResponse } from "@/types/it";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { HeadphonesIcon } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function TicketsPage() {
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTickets = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await itRepository.getTickets();
      setTickets(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load tickets.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  if (isLoading) return <LoadingState message="Loading tickets..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchTickets} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">IT Helpdesk Tickets</h1>
        <Button variant="primary">New Ticket</Button>
      </div>

      {tickets.length === 0 ? (
        <EmptyState 
          title="No tickets found"
          description="There are no helpdesk tickets to display."
          icon={<HeadphonesIcon className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ticket #</TableHead>
              <TableHead>Title</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Priority</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Created At</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tickets.map((ticket) => (
              <TableRow key={ticket.id}>
                <TableCell className="font-medium text-muted-foreground">
                  {ticket.ticket_number}
                </TableCell>
                <TableCell>{ticket.title}</TableCell>
                <TableCell>{ticket.category}</TableCell>
                <TableCell>
                  <Badge variant={ticket.priority === "HIGH" ? "destructive" : "secondary"}>
                    {ticket.priority}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge 
                    variant={
                      ticket.status === "RESOLVED"
                        ? "success"
                        : ticket.status === "OPEN"
                        ? "warning"
                        : "secondary"
                    }
                  >
                    {ticket.status}
                  </Badge>
                </TableCell>
                <TableCell>{new Date(ticket.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
