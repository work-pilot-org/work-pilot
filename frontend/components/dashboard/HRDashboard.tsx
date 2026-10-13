"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { hrRepository } from "@/repositories/hrRepository";
import { Users, Clock, Calendar, CheckCircle2, UserPlus, AlertTriangle } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmployeeResponse } from "@/types/hr";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { getAttendanceSummary, getLeaveUtilization, getHeadcount } from "@/lib/api/analytics";
import { CustomBarChart, CustomPieChart } from "@/components/analytics/AnalyticsCharts";

export function HRDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [attendanceSummary, setAttendanceSummary] = useState<any[]>([]);
  const [leaveSummary, setLeaveSummary] = useState<any[]>([]);
  const [headcountSummary, setHeadcountSummary] = useState<any[]>([]);
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [empData, attData, leaveData, hcData] = await Promise.all([
          hrRepository.getEmployees().catch(() => []),
          getAttendanceSummary().catch(() => ({ summary: [] })),
          getLeaveUtilization().catch(() => ({ summary: [] })),
          getHeadcount().catch(() => ({ summary: [] }))
        ]);
        setEmployees(empData);
        setAttendanceSummary(attData.summary || []);
        setLeaveSummary(leaveData.summary || []);
        setHeadcountSummary(hcData.summary || []);
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

  const totalEmployees = headcountSummary.reduce((acc, curr) => acc + (curr.count || 0), 0);
  const presentCount = attendanceSummary.find(a => a.status === "PRESENT")?.records || 0;
  const absentCount = attendanceSummary.find(a => a.status === "ABSENT")?.records || 0;
  const lateCount = attendanceSummary.find(a => a.status === "LATE")?.records || 0;

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto w-full pb-12">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-2">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">
              HR Operations, {user?.name || "Admin"}
            </h1>
            <p className="text-sm font-medium text-muted-foreground mt-1">
              {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="primary" onClick={() => router.push('/dashboard/hr/create')}>
            <UserPlus className="w-4 h-4 mr-2" />
            Add Employee
          </Button>
        </div>
      </div>
      
      {/* Real Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Total Headcount</span>
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Users className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{totalEmployees}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Present Today</span>
              <div className="w-8 h-8 rounded-full bg-success/10 flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4 text-success" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{presentCount}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Late Arrivals</span>
              <div className="w-8 h-8 rounded-full bg-warning/10 flex items-center justify-center">
                <Clock className="w-4 h-4 text-warning" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{lateCount}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Absences</span>
              <div className="w-8 h-8 rounded-full bg-destructive/10 flex items-center justify-center">
                <AlertTriangle className="w-4 h-4 text-destructive" />
              </div>
            </div>
            <div className="text-3xl font-bold text-foreground tracking-tight">{absentCount}</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Leave Utilization
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <CustomPieChart data={leaveSummary} dataKey="requests" nameKey="status" />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Headcount Distribution
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <CustomBarChart 
              data={headcountSummary} 
              xAxisKey="status" 
              bars={[{ key: "count", color: "var(--primary)", name: "Employees" }]} 
            />
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Quick Links Panel */}
        <Card>
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              HR Operations
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid grid-cols-2 gap-4">
              <button onClick={() => router.push('/dashboard/hr')} className="group flex flex-col items-center justify-center p-6 bg-surface-hover/30 rounded-xl border border-border/60 hover:border-border-strong hover:bg-surface-hover transition-all gap-4 shadow-[var(--shadow-subtle)]">
                <div className="w-12 h-12 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                  <Users className="w-5 h-5 text-primary" />
                </div>
                <span className="text-sm font-semibold text-foreground">Directory</span>
              </button>
              <button onClick={() => router.push('/dashboard/hr/attendance')} className="group flex flex-col items-center justify-center p-6 bg-surface-hover/30 rounded-xl border border-border/60 hover:border-border-strong hover:bg-surface-hover transition-all gap-4 shadow-[var(--shadow-subtle)]">
                <div className="w-12 h-12 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                  <Clock className="w-5 h-5 text-primary" />
                </div>
                <span className="text-sm font-semibold text-foreground">Attendance Logs</span>
              </button>
              <button onClick={() => router.push('/dashboard/hr/leave')} className="group flex flex-col items-center justify-center p-6 bg-surface-hover/30 rounded-xl border border-border/60 hover:border-border-strong hover:bg-surface-hover transition-all gap-4 shadow-[var(--shadow-subtle)]">
                <div className="w-12 h-12 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                  <Calendar className="w-5 h-5 text-primary" />
                </div>
                <span className="text-sm font-semibold text-foreground">Leave Requests</span>
              </button>
              <button onClick={() => router.push('/dashboard/hr/organization')} className="group flex flex-col items-center justify-center p-6 bg-surface-hover/30 rounded-xl border border-border/60 hover:border-border-strong hover:bg-surface-hover transition-all gap-4 shadow-[var(--shadow-subtle)]">
                <div className="w-12 h-12 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                  <UserPlus className="w-5 h-5 text-primary" />
                </div>
                <span className="text-sm font-semibold text-foreground">Organization Config</span>
              </button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Additions */}
        <Card className="flex flex-col">
          <CardHeader className="border-b border-border/40 pb-4">
            <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Recently Added
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6 flex-1 flex flex-col">
            {employees.length === 0 ? (
              <div className="flex-1 flex items-center justify-center text-sm font-medium text-muted-foreground border-2 border-dashed border-border/60 rounded-xl bg-surface-hover/30 min-h-[200px]">
                No employees found in the organization.
              </div>
            ) : (
              <div className="space-y-3 flex-1 overflow-auto max-h-[300px] pr-2">
                {employees.slice(0, 5).map(emp => (
                  <div key={emp.id} className="flex items-center gap-4 p-4 rounded-xl border border-border/40 bg-surface hover:bg-surface-hover/50 transition-colors shadow-[var(--shadow-subtle)]">
                    <div className="w-10 h-10 rounded-full bg-primary/5 text-primary flex items-center justify-center font-bold text-sm border border-primary/10 shrink-0">
                      {emp.first_name[0]}{emp.last_name[0]}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-foreground truncate">{emp.first_name} {emp.last_name}</p>
                      <p className="text-[11px] font-medium uppercase tracking-widest text-muted-foreground truncate mt-0.5">{emp.employment_type} • {emp.employee_code}</p>
                    </div>
                    <Button variant="secondary" size="sm" onClick={() => router.push(`/dashboard/hr/employees/${emp.id}`)}>
                      View
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

    </div>
  );
}
