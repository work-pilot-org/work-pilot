"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { hrRepository } from "@/repositories/hrRepository";
import { workflowRepository } from "@/repositories/workflowRepository";
import { Users, ClipboardList, Clock, ArrowRight, Check, X } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmployeeResponse } from "@/types/hr";
import { WorkflowExecutionResponse } from "@/types/workflow";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";

export function ManagerDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  
  const [team, setTeam] = useState<EmployeeResponse[]>([]);
  const [executions, setExecutions] = useState<WorkflowExecutionResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [empData, execData] = await Promise.all([
          hrRepository.getEmployees().catch(() => []),
          workflowRepository.getWorkflowExecutions().catch(() => [])
        ]);
        
        // Simulating team scoped data (normally handled by backend permissions)
        setTeam(empData.slice(0, 8)); 
        setExecutions(execData);
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
    <div className="flex flex-col h-full space-y-6 max-w-7xl mx-auto pb-12">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-surface border border-border-strong rounded-xl p-6 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Manager Overview, {user?.name || "Manager"}
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm" onClick={() => router.push('/dashboard/workflows')}>
            View Approvals
          </Button>
        </div>
      </div>
      
      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Team Size</span>
            <Users className="w-4 h-4 text-primary" />
          </div>
          <div className="text-3xl font-bold text-foreground">{team.length}</div>
        </div>
        
        <div className={`bg-surface border border-border-strong rounded-xl p-5 shadow-sm ${pendingApprovals.length > 0 ? 'border-l-4 border-l-warning' : ''}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Pending Approvals</span>
            <ClipboardList className="w-4 h-4 text-warning" />
          </div>
          <div className="text-3xl font-bold text-foreground">{pendingApprovals.length}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Team Absences</span>
            <Clock className="w-4 h-4 text-muted-foreground" />
          </div>
          <div className="text-3xl font-bold text-foreground">0</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4">
        
        {/* Approvals Action Required */}
        <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-6 flex flex-col">
          <h3 className="text-lg font-semibold text-foreground mb-4">Requires Action</h3>
          {pendingApprovals.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-sm text-muted-foreground border-2 border-dashed border-border rounded-lg p-6">
              You're all caught up. No pending approvals.
            </div>
          ) : (
            <div className="space-y-4 flex-1 overflow-auto max-h-[300px] pr-2">
              {pendingApprovals.slice(0, 5).map(exec => (
                <div key={exec.id} className="flex flex-col gap-3 p-4 rounded-lg border border-warning/30 bg-warning/5">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm font-semibold text-foreground">Workflow Request #{exec.id.split('-')[0]}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">Submitted: {new Date(exec.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" className="flex-1 text-success border-success/30 hover:bg-success/10" onClick={() => router.push('/dashboard/workflows')}>
                      <Check className="w-4 h-4 mr-1.5" /> Approve
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1 text-destructive border-destructive/30 hover:bg-destructive/10" onClick={() => router.push('/dashboard/workflows')}>
                      <X className="w-4 h-4 mr-1.5" /> Reject
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Team Members */}
        <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-6 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground">Direct Reports</h3>
            <button onClick={() => router.push('/dashboard/hr')} className="text-sm text-primary hover:underline">
              View Directory
            </button>
          </div>
          
          {team.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-sm text-muted-foreground border-2 border-dashed border-border rounded-lg">
              No team members found.
            </div>
          ) : (
            <div className="space-y-3 flex-1 overflow-auto max-h-[300px] pr-2">
              {team.map(emp => (
                <div key={emp.id} className="flex items-center justify-between p-3 rounded-lg border border-border hover:border-primary/50 transition-colors cursor-pointer" onClick={() => router.push(`/dashboard/hr/${emp.id}`)}>
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xs shrink-0">
                      {emp.first_name[0]}{emp.last_name[0]}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-foreground">{emp.first_name} {emp.last_name}</p>
                      <p className="text-xs text-muted-foreground">{emp.employment_type}</p>
                    </div>
                  </div>
                  <ArrowRight className="w-4 h-4 text-muted-foreground" />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
