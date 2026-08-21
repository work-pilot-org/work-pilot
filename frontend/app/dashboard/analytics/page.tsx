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
import { Users, Briefcase, Ticket, Activity } from "lucide-react";

export default function AnalyticsDashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [attendance, setAttendance] = useState<any>(null);
  const [leave, setLeave] = useState<any>(null);
  const [headcount, setHeadcount] = useState<any>(null);
  const [tickets, setTickets] = useState<any>(null);
  const [assets, setAssets] = useState<any>(null);
  const [workflowPerf, setWorkflowPerf] = useState<any>(null);
  const [workflowBot, setWorkflowBot] = useState<any>(null);

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
        if (!assetRes.error) setAssets(assetRes.summary || []);
        if (!wpRes.error) setWorkflowPerf(wpRes.summary || []);
        if (!wbRes.error) setWorkflowBot(wbRes.summary || []);

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
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-6 rounded-lg text-red-600 text-center mt-6">
        {error}
      </div>
    );
  }

  // Derived KPIs
  const totalEmployees = headcount?.reduce((acc: number, curr: any) => acc + (curr.count || 0), 0) || 0;
  const activeEmployees = headcount?.find((h: any) => h.status === 'ACTIVE')?.count || 0;
  
  const totalOpenTickets = tickets?.filter((t: any) => t.status === 'OPEN' || t.status === 'IN_PROGRESS')
    .reduce((acc: number, curr: any) => acc + (curr.total_tickets || 0), 0) || 0;
    
  const totalLeaveRequests = leave?.reduce((acc: number, curr: any) => acc + (curr.requests || 0), 0) || 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Analytics Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
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

      <div className="space-y-12">
        {/* HR Section */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 border-b pb-2">HR Analytics</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-700 mb-4">Headcount by Status</h3>
              <CustomPieChart data={headcount} dataKey="count" nameKey="status" />
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-700 mb-4">Leave Utilization</h3>
              <CustomBarChart 
                data={leave} 
                xAxisKey="status" 
                bars={[{ key: "total_days", color: "#8884d8", name: "Total Days" }]} 
              />
            </div>
          </div>
        </section>

        {/* IT Section */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 border-b pb-2">IT Analytics</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-700 mb-4">Tickets by Status</h3>
              <CustomPieChart data={tickets} dataKey="total_tickets" nameKey="status" />
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-700 mb-4">Asset Assignments</h3>
              <CustomBarChart 
                data={assets} 
                xAxisKey="status" 
                bars={[{ key: "total_assets", color: "#82ca9d", name: "Total Assets" }]} 
              />
            </div>
          </div>
        </section>

        {/* Workflow Section */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 border-b pb-2">Workflow Analytics</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-700 mb-4">Workflow Performance</h3>
              <CustomBarChart 
                data={workflowPerf} 
                xAxisKey="execution_status" 
                bars={[{ key: "total_executions", color: "#ffc658", name: "Executions" }]} 
              />
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-700 mb-4">Workflow Bottlenecks</h3>
              <CustomPieChart data={workflowBot} dataKey="count" nameKey="status" />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
