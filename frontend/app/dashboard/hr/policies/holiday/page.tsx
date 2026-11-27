"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { HolidayPolicyResponse } from "@/types/hr";
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
import { CalendarDays } from "lucide-react";

export default function HolidayPolicyPage() {
  const [policies, setPolicies] = useState<HolidayPolicyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPolicies = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getHolidayPolicies();
      setPolicies(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load holiday policies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  if (isLoading) return <LoadingState message="Loading holiday policies..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchPolicies} />;

  return (
    <div className="space-y-6">
      {policies.length === 0 ? (
        <EmptyState 
          title="No Holiday Policies"
          description="There are currently no holiday policies configured."
          icon={<CalendarDays className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Calendar Name</TableHead>
              <TableHead>Country / State</TableHead>
              <TableHead>Floating Holidays</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {policies.map((policy) => (
              <TableRow key={policy.id}>
                <TableCell className="font-bold">{policy.name}</TableCell>
                <TableCell>{policy.calendar_name}</TableCell>
                <TableCell>
                  {policy.country}
                  {policy.state && <span className="text-muted-foreground ml-1">({policy.state})</span>}
                </TableCell>
                <TableCell>{policy.floating_holidays}</TableCell>
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
