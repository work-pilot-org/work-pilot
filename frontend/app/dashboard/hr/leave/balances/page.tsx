"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeaveBalanceResponse } from "@/types/hr";
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
import { Scale } from "lucide-react";

export default function LeaveBalancesPage() {
  const [balances, setBalances] = useState<LeaveBalanceResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBalances = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getLeaveBalances();
      setBalances(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave balances.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBalances();
  }, []);

  if (isLoading) return <LoadingState message="Loading leave balances..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchBalances} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Leave Balances</h1>
      </div>

      {balances.length === 0 ? (
        <EmptyState 
          title="No leave balances found"
          description="There are currently no leave balances to display."
          icon={<Scale className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee ID</TableHead>
              <TableHead>Leave Type</TableHead>
              <TableHead>Year</TableHead>
              <TableHead>Allocated Days</TableHead>
              <TableHead>Used Days</TableHead>
              <TableHead>Carried Forward</TableHead>
              <TableHead>Remaining Days</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {balances.map((balance) => (
              <TableRow key={balance.id}>
                <TableCell className="font-medium text-muted-foreground">
                  {balance.employee_id.split("-")[0]}...
                </TableCell>
                <TableCell>{balance.leave_type.replace("_", " ")}</TableCell>
                <TableCell>{balance.year}</TableCell>
                <TableCell>{balance.allocated_days}</TableCell>
                <TableCell>{balance.used_days}</TableCell>
                <TableCell>{balance.carried_forward_days}</TableCell>
                <TableCell className="font-bold text-primary">{balance.remaining_days}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
