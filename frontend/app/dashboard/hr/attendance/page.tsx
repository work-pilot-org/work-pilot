"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { AttendanceResponse } from "@/types/hr";
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
import { Button } from "@/components/ui/Button";

export default function AttendancePage() {
  const [attendance, setAttendance] = useState<AttendanceResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAttendance = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getTodayAttendance();
      setAttendance(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load today's attendance.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAttendance();
  }, []);

  if (isLoading) return <LoadingState message="Loading attendance data..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchAttendance} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Today's Attendance</h1>
        <div className="flex gap-2">
          <Button 
            variant="primary" 
            onClick={async () => {
              try {
                await hrRepository.checkIn();
                fetchAttendance();
              } catch (err: unknown) {
                alert(err instanceof Error ? err.message : "Check-in failed");
              }
            }}
          >
            Check In
          </Button>
          <Button 
            variant="outline"
            onClick={async () => {
              try {
                await hrRepository.checkOut();
                fetchAttendance();
              } catch (err: unknown) {
                alert(err instanceof Error ? err.message : "Check-out failed");
              }
            }}
          >
            Check Out
          </Button>
        </div>
      </div>

      {attendance.length === 0 ? (
        <EmptyState 
          title="No attendance records found"
          description="There are no attendance records for today."
          icon={<UserCheck className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee ID</TableHead>
              <TableHead>Check In</TableHead>
              <TableHead>Check Out</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Working Mins</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {attendance.map((record) => (
              <TableRow key={record.id}>
                <TableCell className="font-medium text-muted-foreground">
                  {record.employee_id.split("-")[0]}...
                </TableCell>
                <TableCell>{record.check_in || "--:--"}</TableCell>
                <TableCell>{record.check_out || "--:--"}</TableCell>
                <TableCell>
                  <Badge 
                    variant={
                      record.status === "PRESENT"
                        ? "success"
                        : record.status === "ABSENT"
                        ? "destructive"
                        : "warning"
                    }
                  >
                    {record.status}
                  </Badge>
                </TableCell>
                <TableCell>{record.working_minutes}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
