"use client";

import { useEffect, useState } from "react";
import { analyticsRepository } from "@/repositories/analyticsRepository";
import { HeadcountResponse, TicketSummaryResponse, WorkflowPerformanceResponse } from "@/types/analytics";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Users, Ticket, Activity, Building2 } from "lucide-react";
import { RequireRole } from "@/components/RequireRole";

export default function OrgAnalyticsPage() {
  const [headcount, setHeadcount] = useState<HeadcountResponse | null>(null);
  const [tickets, setTickets] = useState<TicketSummaryResponse | null>(null);
  const [workflows, setWorkflows] = useState<WorkflowPerformanceResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const [hc, tk, wf] = await Promise.all([
        analyticsRepository.getHrHeadcount().catch(() => null),
        analyticsRepository.getItTicketSummary().catch(() => null),
        analyticsRepository.getWorkflowPerformance().catch(() => null),
      ]);
      
      if (hc) setHeadcount(hc);
      if (tk) setTickets(tk);
      if (wf) setWorkflows(wf);
      
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load analytics data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (isLoading) {
    return <LoadingState message="Loading organization analytics..." className="py-12" />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchAnalytics} />;
  }

  const activeHeadcount = headcount?.summary.find(s => s.status === 'ACTIVE')?.count || 0;
  const totalTickets = tickets?.summary.reduce((acc, curr) => acc + curr.tickets, 0) || 0;
  const totalExecutions = workflows?.reduce((acc, curr) => acc + curr.total_executions, 0) || 0;
  
  return (
    <RequireRole allowedRoles={["ORG_ADMIN"]}>
      <div className="space-y-8 mt-2 max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-gray-900">Organization Analytics</h2>
            <p className="text-sm text-gray-500 mt-1">Comprehensive metrics across HR, IT, and Workflows.</p>
          </div>
        </div>

        {/* High Level KPI Row */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
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
          
          <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2.5 bg-amber-50 rounded-lg text-amber-600">
                <Ticket className="w-5 h-5" />
              </div>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{totalTickets}</h3>
              <p className="text-sm font-medium text-gray-500 mt-1">Total IT Tickets</p>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2.5 bg-emerald-50 rounded-lg text-emerald-600">
                <Activity className="w-5 h-5" />
              </div>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{totalExecutions}</h3>
              <p className="text-sm font-medium text-gray-500 mt-1">Workflow Executions</p>
            </div>
          </div>
        </div>

        {/* Detailed Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Employee Status Breakdown */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
            <h3 className="text-base font-semibold text-gray-900 mb-6">Employee Status Distribution</h3>
            {headcount?.summary.length === 0 ? (
               <div className="text-sm text-gray-500">No data available</div>
            ) : (
               <div className="space-y-4">
                 {headcount?.summary.map((item) => {
                   const total = headcount.summary.reduce((acc, curr) => acc + curr.count, 0);
                   const percentage = total > 0 ? (item.count / total) * 100 : 0;
                   return (
                     <div key={item.status}>
                       <div className="flex justify-between text-sm mb-1">
                         <span className="font-medium text-gray-700 capitalize">{item.status.replace("_", " ").toLowerCase()}</span>
                         <span className="text-gray-900 font-semibold">{item.count}</span>
                       </div>
                       <div className="w-full bg-gray-100 rounded-full h-2">
                         <div className="bg-indigo-500 h-2 rounded-full" style={{ width: `${percentage}%` }}></div>
                       </div>
                     </div>
                   );
                 })}
               </div>
            )}
          </div>

          {/* IT Tickets Breakdown */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
            <h3 className="text-base font-semibold text-gray-900 mb-6">IT Ticket Status</h3>
            {tickets?.summary.length === 0 ? (
               <div className="text-sm text-gray-500">No ticket data available</div>
            ) : (
               <div className="space-y-4">
                 {tickets?.summary.map((item) => {
                   const percentage = totalTickets > 0 ? (item.tickets / totalTickets) * 100 : 0;
                   return (
                     <div key={item.status}>
                       <div className="flex justify-between text-sm mb-1">
                         <span className="font-medium text-gray-700 capitalize">{item.status.replace("_", " ").toLowerCase()}</span>
                         <span className="text-gray-900 font-semibold">{item.tickets}</span>
                       </div>
                       <div className="w-full bg-gray-100 rounded-full h-2">
                         <div className="bg-amber-500 h-2 rounded-full" style={{ width: `${percentage}%` }}></div>
                       </div>
                     </div>
                   );
                 })}
               </div>
            )}
          </div>
        </div>

      </div>
    </RequireRole>
  );
}
