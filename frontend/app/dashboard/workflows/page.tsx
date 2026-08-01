"use client";

import { useEffect, useState } from "react";
import { workflowRepository } from "@/repositories/workflowRepository";
import { WorkflowResponse } from "@/types/workflow";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { WorkflowIcon } from "lucide-react";

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<WorkflowResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWorkflows = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await workflowRepository.getWorkflows();
      setWorkflows(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load workflows.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkflows();
  }, []);

  if (isLoading) return <LoadingState message="Loading workflows..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchWorkflows} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Workflows</h1>
      </div>

      {workflows.length === 0 ? (
        <EmptyState 
          title="No workflows found"
          description="There are no active workflows to display."
          icon={<WorkflowIcon className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Workflow ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Created At</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {workflows.map((workflow) => (
              <TableRow key={workflow.id}>
                <TableCell className="font-medium text-muted-foreground">
                  {workflow.id}
                </TableCell>
                <TableCell>{workflow.name}</TableCell>
                <TableCell>{workflow.is_active ? 'Active' : 'Inactive'}</TableCell>
                <TableCell>{new Date(workflow.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
