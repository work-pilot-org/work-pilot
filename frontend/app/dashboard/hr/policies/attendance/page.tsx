"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { AttendancePolicyResponse } from "@/types/hr";
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
import { Clock } from "lucide-react";

export default function AttendancePolicyPage() {
  const [policies, setPolicies] = useState<AttendancePolicyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPolicies = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getAttendancePolicies();
      setPolicies(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load attendance policies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  if (isLoading) return <LoadingState message="Loading attendance policies..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchPolicies} />;

  return (
    <div className="space-y-6">
      {policies.length === 0 ? (
        <EmptyState 
          title="No Attendance Policies"
          description="There are currently no attendance policies configured."
          icon={<Clock className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Working Hours</TableHead>
              <TableHead>Grace Period</TableHead>
              <TableHead>Late Limit</TableHead>
              <TableHead>Half Day Rules</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {policies.map((policy) => (
              <TableRow key={policy.id}>
                <TableCell className="font-bold">
                  {policy.name}
                </TableCell>
                <TableCell>{policy.working_hours} hrs</TableCell>
                <TableCell>{policy.grace_period} mins</TableCell>
                <TableCell>{policy.late_mark_limit} times/month</TableCell>
                <TableCell>After {policy.half_day_after_hours} hrs</TableCell>
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
