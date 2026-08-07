"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { useAuthStore } from "@/store/authStore";
import { EmployeeResponse, AttendanceResponse } from "@/types/hr";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import {
  User,
  Clock,
  Calendar,
  Briefcase,
  CheckCircle,
  XCircle,
} from "lucide-react";

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
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">
          Welcome back, {profile?.first_name || user?.name || "Employee"}!
        </h1>
        <p className="text-sm text-gray-500 mt-1">
          {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
        </p>
      </div>

      {/* Profile + Attendance Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Employee Profile Card */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center">
              <User className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900">My Profile</h2>
              <p className="text-xs text-gray-500">Employee Details</p>
            </div>
          </div>
          {profile ? (
            <dl className="space-y-3 text-sm">
              <div className="flex justify-between">
                <dt className="text-gray-500">Employee Code</dt>
                <dd className="font-medium text-gray-900">{profile.employee_code}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Full Name</dt>
                <dd className="font-medium text-gray-900">{profile.first_name} {profile.last_name}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Employment Type</dt>
                <dd><Badge variant="secondary">{profile.employment_type}</Badge></dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Status</dt>
                <dd>
                  <Badge variant={profile.employment_status === "ACTIVE" ? "success" : "secondary" as never}>
                    {profile.employment_status}
                  </Badge>
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Joining Date</dt>
                <dd className="font-medium text-gray-900">
                  {new Date(profile.joining_date).toLocaleDateString()}
                </dd>
              </div>
            </dl>
          ) : (
            <p className="text-sm text-gray-400 italic">No employee profile found. Contact HR.</p>
          )}
        </div>

        {/* Today's Attendance Card */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
              <Clock className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900">Today&apos;s Attendance</h2>
              <p className="text-xs text-gray-500">Live status</p>
            </div>
          </div>
          {attendanceError ? (
            <div className="text-sm text-red-600 bg-red-50 p-4 rounded-lg border border-red-100 flex flex-col gap-1">
              <span className="font-semibold flex items-center gap-2">
                <XCircle className="w-4 h-4" /> Attendance Service Error
              </span>
              <span>{attendanceError}</span>
            </div>
          ) : attendance ? (
            <dl className="space-y-3 text-sm">
              <div className="flex justify-between items-center">
                <dt className="text-gray-500">Status</dt>
                <dd>
                  <Badge
                    variant={
                      attendance.status === "PRESENT"
                        ? "success"
                        : attendance.status === "ABSENT"
                        ? "destructive"
                        : "secondary" as never
                    }
                  >
                    {attendance.status}
                  </Badge>
                </dd>
              </div>
              <div className="flex justify-between items-center">
                <dt className="text-gray-500 flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5 text-green-500" /> Check-in
                </dt>
                <dd className="font-medium text-gray-900">{formatTime(attendance.check_in)}</dd>
              </div>
              <div className="flex justify-between items-center">
                <dt className="text-gray-500 flex items-center gap-1">
                  <XCircle className="w-3.5 h-3.5 text-red-400" /> Check-out
                </dt>
                <dd className="font-medium text-gray-900">{formatTime(attendance.check_out)}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Hours Worked</dt>
                <dd className="font-medium text-gray-900">{formatMinutes(attendance.working_minutes)}</dd>
              </div>
              {attendance.overtime_minutes > 0 && (
                <div className="flex justify-between">
                  <dt className="text-gray-500">Overtime</dt>
                  <dd className="font-medium text-orange-600">{formatMinutes(attendance.overtime_minutes)}</dd>
                </div>
              )}
            </dl>
          ) : (
            <div className="text-sm text-gray-400 italic space-y-1">
              <p>No attendance record for today.</p>
              <p className="text-xs">Contact your HR administrator if you believe this is an error.</p>
            </div>
          )}
        </div>
      </div>

      {/* Info Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex items-center gap-4">
          <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
            <Briefcase className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">{profile?.employment_type ?? "—"}</p>
            <p className="text-xs text-gray-500">Employment Type</p>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex items-center gap-4">
          <div className="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center">
            <Calendar className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">
              {profile?.joining_date
                ? new Date(profile.joining_date).toLocaleDateString()
                : "—"}
            </p>
            <p className="text-xs text-gray-500">Joining Date</p>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex items-center gap-4">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${checkedIn && !checkedOut ? "bg-green-50" : "bg-gray-50"}`}>
            <Clock className={`w-5 h-5 ${checkedIn && !checkedOut ? "text-green-600" : "text-gray-400"}`} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">
              {!checkedIn ? "Not Checked In" : !checkedOut ? "Currently Working" : "Day Complete"}
            </p>
            <p className="text-xs text-gray-500">Today&apos;s Status</p>
          </div>
        </div>
      </div>
    </div>
  );
}
