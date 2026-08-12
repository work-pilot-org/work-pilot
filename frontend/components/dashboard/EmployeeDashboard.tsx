"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { useAuthStore } from "@/store/authStore";
import { EmployeeResponse, AttendanceResponse } from "@/types/hr";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Button } from "@/components/ui/Button";
import {
  UserCircle2,
  Clock,
  Calendar,
  Briefcase,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  LogOut,
  LogIn
} from "lucide-react";
import { useRouter } from "next/navigation";

function formatTime(iso?: string): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function formatMinutes(mins: number): string {
  if (!mins) return "0h 0m";
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return `${h}h ${m}m`;
}

export function EmployeeDashboard() {
  const { user } = useAuthStore();
  const router = useRouter();
  const [profile, setProfile] = useState<EmployeeResponse | null>(null);
  const [attendance, setAttendance] = useState<AttendanceResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [attendanceError, setAttendanceError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setIsLoading(true);
        setError(null);
        setAttendanceError(null);
        const [emp, att] = await Promise.allSettled([
          hrRepository.getMyProfile(),
          hrRepository.getMyTodayAttendance(),
        ]);
        
        if (emp.status === "fulfilled") setProfile(emp.value);
        else throw new Error(emp.reason?.message || "Failed to load profile.");
        
        if (att.status === "fulfilled") setAttendance(att.value);
        else setAttendanceError(att.reason?.message || "Failed to load attendance.");
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load your workspace.");
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, []);

  if (isLoading) return <LoadingState message="Loading your workspace..." className="py-20" />;
  if (error) return <ErrorState message={error} />;

  const checkedIn = !!attendance?.check_in;
  const checkedOut = !!attendance?.check_out;

  return (
    <div className="flex flex-col space-y-6">
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-surface border border-border-strong rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xl border-2 border-surface shadow-sm">
            {profile?.first_name?.[0] || ""}{profile?.last_name?.[0] || ""}
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-foreground">
              Welcome back, {profile?.first_name || user?.name || "Employee"}!
            </h1>
            <p className="text-sm text-muted-foreground mt-1">
              {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
            </p>
          </div>
        </div>
        <Button variant="outline" className="shadow-sm" onClick={() => router.push('/dashboard/hr/leave')}>
          Request Leave
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Attendance Action Card */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm p-6">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-4">Today's Shift</h3>
            
            <div className="flex items-center gap-3 mb-6">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                checkedOut ? "bg-muted text-muted-foreground" :
                checkedIn ? "bg-success/10 text-success" :
                "bg-warning/10 text-warning"
              }`}>
                {checkedOut ? <LogOut className="w-5 h-5" /> : checkedIn ? <CheckCircle2 className="w-5 h-5" /> : <Clock className="w-5 h-5" />}
              </div>
              <div>
                <p className="text-sm font-medium text-foreground">
                  {checkedOut ? "Shift Complete" : checkedIn ? "Currently Working" : "Not Checked In"}
                </p>
                {attendance?.status && (
                  <Badge variant={attendance.status === "PRESENT" ? "success" : "secondary"} className="mt-1">
                    {attendance.status}
                  </Badge>
                )}
              </div>
            </div>

            <div className="space-y-3">
              <Button 
                className="w-full shadow-sm"
                disabled={!profile || checkedIn}
                onClick={async () => {
                  if (!profile) return;
                  try {
                    setIsLoading(true);
                    await hrRepository.checkIn(profile.id);
                    const newAtt = await hrRepository.getMyTodayAttendance();
                    setAttendance(newAtt);
                  } catch (err: any) {
                    alert(err.message || "Failed to check in");
                  } finally {
                    setIsLoading(false);
                  }
                }}
              >
                <LogIn className="w-4 h-4 mr-2" />
                Check In Now
              </Button>
              <Button 
                variant="outline"
                className="w-full shadow-sm"
                disabled={!profile || !checkedIn || checkedOut}
                onClick={async () => {
                  if (!profile) return;
                  try {
                    setIsLoading(true);
                    await hrRepository.checkOut(profile.id);
                    const newAtt = await hrRepository.getMyTodayAttendance();
                    setAttendance(newAtt);
                  } catch (err: any) {
                    alert(err.message || "Failed to check out");
                  } finally {
                    setIsLoading(false);
                  }
                }}
              >
                <LogOut className="w-4 h-4 mr-2" />
                Check Out
              </Button>
            </div>

            {attendanceError && (
              <div className="mt-4 text-xs text-destructive bg-destructive/10 p-3 rounded-lg flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0" />
                <span>{attendanceError}</span>
              </div>
            )}
          </div>
          
          {/* Quick Links */}
          <div className="bg-surface-hover/30 border border-border rounded-xl p-4 flex flex-col gap-2">
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-2">Quick Links</h3>
            <button onClick={() => router.push('/dashboard/hr/attendance')} className="flex items-center justify-between p-2 rounded-lg hover:bg-surface transition-colors text-sm font-medium text-foreground">
              <div className="flex items-center gap-2"><Calendar className="w-4 h-4 text-muted-foreground" /> Timesheets</div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
            </button>
            <button onClick={() => router.push('/dashboard/it/tickets')} className="flex items-center justify-between p-2 rounded-lg hover:bg-surface transition-colors text-sm font-medium text-foreground">
              <div className="flex items-center gap-2"><AlertTriangle className="w-4 h-4 text-muted-foreground" /> Report IT Issue</div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
            </button>
          </div>
        </div>

        {/* Profile & Context */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm">
            <div className="px-6 py-4 border-b border-border flex items-center justify-between">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider flex items-center gap-2">
                <UserCircle2 className="w-4 h-4" /> My Profile
              </h3>
            </div>
            
            {profile ? (
              <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-8">
                <div>
                  <dt className="text-xs font-medium text-muted-foreground mb-1">Employee Code</dt>
                  <dd className="text-sm font-medium text-foreground">{profile.employee_code}</dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-muted-foreground mb-1">Employment Type</dt>
                  <dd className="text-sm font-medium text-foreground">{profile.employment_type}</dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-muted-foreground mb-1">Status</dt>
                  <dd>
                    <Badge variant={profile.employment_status === "ACTIVE" ? "success" : "secondary"}>
                      {profile.employment_status}
                    </Badge>
                  </dd>
                </div>
                <div>
                  <dt className="text-xs font-medium text-muted-foreground mb-1">Joining Date</dt>
                  <dd className="text-sm font-medium text-foreground">
                    {new Date(profile.joining_date).toLocaleDateString()}
                  </dd>
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-sm text-muted-foreground">
                Profile context unavailable.
              </div>
            )}
          </div>
          
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm">
            <div className="px-6 py-4 border-b border-border flex items-center justify-between">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider flex items-center gap-2">
                <Clock className="w-4 h-4" /> Today's Log
              </h3>
            </div>
            {attendance ? (
              <div className="p-6 grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
                <div className="bg-surface-hover/50 p-4 rounded-lg">
                  <span className="block text-xs font-medium text-muted-foreground mb-1">Time In</span>
                  <span className="text-lg font-bold text-foreground">{formatTime(attendance.check_in)}</span>
                </div>
                <div className="bg-surface-hover/50 p-4 rounded-lg">
                  <span className="block text-xs font-medium text-muted-foreground mb-1">Time Out</span>
                  <span className="text-lg font-bold text-foreground">{formatTime(attendance.check_out)}</span>
                </div>
                <div className="bg-surface-hover/50 p-4 rounded-lg">
                  <span className="block text-xs font-medium text-muted-foreground mb-1">Hours Logged</span>
                  <span className="text-lg font-bold text-foreground">{formatMinutes(attendance.working_minutes)}</span>
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-sm text-muted-foreground">
                No active log for today. Check in to start tracking.
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}
