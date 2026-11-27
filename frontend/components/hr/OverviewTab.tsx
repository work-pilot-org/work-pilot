import { useEffect, useState } from "react";
import { analyticsRepository } from "@/repositories/analyticsRepository";
import { HeadcountResponse, TicketSummaryResponse, WorkflowPerformanceResponse } from "@/types/analytics";
import { InvitationResponse } from "@/types/invitation";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Users, Ticket, Activity, Mail } from "lucide-react";
import { invitationRepository } from "@/repositories/invitationRepository";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";


export function OverviewTab({ refreshTrigger = 0 }: { refreshTrigger?: number }) {
  const [headcount, setHeadcount] = useState<HeadcountResponse | null>(null);
  const [tickets, setTickets] = useState<TicketSummaryResponse | null>(null);
  const [workflows, setWorkflows] = useState<WorkflowPerformanceResponse | null>(null);
  const [invitations, setInvitations] = useState<InvitationResponse[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const [hc, tk, wf, invs] = await Promise.all([
        analyticsRepository.getHrHeadcount().catch(() => null),
        analyticsRepository.getItTicketSummary().catch(() => null),
        analyticsRepository.getWorkflowPerformance().catch(() => null),
        invitationRepository.listInvitations().catch(() => null),
      ]);
      
      if (hc) setHeadcount(hc);
      if (tk) setTickets(tk);
      if (wf) setWorkflows(wf);
      if (invs) setInvitations(invs);
      
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load overview data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [refreshTrigger]);

  if (isLoading) {
    return <LoadingState message="Loading overview..." className="py-12" />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchAnalytics} />;
  }

  const activeHeadcount = headcount?.summary.find(s => s.status === 'ACTIVE')?.count || 0;
  const openTickets = tickets?.summary
    .filter(s => s.status === 'OPEN' || s.status === 'IN_PROGRESS')
    .reduce((acc, curr) => acc + curr.tickets, 0) || 0;
  const pendingInvites = invitations?.filter(i => i.status === 'PENDING').length || 0;
  
  const totalExecutions = workflows?.reduce((acc, curr) => acc + curr.total_executions, 0) || 0;
  const completedExecutions = workflows?.filter(w => w.execution_status === 'COMPLETED').reduce((acc, curr) => acc + curr.total_executions, 0) || 0;
  const avgWorkflowSuccess = totalExecutions > 0 ? completedExecutions / totalExecutions : 0;

  return (
    <div className="space-y-6 mt-4 pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold tracking-tight text-foreground">Organization Overview</h2>
          <p className="text-sm text-muted-foreground mt-1">High-level metrics and activity across your organization.</p>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Active Employees</span>
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Users className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{activeHeadcount}</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Pending Invitations</span>
              <div className="w-8 h-8 rounded-full bg-purple-500/10 flex items-center justify-center">
                <Mail className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{pendingInvites}</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Active IT Tickets</span>
              <div className="w-8 h-8 rounded-full bg-warning/10 flex items-center justify-center">
                <Ticket className="w-4 h-4 text-warning" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{openTickets}</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Avg Workflow Success</span>
              <div className="w-8 h-8 rounded-full bg-success/10 flex items-center justify-center">
                <Activity className="w-4 h-4 text-success" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{(avgWorkflowSuccess * 100).toFixed(1)}%</div>
          </CardContent>
        </Card>
      </div>

      {/* Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
         {/* Employee Distribution */}
         <Card className="flex flex-col">
            <CardHeader className="border-b border-border/40 pb-4">
              <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Employee Distribution</CardTitle>
            </CardHeader>
            <CardContent className="p-6 flex-1">
              {headcount?.summary.length === 0 ? (
                <div className="h-full flex items-center justify-center text-sm text-muted-foreground">No data available</div>
              ) : (
                <div className="space-y-5">
                  {headcount?.summary.map((item) => {
                    const total = headcount.summary.reduce((acc, curr) => acc + curr.count, 0);
                    const percentage = total > 0 ? (item.count / total) * 100 : 0;
                    return (
                      <div key={item.status}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-foreground capitalize">{item.status.replace("_", " ").toLowerCase()}</span>
                          <span className="text-sm font-semibold text-foreground">{item.count}</span>
                        </div>
                        <div className="w-full bg-surface-hover rounded-full h-2 overflow-hidden">
                          <div 
                            className="bg-primary h-2 rounded-full" 
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
         </Card>

         {/* Workflow Performance */}
         <Card className="flex flex-col">
            <CardHeader className="border-b border-border/40 pb-4">
              <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Workflow Performance</CardTitle>
            </CardHeader>
            <CardContent className="p-0 flex-1">
              {!workflows || workflows.length === 0 ? (
                <div className="p-6 h-full flex items-center justify-center text-sm text-muted-foreground">No workflow data available</div>
              ) : (
                <div className="divide-y divide-border/40">
                  {workflows.slice(0, 5).map((item, idx) => (
                    <div key={`${item.workflow_name}-${idx}`} className="p-5 flex items-center justify-between hover:bg-surface-hover/30 transition-colors">
                      <div className="flex flex-col">
                        <span className="text-sm font-semibold text-foreground">{item.workflow_name}</span>
                        <span className="text-xs text-muted-foreground mt-1">Avg Duration: {item.avg_completion_minutes.toFixed(1)} min</span>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-success/10 text-success">
                          {item.execution_status}
                        </span>
                        <span className="text-xs text-muted-foreground mt-1.5 font-medium">{item.total_executions} executions</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
         </Card>
      </div>
    </div>
  );
}
