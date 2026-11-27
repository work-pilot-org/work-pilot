"use client";

import { useEffect, useState } from "react";
import { workflowRepository } from "@/repositories/workflowRepository";
import { WorkflowResponse, WorkflowExecutionResponse } from "@/types/workflow";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { CheckCircle, Clock, Check, X, ArrowRight, PlayCircle, Briefcase } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Drawer } from "@/components/ui/Drawer";

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<WorkflowResponse[]>([]);
  const [executions, setExecutions] = useState<WorkflowExecutionResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedExecution, setSelectedExecution] = useState<WorkflowExecutionResponse | null>(null);
  
  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [wfs, execs] = await Promise.all([
        workflowRepository.getWorkflows(),
        workflowRepository.getWorkflowExecutions().catch(() => []) // Fallback in case of error
      ]);
      setWorkflows(wfs);
      setExecutions(execs);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load workflow data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleApprove = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await workflowRepository.approveTask(id, { action: "APPROVE" });
      fetchData();
    } catch (error) {
      alert("Failed to process approval");
    }
  };
  
  const handleReject = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await workflowRepository.approveTask(id, { action: "REJECT" });
      fetchData();
    } catch (error) {
      alert("Failed to process rejection");
    }
  };

  if (isLoading) return <LoadingState message="Loading your action items..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;

  // Derived state
  const pendingExecutions = executions.filter(e => e.status === "pending");
  const completedExecutions = executions.filter(e => e.status === "completed" || e.status === "rejected" || e.status === "cancelled");

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Workflows & Approvals</h1>
          <p className="text-muted-foreground mt-1 text-sm">Review pending requests and monitor automated processes.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm">
            <PlayCircle className="mr-2 h-4 w-4" />
            Start Workflow
          </Button>
        </div>
      </div>

      {/* Action Required Area */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
          <Clock className="w-5 h-5 text-warning" />
          Pending Approvals
        </h2>
        
        {pendingExecutions.length === 0 ? (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-12">
            <EmptyState 
              title="You're all caught up"
              description="There are no workflow tasks requiring your immediate attention."
              icon={<CheckCircle className="w-8 h-8 text-success" />}
            />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {pendingExecutions.map(exec => (
              <div 
                key={exec.id} 
                onClick={() => setSelectedExecution(exec)}
                className="bg-surface border border-warning/30 rounded-xl p-5 shadow-sm ring-1 ring-warning/20 cursor-pointer hover:border-warning/60 transition-colors group"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider block mb-1">
                      {workflows.find(w => w.id === exec.workflow_id)?.name || "Unknown Workflow"}
                    </span>
                    <h3 className="text-sm font-semibold text-foreground line-clamp-2">
                      Execution #{exec.id.split("-")[0]}
                    </h3>
                  </div>
                  <Badge variant="warning" className="ml-2 shrink-0 bg-warning/10 text-warning border-transparent">Requires Action</Badge>
                </div>
                
                <div className="flex items-center gap-2 text-xs text-muted-foreground mb-5">
                  <Clock className="w-3 h-3" />
                  Started {new Date(exec.created_at).toLocaleDateString()}
                </div>

                <div className="flex items-center gap-2 mt-auto">
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="flex-1 text-success border-success/30 hover:bg-success/10"
                    onClick={(e) => handleApprove(exec.id, e)}
                  >
                    <Check className="w-4 h-4 mr-1.5" />
                    Approve
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="flex-1 text-destructive border-destructive/30 hover:bg-destructive/10"
                    onClick={(e) => handleReject(exec.id, e)}
                  >
                    <X className="w-4 h-4 mr-1.5" />
                    Reject
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Workflow History / Active Definitions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-4">
        
        {/* Left Col: Executions History */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-lg font-semibold text-foreground">Recent Activity</h2>
          {completedExecutions.length === 0 ? (
            <div className="bg-surface rounded-xl border border-border shadow-sm p-8 text-center text-muted-foreground text-sm">
              No recent workflow executions found.
            </div>
          ) : (
            <div className="bg-surface rounded-xl border border-border-strong shadow-sm divide-y divide-border overflow-hidden">
              {completedExecutions.slice(0, 5).map(exec => (
                <div key={exec.id} onClick={() => setSelectedExecution(exec)} className="p-4 flex items-center justify-between hover:bg-surface-hover cursor-pointer transition-colors group">
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                      exec.status === "completed" ? "bg-success/10 text-success" :
                      exec.status === "rejected" ? "bg-destructive/10 text-destructive" :
                      "bg-muted text-muted-foreground"
                    }`}>
                      <Briefcase className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                        {workflows.find(w => w.id === exec.workflow_id)?.name || `Execution ${exec.id.split("-")[0]}`}
                      </h4>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        Started on {exec.created_at ? new Date(exec.created_at).toLocaleDateString() : "N/A"}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant={
                      exec.status === "completed" ? "success" : 
                      exec.status === "rejected" ? "destructive" : 
                      "secondary"
                    }>
                      {exec.status}
                    </Badge>
                    <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Col: Available Workflows */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-foreground">Available Workflows</h2>
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-4 space-y-2">
            {workflows.map(wf => (
              <div key={wf.id} className="p-3 rounded-lg border border-border bg-surface-hover/50 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-medium text-foreground">{wf.name}</h4>
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider block mt-0.5">
                    {wf.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <Button variant="outline" size="sm" className="h-8 shadow-none" disabled={!wf.is_active}>
                  Start
                </Button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Execution Details Drawer */}
      <Drawer
        isOpen={!!selectedExecution}
        onClose={() => setSelectedExecution(null)}
        title="Workflow Details"
        description={`Execution #${selectedExecution?.id.split("-")[0]}`}
      >
        {selectedExecution && (
          <div className="space-y-6 py-4">
            <div className="bg-muted/30 p-4 rounded-xl border border-border">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="block text-xs font-medium text-muted-foreground mb-1">Status</span>
                  <Badge variant={
                    selectedExecution.status === "completed" ? "success" :
                    selectedExecution.status === "rejected" ? "destructive" :
                    selectedExecution.status === "pending" ? "warning" :
                    "secondary"
                  }>
                    {selectedExecution.status}
                  </Badge>
                </div>
                <div>
                  <span className="block text-xs font-medium text-muted-foreground mb-1">Workflow Type</span>
                  <span className="text-sm font-medium text-foreground">
                    {workflows.find(w => w.id === selectedExecution.workflow_id)?.name || selectedExecution.workflow_id}
                  </span>
                </div>
              </div>
            </div>

            {selectedExecution.status === "pending" && (
              <div className="pt-4 border-t border-border">
                <h4 className="text-sm font-semibold text-foreground mb-4">Required Actions</h4>
                <div className="flex gap-3">
                  <Button className="flex-1" onClick={(e) => handleApprove(selectedExecution.id, e as any)}>
                    Approve Request
                  </Button>
                  <Button variant="outline" className="flex-1 text-destructive hover:bg-destructive/5 border-destructive/20" onClick={(e) => handleReject(selectedExecution.id, e as any)}>
                    Reject
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </Drawer>
    </div>
  );
}
