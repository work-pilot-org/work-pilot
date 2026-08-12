"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { hrRepository } from "@/repositories/hrRepository";
import { Users, Clock, Calendar, CheckCircle2, UserPlus, AlertTriangle } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmployeeResponse, AttendanceResponse } from "@/types/hr";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";

export function HRDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [attendance, setAttendance] = useState<AttendanceResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [empData, attData] = await Promise.all([
          hrRepository.getEmployees().catch(() => []),
          hrRepository.getTodayAttendance().catch(() => [])
        ]);
        setEmployees(empData);
        setAttendance(attData);
      } catch (err: unknown) {
        setError("Failed to load HR dashboard data.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading HR Overview..." className="py-20" />;
  if (error) return <ErrorState message={error} />;

  const totalEmployees = employees.length;
  const presentCount = attendance.filter(a => a.status === "PRESENT").length;
  const absentCount = attendance.filter(a => a.status === "ABSENT").length;
  const lateCount = attendance.filter(a => a.status === "LATE").length;

  return (
    <div className="flex flex-col h-full space-y-6 max-w-7xl mx-auto pb-12">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-surface border border-border-strong rounded-xl p-6 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            HR Operations, {user?.name || "Admin"}
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm" onClick={() => router.push('/dashboard/hr/create')}>
            <UserPlus className="w-4 h-4 mr-2" />
            Add Employee
          </Button>
        </div>
      </div>
      
      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Total Headcount</span>
            <Users className="w-4 h-4 text-primary" />
          </div>
          <div className="text-3xl font-bold text-foreground">{totalEmployees}</div>
        </div>
        
        <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-muted-foreground">Present Today</span>
            <CheckCircle2 className="w-4 h-4 text-success" />
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
            <span className="text-sm font-semibold text-muted-foreground">Absences</span>
            <AlertTriangle className="w-4 h-4 text-destructive" />
          </div>
          <div className="text-3xl font-bold text-foreground">{absentCount}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4">
        {/* Quick Links Panel */}
        <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">HR Operations</h3>
          <div className="grid grid-cols-2 gap-4">
            <button onClick={() => router.push('/dashboard/hr')} className="flex flex-col items-center justify-center p-6 bg-surface-hover/50 rounded-lg border border-border hover:border-primary transition-colors gap-3">
              <Users className="w-6 h-6 text-primary" />
              <span className="text-sm font-medium text-foreground">Employee Directory</span>
            </button>
            <button onClick={() => router.push('/dashboard/hr/attendance')} className="flex flex-col items-center justify-center p-6 bg-surface-hover/50 rounded-lg border border-border hover:border-primary transition-colors gap-3">
              <Clock className="w-6 h-6 text-primary" />
              <span className="text-sm font-medium text-foreground">Attendance Logs</span>
            </button>
            <button onClick={() => router.push('/dashboard/hr/leave')} className="flex flex-col items-center justify-center p-6 bg-surface-hover/50 rounded-lg border border-border hover:border-primary transition-colors gap-3">
              <Calendar className="w-6 h-6 text-primary" />
              <span className="text-sm font-medium text-foreground">Leave Requests</span>
            </button>
            <button onClick={() => router.push('/dashboard/hr/organization')} className="flex flex-col items-center justify-center p-6 bg-surface-hover/50 rounded-lg border border-border hover:border-primary transition-colors gap-3">
              <UserPlus className="w-6 h-6 text-primary" />
              <span className="text-sm font-medium text-foreground">Organization Config</span>
            </button>
          </div>
        </div>

        {/* Recent Additions */}
        <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-6 flex flex-col">
          <h3 className="text-lg font-semibold text-foreground mb-4">Recently Added</h3>
          {employees.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-sm text-muted-foreground border-2 border-dashed border-border rounded-lg">
              No employees found in the organization.
            </div>
          ) : (
            <div className="space-y-4 flex-1 overflow-auto max-h-[300px] pr-2">
              {employees.slice(0, 5).map(emp => (
                <div key={emp.id} className="flex items-center gap-4 p-3 rounded-lg border border-border bg-surface-hover/30">
                  <div className="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-sm shrink-0">
                    {emp.first_name[0]}{emp.last_name[0]}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-foreground">{emp.first_name} {emp.last_name}</p>
                    <p className="text-xs text-muted-foreground">{emp.employment_type} • {emp.employee_code}</p>
                  </div>
                  <Button variant="outline" size="sm" className="shadow-sm h-8" onClick={() => router.push(`/dashboard/hr/${emp.id}`)}>
                    View
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
