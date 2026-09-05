import { useEffect, useState } from "react";
import { analyticsRepository } from "@/repositories/analyticsRepository";
import { HeadcountResponse, TicketSummaryResponse, WorkflowPerformanceResponse } from "@/types/analytics";
import { InvitationResponse } from "@/types/invitation";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Users, Ticket, Activity, Clock, Mail } from "lucide-react";
import { invitationRepository } from "@/repositories/invitationRepository";


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
  const uniqueWorkflows = new Set(workflows?.map(w => w.workflow_name)).size;

  return (
    <div className="space-y-8 mt-2">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">Organization Overview</h2>
          <p className="text-sm text-gray-500 mt-1">High-level metrics and activity across your organization.</p>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Headcount Card */}
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2.5 bg-indigo-50 rounded-lg text-indigo-600">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div>
            <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{activeHeadcount}</h3>
            <p className="text-sm font-medium text-gray-500 mt-1">Active Employees</p>
          </div>
        </div>

        {/* Invitations Card */}
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2.5 bg-purple-50 rounded-lg text-purple-600">
              <Mail className="w-5 h-5" />
            </div>
          </div>
          <div>
            <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{pendingInvites}</h3>
            <p className="text-sm font-medium text-gray-500 mt-1">Pending Invitations</p>
          </div>
        </div>

        {/* Tickets Card */}
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2.5 bg-amber-50 rounded-lg text-amber-600">
              <Ticket className="w-5 h-5" />
            </div>
          </div>
          <div>
            <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{openTickets}</h3>
            <p className="text-sm font-medium text-gray-500 mt-1">Active IT Tickets</p>
          </div>
        </div>

        {/* Workflow Success Rate Card */}
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2.5 bg-emerald-50 rounded-lg text-emerald-600">
              <Activity className="w-5 h-5" />
            </div>
          </div>
          <div>
            <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{(avgWorkflowSuccess * 100).toFixed(1)}%</h3>
            <p className="text-sm font-medium text-gray-500 mt-1">Avg Workflow Success</p>
          </div>
        </div>
      </div>

      {/* Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
         {/* Employee Distribution */}
         <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
            <div className="px-6 py-5 border-b border-gray-100">
              <h3 className="text-base font-semibold text-gray-900">Employee Distribution</h3>
            </div>
            <div className="p-6 flex-1">
              {headcount?.summary.length === 0 ? (
                <div className="h-full flex items-center justify-center text-sm text-gray-500">No data available</div>
              ) : (
                <div className="space-y-5">
                  {headcount?.summary.map((item) => {
                    const total = headcount.summary.reduce((acc, curr) => acc + curr.count, 0);
                    const percentage = total > 0 ? (item.count / total) * 100 : 0;
                    return (
                      <div key={item.status}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-gray-700 capitalize">{item.status.replace("_", " ").toLowerCase()}</span>
                          <span className="text-sm font-semibold text-gray-900">{item.count}</span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-2">
                          <div 
                            className="bg-indigo-500 h-2 rounded-full" 
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
         </div>

         {/* Workflow Performance */}
         <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
            <div className="px-6 py-5 border-b border-gray-100">
              <h3 className="text-base font-semibold text-gray-900">Workflow Performance</h3>
            </div>
            <div className="p-0 flex-1">
              {!workflows || workflows.length === 0 ? (
                <div className="p-6 h-full flex items-center justify-center text-sm text-gray-500">No workflow data available</div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {workflows.slice(0, 5).map((item, idx) => (
                    <div key={`${item.workflow_name}-${idx}`} className="p-5 flex items-center justify-between hover:bg-gray-50 transition-colors">
                      <div className="flex flex-col">
                        <span className="text-sm font-semibold text-gray-900">{item.workflow_name}</span>
                        <span className="text-xs text-gray-500 mt-1">Avg Duration: {item.avg_completion_minutes.toFixed(1)} min</span>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100">
                          {item.execution_status}
                        </span>
                        <span className="text-xs text-gray-500 mt-1.5 font-medium">{item.total_executions} executions</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
         </div>
      </div>
    </div>
  );
}
