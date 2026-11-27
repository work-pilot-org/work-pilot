"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { AttendanceResponse } from "@/types/hr";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Calendar, Clock } from "lucide-react";

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

export function MyAttendance() {
  const [attendance, setAttendance] = useState<AttendanceResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        const data = await hrRepository.getMyTodayAttendance();
        setAttendance(data);
      } catch (err: any) {
        setError(err.message || "Failed to load attendance");
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  if (isLoading) return <LoadingState message="Loading attendance records..." />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">My Attendance</h2>
        <p className="text-muted-foreground mt-1">View your daily logs and timesheets.</p>
      </div>

      <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
        <div className="p-6 border-b border-border flex items-center justify-between bg-surface-hover/30">
          <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Clock className="w-5 h-5 text-primary" /> Today's Log
          </h3>
          <span className="text-sm font-medium text-muted-foreground">
            {new Date().toLocaleDateString("en-US", { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </span>
        </div>

        <div className="p-8">
          {attendance ? (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
              <div className="bg-surface border border-border p-6 rounded-xl shadow-sm">
                <span className="block text-sm font-medium text-muted-foreground mb-2 uppercase tracking-wider">Time In</span>
                <span className="text-3xl font-bold text-foreground tracking-tight">{formatTime(attendance.check_in)}</span>
              </div>
              <div className="bg-surface border border-border p-6 rounded-xl shadow-sm">
                <span className="block text-sm font-medium text-muted-foreground mb-2 uppercase tracking-wider">Time Out</span>
                <span className="text-3xl font-bold text-foreground tracking-tight">{formatTime(attendance.check_out)}</span>
              </div>
              <div className="bg-surface border border-border p-6 rounded-xl shadow-sm">
                <span className="block text-sm font-medium text-muted-foreground mb-2 uppercase tracking-wider">Hours Logged</span>
                <span className="text-3xl font-bold text-foreground tracking-tight">{formatMinutes(attendance.working_minutes)}</span>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 bg-surface border border-border rounded-xl border-dashed">
              <Calendar className="w-12 h-12 text-muted mx-auto mb-4" />
              <p className="text-lg font-medium text-foreground">No Log for Today</p>
              <p className="text-sm text-muted-foreground mt-1">You haven't checked in yet today.</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden p-8 text-center text-muted-foreground">
        <p>Historical attendance view is coming soon.</p>
      </div>
    </div>
  );
}
