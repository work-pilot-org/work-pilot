"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { Laptop, AlertCircle, Clock, CheckCircle2, Ticket, ShieldAlert, ArrowRight } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
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
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto w-full pb-12">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-2">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            IT Service Desk
          </h1>
          <p className="text-sm font-medium text-muted-foreground mt-1">
            Welcome back, {user?.name || "Admin"} • {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="primary" onClick={() => router.push('/dashboard/it/tickets')}>
            <Ticket className="w-4 h-4 mr-2" />
            View Queue
          </Button>
        </div>
      </div>
      
      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Active Tickets</span>
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <AlertCircle className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{activeTickets}</div>
          </CardContent>
        </Card>
        
        <Card className="border-destructive/30 bg-destructive/5 relative overflow-hidden">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-destructive">High/Urgent Active</span>
              <div className="w-8 h-8 rounded-full bg-destructive/10 flex items-center justify-center">
                <ShieldAlert className="w-4 h-4 text-destructive" />
              </div>
            </div>
            <div className="text-3xl font-bold text-destructive tracking-tight">{urgentTickets}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Active Asset Assignments</span>
              <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                <Laptop className="w-4 h-4 text-muted-foreground" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{activeAssets}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Resolved Tickets</span>
              <div className="w-8 h-8 rounded-full bg-success/10 flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4 text-success" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{resolvedTickets}</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="flex flex-col overflow-hidden">
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Tickets by Status
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-6 flex flex-col justify-center">
            <CustomBarChart 
              data={ticketSummary} 
              xAxisKey="status" 
              bars={[{ key: "tickets", color: "#f59e0b", name: "Tickets" }]} 
            />
          </CardContent>
        </Card>
        
        <Card className="flex flex-col">
          <CardHeader className="border-b border-border/40 pb-4 flex flex-row items-center justify-between">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Recent Asset Assignments
            </CardTitle>
            <Button variant="outline" size="sm" className="h-8 text-[11px] px-3 shadow-none border-transparent hover:bg-surface-hover/80" onClick={() => router.push('/dashboard/it/assets')}>
              View All
            </Button>
          </CardHeader>
          <CardContent className="flex-1 p-0 flex flex-col">
            <div className="flex-1 overflow-auto max-h-[320px]">
              {assetAssignments.length === 0 ? (
                <div className="h-40 flex items-center justify-center text-muted-foreground text-sm">
                  No recent assignments
                </div>
              ) : (
                <table className="w-full text-sm text-left">
                  <thead className="text-[10px] font-semibold text-muted-foreground uppercase tracking-widest bg-surface-hover/30 sticky top-0">
                    <tr>
                      <th className="px-5 py-3 border-b border-border/40">Asset</th>
                      <th className="px-5 py-3 border-b border-border/40">Employee</th>
                      <th className="px-5 py-3 border-b border-border/40">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {assetAssignments.slice(0, 5).map((asset, i) => (
                      <tr key={i} className="border-b border-border/40 hover:bg-surface-hover/20 transition-colors last:border-0">
                        <td className="px-5 py-4 font-medium text-foreground">{asset.asset_name}</td>
                        <td className="px-5 py-4 text-muted-foreground">{asset.employee_name || 'N/A'}</td>
                        <td className="px-5 py-4">
                          <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
                            asset.status === 'ACTIVE' ? 'bg-success/10 text-success' : 'bg-muted text-muted-foreground'
                          }`}>
                            {asset.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Quick Links Panel */}
        <Card>
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Operations Center
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button onClick={() => router.push('/dashboard/it/tickets')} className="flex items-center p-4 rounded-xl hover:bg-surface-hover/80 border border-transparent hover:border-border/40 transition-colors group text-left">
                <div className="w-10 h-10 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors shrink-0 mr-3">
                  <Ticket className="w-4 h-4 text-primary" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-foreground">Ticket Queue</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5">Manage support requests</div>
                </div>
                <ArrowRight className="w-4 h-4 text-muted-foreground/30 group-hover:text-foreground transition-colors ml-2" />
              </button>
              
              <button onClick={() => router.push('/dashboard/it/assets')} className="flex items-center p-4 rounded-xl hover:bg-surface-hover/80 border border-transparent hover:border-border/40 transition-colors group text-left">
                <div className="w-10 h-10 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors shrink-0 mr-3">
                  <Laptop className="w-4 h-4 text-primary" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-foreground">Hardware Assets</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5">Track devices & inventory</div>
                </div>
                <ArrowRight className="w-4 h-4 text-muted-foreground/30 group-hover:text-foreground transition-colors ml-2" />
              </button>
            </div>
          </CardContent>
        </Card>
      </div>

    </div>
  );
}
