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
import { HeadphonesIcon, AlertTriangle, CheckCircle2, Clock, Plus, Search, Filter, MonitorSmartphone } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Drawer } from "@/components/ui/Drawer";
import { DropdownMenu } from "@/components/ui/DropdownMenu";

export default function TicketsPage() {
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchKeyword, setSearchKeyword] = useState("");
  
  // Drawer state
  const [selectedTicket, setSelectedTicket] = useState<TicketResponse | null>(null);

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

  if (isLoading) return <LoadingState message="Loading IT workspace..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchTickets} />;

  // Derived context metrics
  const openTickets = tickets.filter(t => t.status === "OPEN" || t.status === "IN_PROGRESS");
  const urgentTickets = tickets.filter(t => (t.priority === "URGENT" || t.priority === "HIGH") && t.status !== "RESOLVED" && t.status !== "CLOSED");
  const recentlyResolved = tickets.filter(t => t.status === "RESOLVED").length;

  const filteredTickets = tickets.filter(t => 
    t.title.toLowerCase().includes(searchKeyword.toLowerCase()) || 
    t.ticket_number.toLowerCase().includes(searchKeyword.toLowerCase())
  );

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">IT Helpdesk</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage service requests, report issues, and view service health.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm">
            <Plus className="mr-2 h-4 w-4" />
            New Ticket
          </Button>
        </div>
      </div>

      {/* Service Context & Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 text-muted-foreground mb-3">
            <Clock className="h-5 w-5 text-primary" />
            <span className="text-sm font-semibold">Active Issues</span>
          </div>
          <div className="text-3xl font-bold text-foreground">{openTickets.length}</div>
          <p className="text-xs text-muted-foreground mt-1">Pending resolution</p>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm ring-1 ring-destructive/10">
          <div className="flex items-center gap-3 text-muted-foreground mb-3">
            <AlertTriangle className="h-5 w-5 text-destructive" />
            <span className="text-sm font-semibold">Urgent Attention</span>
          </div>
          <div className="text-3xl font-bold text-foreground">{urgentTickets.length}</div>
          <p className="text-xs text-muted-foreground mt-1">High priority tickets open</p>
        </div>

        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 text-muted-foreground mb-3">
            <CheckCircle2 className="h-5 w-5 text-success" />
            <span className="text-sm font-semibold">Service Health</span>
          </div>
          <div className="text-3xl font-bold text-foreground">99.9%</div>
          <p className="text-xs text-muted-foreground mt-1">{recentlyResolved} tickets resolved recently</p>
        </div>
      </div>

      {/* Ticket Management Area */}
      <div className="flex flex-col space-y-6">
        
        {/* Toolbar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface p-4 rounded-xl border border-border-strong shadow-sm">
          <div className="relative max-w-md w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search tickets..." 
              className="flex h-10 w-full rounded-md border border-border bg-transparent px-9 py-2 text-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="h-10 border-border text-muted-foreground bg-transparent">
              <Filter className="mr-2 h-4 w-4" />
              Filter by Status
            </Button>
          </div>
        </div>

        {filteredTickets.length === 0 ? (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-12">
            <EmptyState 
              title="No tickets found"
              description="You have a clean queue. There are no helpdesk tickets to display."
              icon={<HeadphonesIcon className="w-8 h-8 text-muted-foreground" />}
            />
          </div>
        ) : (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Ticket</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Priority</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredTickets.map((ticket) => (
                  <TableRow 
                    key={ticket.id} 
                    className="cursor-pointer group"
                    onClick={() => setSelectedTicket(ticket)}
                  >
                    <TableCell>
                      <div className="flex flex-col">
                        <span className="font-medium text-foreground group-hover:text-primary transition-colors">
                          {ticket.title}
                        </span>
                        <span className="text-xs text-muted-foreground mt-0.5">{ticket.ticket_number}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-foreground">{ticket.category}</span>
                    </TableCell>
                    <TableCell>
                      <Badge variant={ticket.priority === "HIGH" || ticket.priority === "URGENT" ? "destructive" : "secondary"}>
                        {ticket.priority}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge 
                        variant={
                          ticket.status === "RESOLVED" || ticket.status === "CLOSED" ? "success"
                            : ticket.status === "OPEN" ? "warning"
                            : "secondary"
                        }
                      >
                        {ticket.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu 
                        items={[
                          { label: "View Details", onClick: (e) => { e.stopPropagation(); setSelectedTicket(ticket); } },
                          { label: "Add Comment", onClick: (e) => { e.stopPropagation(); } },
                          { label: "Close Ticket", onClick: (e) => { e.stopPropagation(); } }
                        ]}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>

      {/* Ticket Detail Drawer */}
      <Drawer
        isOpen={!!selectedTicket}
        onClose={() => setSelectedTicket(null)}
        title={selectedTicket?.ticket_number}
        description="Ticket Details & History"
      >
        {selectedTicket && (
          <div className="space-y-8 py-2">
            
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-foreground leading-tight">{selectedTicket.title}</h3>
              <div className="flex items-center gap-2">
                <Badge variant={selectedTicket.status === "RESOLVED" || selectedTicket.status === "CLOSED" ? "success" : selectedTicket.status === "OPEN" ? "warning" : "secondary"}>
                  {selectedTicket.status}
                </Badge>
                <Badge variant={selectedTicket.priority === "HIGH" || selectedTicket.priority === "URGENT" ? "destructive" : "secondary"}>
                  {selectedTicket.priority}
                </Badge>
              </div>
            </div>

            <div className="h-px bg-border w-full" />

            <div className="space-y-6">
              <div>
                <h4 className="text-sm font-semibold text-foreground mb-2">Description</h4>
                <div className="bg-muted/50 p-4 rounded-lg text-sm text-foreground border border-border">
                  {selectedTicket.description || "No detailed description provided."}
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-xs text-muted-foreground block mb-1">Category</span>
                  <span className="text-sm font-medium text-foreground">{selectedTicket.category}</span>
                </div>
                <div>
                  <span className="text-xs text-muted-foreground block mb-1">Created At</span>
                  <span className="text-sm font-medium text-foreground">{new Date(selectedTicket.created_at).toLocaleString()}</span>
                </div>
              </div>
            </div>

            <div className="pt-6 mt-8 border-t border-border flex justify-end gap-3">
              <Button variant="outline" onClick={() => setSelectedTicket(null)}>
                Close
              </Button>
              <Button>
                Update Status
              </Button>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}
