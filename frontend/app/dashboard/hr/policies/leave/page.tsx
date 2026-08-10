"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeavePolicyResponse } from "@/types/hr";
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
import { CalendarHeart } from "lucide-react";

export default function LeavePolicyPage() {
  const [policies, setPolicies] = useState<LeavePolicyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPolicies = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getLeavePolicies();
      setPolicies(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave policies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  if (isLoading) return <LoadingState message="Loading leave policies..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchPolicies} />;

  return (
    <div className="space-y-6">
      {policies.length === 0 ? (
        <EmptyState 
          title="No Leave Policies"
          description="There are currently no leave policies configured."
          icon={<CalendarHeart className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Casual / Sick / Earned</TableHead>
              <TableHead>Carry Forward</TableHead>
              <TableHead>Notice Days</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {policies.map((policy) => (
              <TableRow key={policy.id}>
                <TableCell className="font-bold">
                  {policy.name}
                  {policy.description && (
                    <span className="block text-xs text-muted-foreground font-normal mt-1">
                      {policy.description}
                    </span>
                  )}
                </TableCell>
                <TableCell>
                  {policy.casual_leave_days} / {policy.sick_leave_days} / {policy.earned_leave_days}
                </TableCell>
                <TableCell>
                  {policy.carry_forward_enabled ? (
                    <span className="text-green-600 font-medium">Yes (Max: {policy.max_carry_forward})</span>
                  ) : (
                    <span className="text-muted-foreground">No</span>
                  )}
                </TableCell>
                <TableCell>{policy.minimum_notice_days}</TableCell>
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
