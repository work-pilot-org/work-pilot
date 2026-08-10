"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { ShiftPolicyResponse } from "@/types/hr";
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
import { Briefcase } from "lucide-react";

export default function ShiftPolicyPage() {
  const [policies, setPolicies] = useState<ShiftPolicyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPolicies = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getShiftPolicies();
      setPolicies(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load shift policies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  if (isLoading) return <LoadingState message="Loading shift policies..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchPolicies} />;

  return (
    <div className="space-y-6">
      {policies.length === 0 ? (
        <EmptyState 
          title="No Shift Policies"
          description="There are currently no shift policies configured."
          icon={<Briefcase className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Shift Start</TableHead>
              <TableHead>Shift End</TableHead>
              <TableHead>Break Duration</TableHead>
              <TableHead>Weekly Off</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {policies.map((policy) => (
              <TableRow key={policy.id}>
                <TableCell className="font-bold">
                  {policy.name}
                  {policy.night_shift && (
                    <Badge variant="outline" className="ml-2 bg-blue-50 text-blue-700">Night Shift</Badge>
                  )}
                </TableCell>
                <TableCell>{policy.shift_start}</TableCell>
                <TableCell>{policy.shift_end}</TableCell>
                <TableCell>{policy.break_duration} mins</TableCell>
                <TableCell>{policy.weekly_off || "None"}</TableCell>
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
