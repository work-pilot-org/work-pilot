"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { ProbationPolicyResponse } from "@/types/hr";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { UserCheck } from "lucide-react";

export default function ProbationPolicyPage() {
  const [policies, setPolicies] = useState<ProbationPolicyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPolicies = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getProbationPolicies();
      setPolicies(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load probation policies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  if (isLoading) return <LoadingState message="Loading probation policies..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchPolicies} />;

  return (
    <div className="space-y-6">
      {policies.length === 0 ? (
        <EmptyState 
          title="No Probation Policies"
          description="There are currently no probation policies configured."
          icon={<UserCheck className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Duration</TableHead>
              <TableHead>Review Period</TableHead>
              <TableHead>Notice Period</TableHead>
              <TableHead>Confirmation</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {policies.map((policy) => (
              <TableRow key={policy.id}>
                <TableCell className="font-bold">{policy.name}</TableCell>
                <TableCell>{policy.duration_months} months</TableCell>
                <TableCell>After {policy.review_after_months} months</TableCell>
                <TableCell>{policy.notice_period} days</TableCell>
                <TableCell>
                  {policy.confirmation_required ? (
                    <span className="text-blue-600 font-medium">Required</span>
                  ) : (
                    <span className="text-muted-foreground">Automatic</span>
                  )}
                </TableCell>
                <TableCell>
                  <Badge variant={policy.is_active ? "success" : "secondary"}>
                    {policy.is_active ? "Active" : "Inactive"}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
