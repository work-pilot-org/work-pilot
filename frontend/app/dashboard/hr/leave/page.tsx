"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeaveRequestResponse, OrganizationLeaveReportResponse } from "@/types/hr";
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
import { Calendar, CheckCircle, XCircle, Clock, Check, X, FileText, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function LeaveRequestsPage() {
  const [leaveRequests, setLeaveRequests] = useState<LeaveRequestResponse[]>([]);
  const [report, setReport] = useState<OrganizationLeaveReportResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLeaveData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [requestsData, reportData] = await Promise.all([
        hrRepository.getLeaveRequests(),
        hrRepository.getOrganizationLeaveReport().catch(() => null) // Fallback if endpoint fails
      ]);
      setLeaveRequests(requestsData);
      setReport(reportData);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaveData();
  }, []);

  const handleStatusUpdate = async (id: string, status: "APPROVED" | "REJECTED") => {
    try {
      await hrRepository.updateLeaveRequestStatus(id, status);
      fetchLeaveData();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : `Failed to ${status.toLowerCase()} request`);
    }
  };

  if (isLoading) return <LoadingState message="Loading leave information..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchLeaveData} />;

  const pendingRequests = leaveRequests.filter(r => r.status === "PENDING");
  const pastRequests = leaveRequests.filter(r => r.status !== "PENDING");

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Time Off & Leave</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage employee leave requests, balances, and time-off policies.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" className="bg-surface shadow-sm hover:bg-surface-hover">
            <FileText className="mr-2 h-4 w-4" />
            Generate Report
          </Button>
          <Button className="shadow-sm">
            <Calendar className="mr-2 h-4 w-4" />
            Submit Request
          </Button>
        </div>
      </div>

      {/* High Level Stats (Context) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3 text-muted-foreground mb-3">
            <AlertCircle className="h-5 w-5 text-warning" />
            <span className="text-sm font-semibold">Action Required</span>
          </div>
          <div className="text-3xl font-bold text-foreground">{pendingRequests.length}</div>
          <p className="text-xs text-muted-foreground mt-1">Pending requests</p>
        </div>
        
        {report?.report_items.slice(0, 3).map((item, i) => (
          <div key={i} className="bg-surface border border-border rounded-xl p-5 shadow-sm">
            <div className="flex items-center gap-3 text-muted-foreground mb-3">
              <Calendar className="h-5 w-5" />
              <span className="text-sm font-semibold">{item.leave_type.replace('_', ' ')}</span>
            </div>
            <div className="text-3xl font-bold text-foreground">{item.total_approved}</div>
            <p className="text-xs text-muted-foreground mt-1">Approved this period</p>
          </div>
        ))}
      </div>

      {/* Pending Requests Section */}
      {pendingRequests.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Clock className="w-5 h-5 text-warning" />
            Requires Attention
          </h2>
          <div className="bg-surface rounded-xl border border-warning/30 shadow-sm overflow-hidden ring-1 ring-warning/20">
            <Table>
              <TableHeader className="bg-warning/5">
                <TableRow>
                  <TableHead>Employee ID</TableHead>
                  <TableHead>Leave Type</TableHead>
                  <TableHead>Dates</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {pendingRequests.map((request) => (
                  <TableRow key={request.id} className="hover:bg-warning/5">
                    <TableCell className="font-medium text-foreground">
                      {request.employee_id.split("-")[0]}...
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="bg-surface">
                        {request.leave_type.replace("_", " ")}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm">
                      {new Date(request.start_date).toLocaleDateString()} &rarr; {new Date(request.end_date).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="text-sm font-medium">
                      {request.total_days} day(s) {request.is_half_day ? "(Half Day)" : ""}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-success border-success/30 hover:bg-success/10 hover:border-success"
                          onClick={() => handleStatusUpdate(request.id, "APPROVED")}
                        >
                          <Check className="w-4 h-4 mr-1" />
                          Approve
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-destructive border-destructive/30 hover:bg-destructive/10 hover:border-destructive"
                          onClick={() => handleStatusUpdate(request.id, "REJECTED")}
                        >
                          <X className="w-4 h-4 mr-1" />
                          Reject
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      {/* Request History Section */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-foreground">Request History</h2>
        
        {pastRequests.length === 0 ? (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-12">
            <EmptyState 
              title="No request history"
              description="There are no processed leave requests to display."
              icon={<Calendar className="w-8 h-8 text-muted-foreground" />}
            />
          </div>
        ) : (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Employee ID</TableHead>
                  <TableHead>Leave Type</TableHead>
                  <TableHead>Dates</TableHead>
                  <TableHead>Total Days</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {pastRequests.map((request) => (
                  <TableRow key={request.id}>
                    <TableCell className="font-medium text-muted-foreground">
                      {request.employee_id.split("-")[0]}...
                    </TableCell>
                    <TableCell>
                      {request.leave_type.replace("_", " ")}
                    </TableCell>
                    <TableCell className="text-sm">
                      {new Date(request.start_date).toLocaleDateString()} to {new Date(request.end_date).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="text-sm">
                      {request.total_days} {request.is_half_day ? "(Half Day)" : ""}
                    </TableCell>
                    <TableCell>
                      <Badge 
                        variant={
                          request.status === "APPROVED" ? "success"
                            : request.status === "REJECTED" || request.status === "CANCELLED" ? "destructive"
                            : "secondary"
                        }
                      >
                        {request.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}
