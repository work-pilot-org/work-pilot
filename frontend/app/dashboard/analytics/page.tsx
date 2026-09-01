"use client";

import React, { useEffect, useState } from "react";
import {
  getAttendanceSummary,
  getLeaveUtilization,
  getHeadcount,
  getTicketSummary,
  getAssetAssignments,
  getWorkflowPerformance,
  getWorkflowBottlenecks,
} from "@/lib/api/analytics";
import { MetricCard } from "@/components/analytics/MetricCard";
import { CustomBarChart, CustomPieChart } from "@/components/analytics/AnalyticsCharts";
import { Users, Briefcase, Ticket, Activity, PieChart, BarChart3, AlertCircle } from "lucide-react";
import { RequireRole } from "@/components/RequireRole";

type TabType = "OVERVIEW" | "HR" | "IT" | "WORKFLOWS";

export default function AnalyticsDashboard() {
  const [activeTab, setActiveTab] = useState<TabType>("OVERVIEW");
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [attendance, setAttendance] = useState<any[]>([]);
  const [leave, setLeave] = useState<any[]>([]);
  const [headcount, setHeadcount] = useState<any[]>([]);
  const [tickets, setTickets] = useState<any[]>([]);
  const [assets, setAssets] = useState<any[]>([]);
  const [workflowPerf, setWorkflowPerf] = useState<any[]>([]);
  const [workflowBot, setWorkflowBot] = useState<any[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        setError(null);

        const [
          attRes,
          leaveRes,
          hcRes,
          ticketRes,
          assetRes,
          wpRes,
          wbRes
        ] = await Promise.all([
          getAttendanceSummary().catch(e => ({ error: true })),
          getLeaveUtilization().catch(e => ({ error: true })),
          getHeadcount().catch(e => ({ error: true })),
          getTicketSummary().catch(e => ({ error: true })),
          getAssetAssignments().catch(e => ({ error: true })),
          getWorkflowPerformance().catch(e => ({ error: true })),
          getWorkflowBottlenecks().catch(e => ({ error: true })),
        ]);

        if (!attRes.error) setAttendance(attRes.summary || []);
        if (!leaveRes.error) setLeave(leaveRes.summary || []);
        if (!hcRes.error) setHeadcount(hcRes.summary || []);
        if (!ticketRes.error) setTickets(ticketRes.summary || []);
        if (!assetRes.error) setAssets(assetRes.assignments || []);
        if (!wpRes.error) setWorkflowPerf(wpRes.summary || wpRes || []);
        if (!wbRes.error) setWorkflowBot(wbRes.summary || wbRes || []);

      } catch (err: any) {
        console.error(err);
        setError("Failed to load analytics data. Ensure you have the right permissions.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[500px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  // Derived KPIs
  const totalEmployees = headcount?.reduce((acc: number, curr: any) => acc + (curr.count || 0), 0) || 0;
  const activeEmployees = headcount?.find((h: any) => h.status === 'ACTIVE')?.count || 0;
  
  const totalOpenTickets = tickets?.filter((t: any) => t.status === 'OPEN' || t.status === 'IN_PROGRESS')
    .reduce((acc: number, curr: any) => acc + (curr.tickets || 0), 0) || 0;
    
  const totalLeaveRequests = leave?.reduce((acc: number, curr: any) => acc + (curr.requests || 0), 0) || 0;

  return (
    <RequireRole allowedRoles={["TENANT_ADMIN"]}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-full flex flex-col space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Organization Analytics</h1>
          <p className="text-muted-foreground mt-1">Monitor key metrics across HR, IT, and automated workflows.</p>
        </div>

        {error && (
          <div className="bg-destructive/10 p-4 rounded-lg text-destructive text-sm flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex border-b border-border overflow-x-auto">
          {(["OVERVIEW", "HR", "IT", "WORKFLOWS"] as TabType[]).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex items-center px-4 py-3 border-b-2 font-medium text-sm transition-colors whitespace-nowrap ${
                activeTab === tab 
                  ? "border-primary text-primary" 
                  : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
              }`}
            >
              {tab === "OVERVIEW" && <PieChart className="w-4 h-4 mr-2" />}
              {tab === "HR" && <Users className="w-4 h-4 mr-2" />}
              {tab === "IT" && <Ticket className="w-4 h-4 mr-2" />}
              {tab === "WORKFLOWS" && <Activity className="w-4 h-4 mr-2" />}
              {tab.charAt(0) + tab.slice(1).toLowerCase()}
            </button>
          ))}
        </div>

        <div className="flex-1">
          {activeTab === "OVERVIEW" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard 
                  title="Total Headcount" 
                  value={totalEmployees} 
                  subtitle={`${activeEmployees} Active Employees`}
                  icon={<Users className="h-6 w-6" />} 
                />
                <MetricCard 
                  title="Leave Requests" 
                  value={totalLeaveRequests} 
                  icon={<Briefcase className="h-6 w-6" />} 
                />
                <MetricCard 
                  title="Open IT Tickets" 
                  value={totalOpenTickets} 
                  icon={<Ticket className="h-6 w-6" />} 
                />
                <MetricCard 
                  title="Active Workflows" 
                  value={workflowPerf?.length || 0} 
                  icon={<Activity className="h-6 w-6" />} 
                />
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Headcount Distribution</h3>
                  <CustomPieChart data={headcount} dataKey="count" nameKey="status" />
                </div>
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Workflow Executions</h3>
                  <CustomBarChart 
                    data={workflowPerf} 
                    xAxisKey="workflow_name" 
                    bars={[{ key: "total_executions", color: "#6366f1", name: "Executions" }]} 
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === "HR" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Attendance Summary</h3>
                  <CustomBarChart 
                    data={attendance} 
                    xAxisKey="status" 
                    bars={[{ key: "worked_hours", color: "#10b981", name: "Worked Hours" }]} 
                  />
                </div>
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Leave Utilization</h3>
                  <CustomPieChart data={leave} dataKey="requests" nameKey="status" />
                </div>
              </div>
            </div>
          )}

          {activeTab === "IT" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Tickets by Priority & Status</h3>
                  <CustomBarChart 
                    data={tickets} 
                    xAxisKey="status" 
                    bars={[{ key: "tickets", color: "#f59e0b", name: "Tickets" }]} 
                  />
                </div>
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm flex flex-col">
                  <h3 className="text-lg font-medium text-foreground mb-4">Recent Asset Assignments</h3>
                  <div className="flex-1 overflow-auto max-h-[300px]">
                    {assets.length === 0 ? (
                      <div className="h-full flex items-center justify-center text-muted-foreground text-sm">No recent assignments</div>
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
                          {assets.slice(0, 5).map((asset, i) => (
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
            </div>
          )}

          {activeTab === "WORKFLOWS" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Execution Time (Avg Min)</h3>
                  <CustomBarChart 
                    data={workflowPerf} 
                    xAxisKey="workflow_name" 
                    bars={[{ key: "avg_completion_minutes", color: "#8b5cf6", name: "Avg Minutes" }]} 
                  />
                </div>
                <div className="bg-surface p-6 rounded-xl border border-border shadow-sm">
                  <h3 className="text-lg font-medium text-foreground mb-4">Workflow Bottlenecks (Avg Duration)</h3>
                  <CustomBarChart 
                    data={workflowBot} 
                    xAxisKey="entity_type" 
                    bars={[{ key: "avg_duration_minutes", color: "#ef4444", name: "Duration (Min)" }]} 
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </RequireRole>
  );
}
