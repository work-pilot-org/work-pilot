"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { workflowRepository } from "@/repositories/workflowRepository";
import { WorkflowExecutionResponse } from "@/types/workflow";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Briefcase, ArrowLeft, Clock, CheckCircle2, AlertTriangle, Play, X, User } from "lucide-react";

export default function WorkflowDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const executionId = params.id as string;

  const [execution, setExecution] = useState<WorkflowExecutionResponse | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDetails = async () => {
    if (!executionId) return;
    try {
      setIsLoading(true);
      setError(null);
      const [execData, histData] = await Promise.all([
        workflowRepository.getWorkflowExecution(executionId),
        workflowRepository.getWorkflowHistory(executionId).catch(() => [])
      ]);
      setExecution(execData);
      setHistory(histData);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load workflow execution details.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDetails();
  }, [executionId]);

  const handleApprove = async () => {
    try {
      await workflowRepository.approveTask(executionId, { action: "APPROVE" });
      fetchDetails();
    } catch (err: any) {
      alert("Failed to process approval: " + (err.message || "Unknown error"));
    }
  };

  const handleReject = async () => {
    try {
      await workflowRepository.approveTask(executionId, { action: "REJECT" });
      fetchDetails();
    } catch (err: any) {
      alert("Failed to process rejection: " + (err.message || "Unknown error"));
    }
  };

  if (isLoading) {
    return <LoadingState message="Loading workflow details..." className="py-12" />;
  }

  if (error) {
    return (
      <div className="space-y-4 max-w-7xl mx-auto">
        <ErrorState message={error} onRetry={fetchDetails} />
        <Button variant="outline" onClick={() => router.push("/dashboard/workflows")}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Workflows
        </Button>
      </div>
    );
  }

  if (!execution) {
    return (
      <EmptyState 
        title="Workflow not found"
        description="The workflow execution record could not be found."
        icon={<Briefcase className="w-8 h-8 text-muted-foreground" />}
      />
    );
  }

  return (
    <div className="flex flex-col h-full space-y-6 max-w-5xl mx-auto pb-12">
      
      {/* Header Context */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
            <button onClick={() => router.push("/dashboard/workflows")} className="hover:text-foreground transition-colors">Workflows</button>
            <span>/</span>
            <span className="text-foreground font-medium">Execution #{execution.id.split('-')[0]}</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Briefcase className="w-6 h-6 text-primary" />
            Workflow Execution
          </h1>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant={
            execution.status === "completed" ? "success" :
            execution.status === "rejected" ? "destructive" :
            execution.status === "pending" ? "warning" : "secondary"
          } className="text-sm px-3 py-1 shadow-sm">
            {execution.status.toUpperCase()}
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Main Details */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-border bg-surface-hover/30">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Execution Context</h3>
            </div>
            <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <dt className="text-xs font-medium text-muted-foreground mb-1">Workflow ID</dt>
                <dd className="text-sm font-medium text-foreground">{execution.workflow_id}</dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-muted-foreground mb-1">Entity Reference</dt>
                <dd className="text-sm font-medium text-foreground">{execution.entity_type} ({execution.entity_id})</dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-muted-foreground mb-1">Initiator</dt>
                <dd className="text-sm font-medium text-foreground flex items-center gap-2">
                  <User className="w-3 h-3 text-muted-foreground" />
                  {execution.started_by || "System"}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-muted-foreground mb-1">Submitted On</dt>
                <dd className="text-sm font-medium text-foreground flex items-center gap-2">
                  <Clock className="w-3 h-3 text-muted-foreground" />
                  {new Date(execution.created_at).toLocaleString()}
                </dd>
              </div>
            </div>
          </div>

          <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-border bg-surface-hover/30 flex justify-between items-center">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Audit Trail</h3>
            </div>
            {history.length === 0 ? (
              <div className="p-8 text-center text-sm text-muted-foreground">
                No history recorded for this execution yet.
              </div>
            ) : (
              <div className="p-0">
                {history.map((record, index) => (
                  <div key={record.id || index} className="flex gap-4 p-4 border-b border-border last:border-0 hover:bg-surface-hover/50 transition-colors">
                    <div className="flex flex-col items-center">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                        record.status === "APPROVED" ? "bg-success/10 text-success" :
                        record.status === "REJECTED" ? "bg-destructive/10 text-destructive" :
                        "bg-muted text-muted-foreground"
                      }`}>
                        {record.status === "APPROVED" ? <CheckCircle2 className="w-4 h-4" /> :
                         record.status === "REJECTED" ? <AlertTriangle className="w-4 h-4" /> :
                         <Clock className="w-4 h-4" />}
                      </div>
                      {index !== history.length - 1 && <div className="w-px h-full bg-border my-2"></div>}
                    </div>
                    <div className="flex-1 pb-4">
                      <p className="text-sm font-semibold text-foreground">
                        {record.step_name || "Workflow Step"}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {new Date(record.created_at || 0).toLocaleString()} • {record.actor || "System"}
                      </p>
                      {record.comments && (
                        <div className="mt-2 text-sm text-muted-foreground bg-surface-hover p-3 rounded-md border border-border">
                          "{record.comments}"
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Sidebar Actions */}
        <div className="lg:col-span-1 space-y-6">
          {execution.status === "pending" && (
            <div className="bg-warning/5 border border-warning/30 rounded-xl shadow-sm p-6 space-y-4">
              <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-warning" />
                Action Required
              </h3>
              <p className="text-sm text-muted-foreground">
                This workflow is currently pending your review. Please evaluate the request and provide a decision.
              </p>
              <div className="space-y-3 pt-2">
                <Button className="w-full shadow-sm text-success border-success/30 bg-success/10 hover:bg-success/20 hover:text-success-strong" variant="outline" onClick={handleApprove}>
                  <CheckCircle2 className="w-4 h-4 mr-2" /> Approve Request
                </Button>
                <Button className="w-full shadow-sm text-destructive border-destructive/30 bg-destructive/5 hover:bg-destructive/10" variant="outline" onClick={handleReject}>
                  <X className="w-4 h-4 mr-2" /> Reject Request
                </Button>
              </div>
            </div>
          )}

          <div className="bg-surface border border-border-strong rounded-xl shadow-sm p-6 space-y-4">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Operations</h3>
            <Button variant="outline" className="w-full justify-start shadow-sm" disabled={execution.status !== 'pending'}>
              <Play className="w-4 h-4 mr-2" />
              Force Execute Step
            </Button>
            <Button variant="outline" className="w-full justify-start shadow-sm" onClick={() => router.push(`/dashboard/chat`)}>
              Ask AI about Context
            </Button>
          </div>
        </div>

      </div>
    </div>
  );
}
