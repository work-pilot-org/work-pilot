"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { Laptop, AlertCircle, Clock, CheckCircle2, Ticket, ShieldAlert } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { getTicketSummary, getAssetAssignments } from "@/lib/api/analytics";
import { CustomBarChart, CustomPieChart } from "@/components/analytics/AnalyticsCharts";

export function ITDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  
  const [ticketSummary, setTicketSummary] = useState<any[]>([]);
  const [assetAssignments, setAssetAssignments] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [ticketsData, assetsData] = await Promise.all([
          getTicketSummary().catch(() => ({ summary: [] })),
          getAssetAssignments().catch(() => ({ assignments: [] }))
        ]);
        setTicketSummary(ticketsData.summary || []);
        setAssetAssignments(assetsData.assignments || []);
      } catch (err: unknown) {
        setError("Failed to load IT dashboard analytics data.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading IT Operations..." className="py-20" />;
  if (error) return <ErrorState message={error} />;

  const activeTickets = ticketSummary.filter(t => t.status !== "RESOLVED" && t.status !== "CLOSED")
    .reduce((acc, curr) => acc + (curr.tickets || 0), 0);
  
  const urgentTickets = ticketSummary.filter(t => (t.priority === "URGENT" || t.priority === "HIGH") && t.status !== "RESOLVED" && t.status !== "CLOSED")
    .reduce((acc, curr) => acc + (curr.tickets || 0), 0);

  const resolvedTickets = ticketSummary.filter(t => t.status === "RESOLVED" || t.status === "CLOSED")
    .reduce((acc, curr) => acc + (curr.tickets || 0), 0);

  const activeAssets = assetAssignments.filter(a => a.status === "ACTIVE").length;

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
          <div className="text-3xl font-bold text-foreground">{activeTickets}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm border-l-4 border-l-destructive">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">High/Urgent Active</span>
            <ShieldAlert className="w-4 h-4 text-destructive" />
          </div>
          <div className="text-3xl font-bold text-foreground">{urgentTickets}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Active Asset Assignments</span>
            <Laptop className="w-4 h-4 text-muted-foreground" />
          </div>
          <div className="text-3xl font-bold text-foreground">{activeAssets}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Resolved Tickets</span>
            <CheckCircle2 className="w-4 h-4 text-success" />
          </div>
          <div className="text-3xl font-bold text-foreground">{resolvedTickets}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4">
        <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
          <h3 className="text-lg font-medium text-foreground mb-4">Tickets by Status & Priority</h3>
          <CustomBarChart 
            data={ticketSummary} 
            xAxisKey="status" 
            bars={[{ key: "tickets", color: "#f59e0b", name: "Tickets" }]} 
          />
        </div>
        
        <div className="bg-surface p-6 rounded-xl border border-border shadow-sm flex flex-col">
          <h3 className="text-lg font-medium text-foreground mb-4">Recent Asset Assignments</h3>
          <div className="flex-1 overflow-auto max-h-[300px]">
            {assetAssignments.length === 0 ? (
              <div className="h-full flex items-center justify-center text-muted-foreground text-sm border-2 border-dashed border-border rounded-lg">
                No recent assignments
              </div>
            ) : (
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-muted-foreground uppercase bg-surface-hover sticky top-0">
                  <tr>
                    <th className="px-4 py-2">Asset</th>
                    <th className="px-4 py-2">Employee</th>
                    <th className="px-4 py-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {assetAssignments.slice(0, 5).map((asset, i) => (
                    <tr key={i} className="border-b border-border">
                      <td className="px-4 py-3 font-medium text-foreground">{asset.asset_name}</td>
                      <td className="px-4 py-3">{asset.employee_name || 'N/A'}</td>
                      <td className="px-4 py-3">
                        <span className="bg-primary/10 text-primary px-2 py-1 rounded-full text-xs font-semibold">{asset.status}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
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
      </div>

    </div>
  );
}
