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
import { UserCheck, Clock, Calendar, LogIn, LogOut, CheckCircle2, AlertTriangle, Users } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { DropdownMenu } from "@/components/ui/DropdownMenu";

export default function AttendancePage() {
  const [attendance, setAttendance] = useState<AttendanceResponse[]>([]);
  const [employeeId, setEmployeeId] = useState<string | null>(null);
  const [myAttendance, setMyAttendance] = useState<AttendanceResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [attendanceData, profileData, myToday] = await Promise.all([
        hrRepository.getTodayAttendance().catch(() => []),
        hrRepository.getMyProfile(),
        hrRepository.getMyTodayAttendance().catch(() => null)
      ]);
      setAttendance(attendanceData);
      setEmployeeId(profileData.id);
      setMyAttendance(myToday);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load attendance data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading attendance context..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;

  const presentCount = attendance.filter(a => a.status === "PRESENT").length;
  const absentCount = attendance.filter(a => a.status === "ABSENT").length;
  const lateCount = attendance.filter(a => a.status === "LATE").length;
  
  const hasCheckedIn = myAttendance?.check_in != null;
  const hasCheckedOut = myAttendance?.check_out != null;

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Attendance</h1>
          <p className="text-muted-foreground mt-1 text-sm">Monitor daily attendance, check-ins, and team availability.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left Col: Personal Status & Quick Actions */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
            <h3 className="text-sm font-semibold text-foreground mb-4">Your Status Today</h3>
            
            <div className="flex items-center gap-3 mb-6">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                hasCheckedOut ? "bg-muted text-muted-foreground" :
                hasCheckedIn ? "bg-success/10 text-success" :
                "bg-warning/10 text-warning"
              }`}>
                {hasCheckedOut ? <LogOut className="w-5 h-5" /> : hasCheckedIn ? <CheckCircle2 className="w-5 h-5" /> : <Clock className="w-5 h-5" />}
              </div>
              <div>
                <p className="text-sm font-medium text-foreground">
                  {hasCheckedOut ? "Shift Complete" : hasCheckedIn ? "Active Shift" : "Not Checked In"}
                </p>
                <p className="text-xs text-muted-foreground">
                  {new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' })}
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <Button 
                className="w-full shadow-sm"
                disabled={!employeeId || hasCheckedIn}
                onClick={async () => {
                  if (!employeeId) return;
                  try {
                    await hrRepository.checkIn(employeeId);
                    fetchData();
                  } catch (err: unknown) {
                    alert(err instanceof Error ? err.message : "Check-in failed");
                  }
                }}
              >
                <LogIn className="w-4 h-4 mr-2" />
                Check In Now
              </Button>
              <Button 
                variant="outline"
                className="w-full shadow-sm"
                disabled={!employeeId || !hasCheckedIn || hasCheckedOut}
                onClick={async () => {
                  if (!employeeId) return;
                  try {
                    await hrRepository.checkOut(employeeId);
                    fetchData();
                  } catch (err: unknown) {
                    alert(err instanceof Error ? err.message : "Check-out failed");
                  }
                }}
              >
                <LogOut className="w-4 h-4 mr-2" />
                Check Out
              </Button>
            </div>
            
            {myAttendance && (
              <div className="mt-6 pt-4 border-t border-border grid grid-cols-2 gap-2 text-center text-sm">
                <div>
                  <span className="block text-xs text-muted-foreground mb-1">In</span>
                  <span className="font-medium text-foreground">{myAttendance.check_in || "--:--"}</span>
                </div>
                <div>
                  <span className="block text-xs text-muted-foreground mb-1">Out</span>
                  <span className="font-medium text-foreground">{myAttendance.check_out || "--:--"}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Col: Org Overview */}
        <div className="lg:col-span-3 space-y-6">
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-muted-foreground">Present Today</span>
                <Users className="w-4 h-4 text-success" />
              </div>
              <div className="text-3xl font-bold text-foreground">{presentCount}</div>
            </div>
            <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-muted-foreground">Late Arrivals</span>
                <Clock className="w-4 h-4 text-warning" />
              </div>
              <div className="text-3xl font-bold text-foreground">{lateCount}</div>
            </div>
            <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-muted-foreground">Absent</span>
                <AlertTriangle className="w-4 h-4 text-destructive" />
              </div>
              <div className="text-3xl font-bold text-foreground">{absentCount}</div>
            </div>
          </div>

          <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden">
            <div className="p-4 border-b border-border bg-surface-hover/30 flex justify-between items-center">
              <h3 className="text-sm font-semibold text-foreground">Organization Log</h3>
              <Button variant="outline" size="sm" className="h-8 shadow-none">
                <Calendar className="w-4 h-4 mr-2" />
                Filter by Date
              </Button>
            </div>
            
            {attendance.length === 0 ? (
              <div className="p-12">
                <EmptyState 
                  title="No attendance records"
                  description="There are no attendance records logged for today across the organization."
                  icon={<UserCheck className="w-8 h-8 text-muted-foreground" />}
                />
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Employee</TableHead>
                    <TableHead>Check In</TableHead>
                    <TableHead>Check Out</TableHead>
                    <TableHead>Working Mins</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {attendance.map((record) => (
                    <TableRow key={record.id} className="group hover:bg-surface-hover">
                      <TableCell className="font-medium text-foreground">
                        {record.employee_id.split("-")[0]}...
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {record.check_in || <span className="opacity-50">--:--</span>}
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {record.check_out || <span className="opacity-50">--:--</span>}
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {record.working_minutes}
                      </TableCell>
                      <TableCell>
                        <Badge 
                          variant={
                            record.status === "PRESENT" ? "success"
                              : record.status === "ABSENT" ? "destructive"
                              : "warning"
                          }
                        >
                          {record.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                         <DropdownMenu 
                            items={[
                              { label: "View Details", onClick: () => {} },
                              { label: "Override Status", onClick: () => {} }
                            ]}
                          />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}
