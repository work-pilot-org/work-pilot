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
    <div className="space-y-6 mt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold tracking-tight text-gray-900">Organization Overview</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Headcount Card */}
        <div className="bg-white border rounded-lg p-6 shadow-sm flex flex-col justify-center">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-indigo-100 rounded-full text-indigo-600">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Active Employees</p>
              <h3 className="text-2xl font-bold text-gray-900">{activeHeadcount}</h3>
            </div>
          </div>
        </div>

        {/* Invitations Card */}
        <div className="bg-white border rounded-lg p-6 shadow-sm flex flex-col justify-center">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 rounded-full text-purple-600">
              <Mail className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Pending Invites</p>
              <h3 className="text-2xl font-bold text-gray-900">{pendingInvites}</h3>
            </div>
          </div>
        </div>

        {/* Tickets Card */}
        <div className="bg-white border rounded-lg p-6 shadow-sm flex flex-col justify-center">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-amber-100 rounded-full text-amber-600">
              <Ticket className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Active IT Tickets</p>
              <h3 className="text-2xl font-bold text-gray-900">{openTickets}</h3>
            </div>
          </div>
        </div>

        {/* Workflow Success Rate Card */}
        <div className="bg-white border rounded-lg p-6 shadow-sm flex flex-col justify-center">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-emerald-100 rounded-full text-emerald-600">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Avg Workflow Success</p>
              <h3 className="text-2xl font-bold text-gray-900">{(avgWorkflowSuccess * 100).toFixed(1)}%</h3>
            </div>
          </div>
        </div>

        {/* Workflow Executions Card */}
        <div className="bg-white border rounded-lg p-6 shadow-sm flex flex-col justify-center">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 rounded-full text-blue-600">
              <Clock className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Active Workflows</p>
              <h3 className="text-2xl font-bold text-gray-900">{uniqueWorkflows} Types</h3>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
         <div className="bg-white border rounded-lg p-6 shadow-sm">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Headcount by Status</h3>
            {headcount?.summary.length === 0 ? (
              <p className="text-sm text-gray-500">No data available.</p>
            ) : (
              <div className="space-y-4">
                {headcount?.summary.map((item) => (
                  <div key={item.status} className="flex justify-between items-center border-b pb-2">
                    <span className="text-sm font-medium text-gray-700 capitalize">{item.status.replace("_", " ").toLowerCase()}</span>
                    <span className="text-sm font-bold text-gray-900">{item.count}</span>
                  </div>
                ))}
              </div>
            )}
         </div>

         <div className="bg-white border rounded-lg p-6 shadow-sm">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Workflow Performance</h3>
            {!workflows || workflows.length === 0 ? (
              <p className="text-sm text-gray-500">No data available.</p>
            ) : (
              <div className="space-y-4 max-h-[300px] overflow-y-auto pr-2">
                {workflows.map((item, idx) => (
                  <div key={`${item.workflow_name}-${idx}`} className="flex flex-col border-b pb-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-900">{item.workflow_name}</span>
                      <span className="text-xs font-semibold text-emerald-600">{item.execution_status}</span>
                    </div>
                    <div className="flex justify-between items-center">
                       <span className="text-xs text-gray-500">Executions: {item.total_executions}</span>
                       <span className="text-xs text-gray-500">Avg Duration: {item.avg_completion_minutes.toFixed(1)} min</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
         </div>
      </div>



    </div>
  );
}
