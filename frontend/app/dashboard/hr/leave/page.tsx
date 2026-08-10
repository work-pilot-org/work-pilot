"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeaveRequestResponse } from "@/types/hr";
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
import { Calendar, CheckCircle, XCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function LeaveRequestsPage() {
  const [leaveRequests, setLeaveRequests] = useState<LeaveRequestResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLeaveRequests = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getLeaveRequests();
      setLeaveRequests(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave requests.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaveRequests();
  }, []);

  if (isLoading) return <LoadingState message="Loading leave requests..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchLeaveRequests} />;

  const handleStatusUpdate = async (id: string, status: "APPROVED" | "REJECTED") => {
    try {
      await hrRepository.updateLeaveRequestStatus(id, status);
      fetchLeaveRequests();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : `Failed to ${status.toLowerCase()} request`);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Leave Requests</h1>
      </div>

      {leaveRequests.length === 0 ? (
        <EmptyState 
          title="No leave requests found"
          description="There are currently no leave requests to display."
          icon={<Calendar className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee ID</TableHead>
              <TableHead>Leave Type</TableHead>
              <TableHead>Dates</TableHead>
              <TableHead>Total Days</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {leaveRequests.map((request) => (
              <TableRow key={request.id}>
                <TableCell className="font-medium text-muted-foreground">
                  {request.employee_id.split("-")[0]}...
                </TableCell>
                <TableCell>{request.leave_type.replace("_", " ")}</TableCell>
                <TableCell>
                  {request.start_date} to {request.end_date}
                </TableCell>
                <TableCell>
                  {request.total_days} {request.is_half_day ? "(Half Day)" : ""}
                </TableCell>
                <TableCell>
                  <Badge 
                    variant={
                      request.status === "APPROVED"
                        ? "success"
                        : request.status === "REJECTED" || request.status === "CANCELLED"
                        ? "destructive"
                        : "warning"
                    }
                  >
                    {request.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  {request.status === "PENDING" && (
                    <div className="flex justify-end gap-2">
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="text-green-600 border-green-200 hover:bg-green-50"
                        onClick={() => handleStatusUpdate(request.id, "APPROVED")}
                      >
                        <CheckCircle className="w-4 h-4 mr-1" />
                        Approve
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="text-red-600 border-red-200 hover:bg-red-50"
                        onClick={() => handleStatusUpdate(request.id, "REJECTED")}
                      >
                        <XCircle className="w-4 h-4 mr-1" />
                        Reject
                      </Button>
                    </div>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
