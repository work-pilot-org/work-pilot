"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { OrganizationLeaveReportResponse } from "@/types/hr";
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
import { PieChart, Users, CheckCircle, Clock, XCircle } from "lucide-react";

export default function LeaveReportsPage() {
  const [report, setReport] = useState<OrganizationLeaveReportResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReport = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getOrganizationLeaveReport();
      setReport(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave report.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, []);

  if (isLoading) return <LoadingState message="Loading leave reports..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchReport} />;

  if (!report || report.report_items.length === 0) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Leave Report</h1>
        </div>
        <EmptyState 
          title="No reports available"
          description="There is no leave data to generate a report."
          icon={<PieChart className="w-6 h-6" />}
        />
      </div>
    );
  }

  // Aggregate totals
  const totalRequests = report.report_items.reduce((acc, item) => acc + item.total_requested, 0);
  const totalApproved = report.report_items.reduce((acc, item) => acc + item.total_approved, 0);
  const totalPending = report.report_items.reduce((acc, item) => acc + item.total_pending, 0);
  const totalRejected = report.report_items.reduce((acc, item) => acc + item.total_rejected, 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Leave Report</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-border">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 text-blue-600 rounded-full">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Total Requests</p>
              <h3 className="text-2xl font-bold">{totalRequests}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-border">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 text-green-600 rounded-full">
              <CheckCircle className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Approved</p>
              <h3 className="text-2xl font-bold">{totalApproved}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-border">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-100 text-yellow-600 rounded-full">
              <Clock className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Pending</p>
              <h3 className="text-2xl font-bold">{totalPending}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-border">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-red-100 text-red-600 rounded-full">
              <XCircle className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Rejected</p>
              <h3 className="text-2xl font-bold">{totalRejected}</h3>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-4">Breakdown by Leave Type</h2>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Leave Type</TableHead>
              <TableHead>Total Requests</TableHead>
              <TableHead>Approved</TableHead>
              <TableHead>Pending</TableHead>
              <TableHead>Rejected</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {report.report_items.map((item) => (
              <TableRow key={item.leave_type}>
                <TableCell className="font-bold">{item.leave_type.replace("_", " ")}</TableCell>
                <TableCell>{item.total_requested}</TableCell>
                <TableCell className="text-green-600 font-medium">{item.total_approved}</TableCell>
                <TableCell className="text-yellow-600 font-medium">{item.total_pending}</TableCell>
                <TableCell className="text-red-600 font-medium">{item.total_rejected}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
