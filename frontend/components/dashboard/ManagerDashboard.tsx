"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { hrRepository } from "@/repositories/hrRepository";
import { workflowRepository } from "@/repositories/workflowRepository";
import { Users, ClipboardList, Clock, ArrowRight, Check, X, Activity, UserCircle2 } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmployeeResponse } from "@/types/hr";
import { WorkflowExecutionResponse } from "@/types/workflow";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { getWorkflowPerformance } from "@/lib/api/analytics";
import { CustomBarChart } from "@/components/analytics/AnalyticsCharts";

export function ManagerDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  
  const [team, setTeam] = useState<EmployeeResponse[]>([]);
  const [executions, setExecutions] = useState<WorkflowExecutionResponse[]>([]);
  const [workflowPerformance, setWorkflowPerformance] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [empData, execData, perfData] = await Promise.all([
          hrRepository.getEmployees().catch(() => []),
          workflowRepository.getWorkflowExecutions().catch(() => []),
          getWorkflowPerformance().catch(() => ({ summary: [] }))
        ]);
        
        // Simulating team scoped data (normally handled by backend permissions)
        setTeam(empData.slice(0, 8)); 
        setExecutions(execData);
        setWorkflowPerformance(perfData.summary || perfData || []);
      } catch (err: unknown) {
        setError("Failed to load Manager dashboard data.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading Manager Overview..." className="py-20" />;
  if (error) return <ErrorState message={error} />;

  const pendingApprovals = executions.filter(e => e.status === "pending");

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto w-full pb-12">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-2">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Manager Overview
          </h1>
          <p className="text-sm font-medium text-muted-foreground mt-1">
            Welcome back, {user?.name || "Manager"} • {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="primary" onClick={() => router.push('/dashboard/workflows')}>
            View Approvals
          </Button>
        </div>
      </div>
      
      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Team Size</span>
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Users className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{team.length}</div>
          </CardContent>
        </Card>
        
        <Card className={pendingApprovals.length > 0 ? "border-warning/30 bg-warning/5 relative overflow-hidden" : ""}>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className={`text-[11px] font-bold uppercase tracking-widest ${pendingApprovals.length > 0 ? 'text-warning' : 'text-muted-foreground'}`}>
                Pending Approvals
              </span>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${pendingApprovals.length > 0 ? 'bg-warning/10' : 'bg-muted'}`}>
                <ClipboardList className={`w-4 h-4 ${pendingApprovals.length > 0 ? 'text-warning' : 'text-muted-foreground'}`} />
              </div>
            </div>
            <div className={`text-3xl font-bold tracking-tight ${pendingApprovals.length > 0 ? 'text-warning' : 'text-foreground'}`}>
              {pendingApprovals.length}
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Workflow Executions</span>
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Activity className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{workflowPerformance.reduce((a, b) => a + (b.total_executions || 0), 0)}</div>
          </CardContent>
        </Card>

        <Card className="opacity-70 bg-surface/50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Team Absences</span>
              <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                <Clock className="w-4 h-4 text-muted-foreground" />
              </div>
            </div>
            <div className="text-3xl font-bold text-muted-foreground tracking-tight">0</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pt-4">
        
        {/* Approvals Action Required */}
        <Card className="flex flex-col overflow-hidden">
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Requires Action
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-0 flex flex-col">
            {pendingApprovals.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center p-12 text-center bg-surface-hover/20">
                <ClipboardList className="w-8 h-8 text-muted-foreground/40 mb-4" />
                <p className="text-sm font-semibold text-foreground">You're all caught up</p>
                <p className="text-[13px] text-muted-foreground mt-1">No pending approvals require your attention.</p>
              </div>
            ) : (
              <div className="flex-1 overflow-auto max-h-[350px]">
                {pendingApprovals.slice(0, 5).map(exec => (
                  <div key={exec.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-5 border-b border-border/40 hover:bg-surface-hover/30 transition-colors last:border-0 gap-4">
                    <div>
                      <p className="text-sm font-semibold text-foreground">Workflow Request #{exec.id.split('-')[0]}</p>
                      <p className="text-xs text-muted-foreground mt-1">Submitted: {new Date(exec.created_at).toLocaleDateString()}</p>
                    </div>
                    <div className="flex items-center gap-2 w-full sm:w-auto">
                      <Button variant="outline" size="sm" className="flex-1 sm:flex-none text-[11px] px-3 border-border hover:bg-success/10 hover:text-success hover:border-success/30" onClick={() => router.push('/dashboard/workflows')}>
                        <Check className="w-3.5 h-3.5 mr-1.5" /> Approve
                      </Button>
                      <Button variant="outline" size="sm" className="flex-1 sm:flex-none text-[11px] px-3 border-border hover:bg-destructive/10 hover:text-destructive hover:border-destructive/30" onClick={() => router.push('/dashboard/workflows')}>
                        <X className="w-3.5 h-3.5 mr-1.5" /> Reject
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Team Members */}
        <Card className="flex flex-col">
          <CardHeader className="border-b border-border/40 pb-4 flex flex-row items-center justify-between">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Direct Reports
            </CardTitle>
            <Button variant="outline" size="sm" className="h-8 text-[11px] px-3 shadow-none border-transparent hover:bg-surface-hover/80" onClick={() => router.push('/dashboard/hr')}>
              View Directory
            </Button>
          </CardHeader>
          <CardContent className="flex-1 p-0 flex flex-col">
            {team.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center p-12 text-center bg-surface-hover/20">
                <UserCircle2 className="w-8 h-8 text-muted-foreground/40 mb-4" />
                <p className="text-sm font-semibold text-foreground">No team members</p>
              </div>
            ) : (
              <div className="flex-1 overflow-auto max-h-[350px]">
                {team.map(emp => (
                  <div key={emp.id} className="flex items-center justify-between p-4 border-b border-border/40 hover:bg-surface-hover/40 transition-colors cursor-pointer last:border-0 group" onClick={() => router.push(`/dashboard/hr/${emp.id}`)}>
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-primary/5 text-primary flex items-center justify-center font-bold text-xs shrink-0 group-hover:bg-primary/10 transition-colors">
                        {emp.first_name[0]}{emp.last_name[0]}
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-foreground">{emp.first_name} {emp.last_name}</p>
                        <p className="text-xs text-muted-foreground mt-0.5">{emp.employment_type}</p>
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground/40 group-hover:text-foreground transition-colors" />
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      
      {/* Team Analytics */}
      <div className="grid grid-cols-1 gap-8">
        <Card className="flex flex-col overflow-hidden">
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Team Workflow Performance
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-6">
            <CustomBarChart 
              data={workflowPerformance} 
              xAxisKey="workflow_name" 
              bars={[{ key: "avg_completion_minutes", color: "#6366f1", name: "Avg Time (Min)" }]} 
            />
          </CardContent>
        </Card>
      </div>

    </div>
  );
}
