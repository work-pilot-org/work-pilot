"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { useAuthStore } from "@/store/authStore";
import { EmployeeResponse, AttendanceResponse } from "@/types/hr";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
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
    <div className="flex flex-col space-y-8 max-w-7xl mx-auto w-full">
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-2">
        <div className="flex items-center gap-5">
          <div className="w-14 h-14 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xl border-2 border-background shadow-sm shrink-0">
            {profile?.first_name?.[0] || ""}{profile?.last_name?.[0] || ""}
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">
              Welcome back, {profile?.first_name || user?.name || "Employee"}
            </h1>
            <p className="text-sm font-medium text-muted-foreground mt-1">
              {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
            </p>
          </div>
        </div>
        <Button variant="primary" onClick={() => router.push('/dashboard/employee/leave')}>
          Request Leave
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Content Area */}
        <div className="lg:col-span-2 flex flex-col gap-8">
          
          <Card>
            <CardHeader className="border-b border-border/40 pb-4">
              <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground flex items-center gap-2">
                <UserCircle2 className="w-4 h-4" /> My Profile
              </CardTitle>
            </CardHeader>
            <CardContent>
              {profile ? (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 pt-6">
                  <div>
                    <dt className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1.5">Employee Code</dt>
                    <dd className="text-sm font-semibold text-foreground">{profile.employee_code}</dd>
                  </div>
                  <div>
                    <dt className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1.5">Employment Type</dt>
                    <dd className="text-sm font-semibold text-foreground">{profile.employment_type}</dd>
                  </div>
                  <div>
                    <dt className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1.5">Status</dt>
                    <dd>
                      <Badge variant={profile.employment_status === "ACTIVE" ? "success" : "secondary"}>
                        {profile.employment_status}
                      </Badge>
                    </dd>
                  </div>
                  <div>
                    <dt className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1.5">Joining Date</dt>
                    <dd className="text-sm font-semibold text-foreground">
                      {new Date(profile.joining_date).toLocaleDateString()}
                    </dd>
                  </div>
                </div>
              ) : (
                <div className="pt-6 text-center text-sm font-medium text-muted-foreground">
                  Profile context unavailable.
                </div>
              )}
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="border-b border-border/40 pb-4">
              <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground flex items-center gap-2">
                <Clock className="w-4 h-4" /> Today's Log
              </CardTitle>
            </CardHeader>
            <CardContent>
              {attendance ? (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 pt-6">
                  <div className="bg-surface border border-border/60 shadow-[var(--shadow-subtle)] p-5 rounded-xl text-center">
                    <span className="block text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1.5">Time In</span>
                    <span className="text-2xl font-bold text-foreground tracking-tight">{formatTime(attendance.check_in)}</span>
                  </div>
                  <div className="bg-surface border border-border/60 shadow-[var(--shadow-subtle)] p-5 rounded-xl text-center">
                    <span className="block text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1.5">Time Out</span>
                    <span className="text-2xl font-bold text-foreground tracking-tight">{formatTime(attendance.check_out)}</span>
                  </div>
                  <div className="bg-primary/5 border border-primary/10 p-5 rounded-xl text-center relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-3 opacity-10">
                      <Clock className="w-12 h-12 text-primary" />
                    </div>
                    <span className="relative z-10 block text-[10px] font-bold text-primary uppercase tracking-widest mb-1.5">Hours Logged</span>
                    <span className="relative z-10 text-2xl font-bold text-primary tracking-tight">{formatMinutes(attendance.working_minutes)}</span>
                  </div>
                </div>
              ) : (
                <div className="pt-6 text-center text-sm font-medium text-muted-foreground">
                  No active log for today. Check in to start tracking.
                </div>
              )}
            </CardContent>
          </Card>
          
        </div>

        {/* Action Sidebar (Right Side) */}
        <div className="lg:col-span-1 flex flex-col gap-8">
          
          <Card className="overflow-hidden relative shadow-[var(--shadow-sm)] border-border/80">
            {/* Subtle background decoration */}
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-primary/5 rounded-full blur-2xl -z-10" />
            
            <CardHeader className="pb-2 pt-6 border-none">
              <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Today's Shift</CardTitle>
            </CardHeader>
            <CardContent className="pt-4">
              
              <div className="flex items-center gap-4 mb-8">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 shadow-[var(--shadow-subtle)] border ${
                  checkedOut ? "bg-surface-hover text-muted-foreground border-border/50" :
                  checkedIn ? "bg-success/10 text-success border-success/20" :
                  "bg-warning/10 text-warning border-warning/20"
                }`}>
                  {checkedOut ? <LogOut className="w-5 h-5" /> : checkedIn ? <CheckCircle2 className="w-5 h-5" /> : <Clock className="w-5 h-5" />}
                </div>
                <div>
                  <p className="text-base font-bold text-foreground tracking-tight">
                    {checkedOut ? "Shift Complete" : checkedIn ? "Currently Working" : "Not Checked In"}
                  </p>
                  {attendance?.status && (
                    <Badge variant={attendance.status === "PRESENT" ? "success" : "secondary"} className="mt-1.5">
                      {attendance.status}
                    </Badge>
                  )}
                </div>
              </div>

              <div className="space-y-3">
                <Button 
                  variant="primary"
                  className="w-full h-11 text-sm font-semibold"
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
                  variant="secondary"
                  className="w-full h-11 text-sm font-semibold"
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
                <div className="mt-5 text-xs text-destructive bg-destructive/5 border border-destructive/20 p-3.5 rounded-lg flex items-start gap-2.5">
                  <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                  <span className="leading-relaxed font-medium">{attendanceError}</span>
                </div>
              )}
            </CardContent>
          </Card>
          
          {/* Quick Links as a clean list */}
          <div>
            <h3 className="text-[11px] font-bold text-muted-foreground uppercase tracking-widest mb-3 px-2">Quick Actions</h3>
            <div className="flex flex-col gap-1.5">
              <button onClick={() => router.push('/dashboard/employee/attendance')} className="flex items-center justify-between p-3.5 rounded-xl hover:bg-surface-hover/80 transition-colors text-sm font-semibold text-foreground border border-transparent hover:border-border/40">
                <div className="flex items-center gap-3"><Calendar className="w-4 h-4 text-muted-foreground" /> View Timesheets</div>
                <ArrowRight className="w-4 h-4 text-muted-foreground/50" />
              </button>
              <button onClick={() => router.push('/dashboard/it/tickets')} className="flex items-center justify-between p-3.5 rounded-xl hover:bg-surface-hover/80 transition-colors text-sm font-semibold text-foreground border border-transparent hover:border-border/40">
                <div className="flex items-center gap-3"><AlertTriangle className="w-4 h-4 text-muted-foreground" /> Report IT Issue</div>
                <ArrowRight className="w-4 h-4 text-muted-foreground/50" />
              </button>
            </div>
          </div>
          
        </div>

      </div>
    </div>
  );
}

