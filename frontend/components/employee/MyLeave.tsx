"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeaveRequestResponse } from "@/types/hr";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Plus, CalendarDays } from "lucide-react";
import { useAuthStore } from "@/store/authStore";

export function MyLeave() {
  const { user } = useAuthStore();
  const [requests, setRequests] = useState<LeaveRequestResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isCreating, setIsCreating] = useState(false);
  const [newRequest, setNewRequest] = useState({
    leave_type: "ANNUAL",
    start_date: "",
    end_date: "",
    reason: "",
    employee_id: "00000000-0000-0000-0000-000000000000" // Backend overwrites this
  });

  const loadRequests = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getMyLeaveRequests();
      setRequests(data);
    } catch (err: any) {
      setError(err.message || "Failed to load leave requests");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadRequests();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      await hrRepository.createLeaveRequest(newRequest);
      setIsCreating(false);
      setNewRequest({
        leave_type: "ANNUAL",
        start_date: "",
        end_date: "",
        reason: "",
        employee_id: "00000000-0000-0000-0000-000000000000"
      });
      await loadRequests();
    } catch (err: any) {
      alert(err.message || "Failed to submit request");
      setIsLoading(false);
    }
  };

  if (isLoading && !isCreating && requests.length === 0) return <LoadingState message="Loading your leave requests..." />;
  if (error && requests.length === 0) return <ErrorState message={error} />;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">My Leave</h2>
          <p className="text-muted-foreground mt-1">Request time off and view your leave history.</p>
        </div>
        <Button onClick={() => setIsCreating(true)} disabled={isCreating}>
          <Plus className="w-4 h-4 mr-2" /> Request Time Off
        </Button>
      </div>

      {isCreating && (
        <form onSubmit={handleCreate} className="bg-surface border border-border rounded-xl p-6 shadow-sm space-y-4">
          <h3 className="text-lg font-semibold mb-4">Request Time Off</h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">Leave Type</label>
                <select
                  value={newRequest.leave_type}
                  onChange={(e) => setNewRequest({ ...newRequest, leave_type: e.target.value as any })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                >
                  <option value="ANNUAL">Annual Leave</option>
                  <option value="SICK">Sick Leave</option>
                  <option value="UNPAID">Unpaid Leave</option>
                  <option value="MATERNITY">Maternity</option>
                  <option value="PATERNITY">Paternity</option>
                  <option value="BEREAVEMENT">Bereavement</option>
                  <option value="STUDY">Study Leave</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">Start Date</label>
                <input
                  required
                  type="date"
                  value={newRequest.start_date}
                  onChange={(e) => setNewRequest({ ...newRequest, start_date: e.target.value })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">End Date</label>
                <input
                  required
                  type="date"
                  value={newRequest.end_date}
                  onChange={(e) => setNewRequest({ ...newRequest, end_date: e.target.value })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Reason</label>
              <textarea
                value={newRequest.reason}
                onChange={(e) => setNewRequest({ ...newRequest, reason: e.target.value })}
                className="w-full p-3 rounded-md border border-border bg-background text-sm min-h-[80px]"
                placeholder="Optional reason for your leave request..."
              />
            </div>
          </div>
          
          <div className="flex justify-end gap-3 mt-6">
            <Button variant="outline" type="button" onClick={() => setIsCreating(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Submitting..." : "Submit Request"}
            </Button>
          </div>
        </form>
      )}

      {!isCreating && requests.length === 0 && (
        <div className="bg-surface border border-border rounded-xl p-12 text-center text-muted-foreground flex flex-col items-center">
          <CalendarDays className="w-12 h-12 mb-4 text-muted" />
          <p className="text-lg font-medium text-foreground">No Leave Requests Found</p>
          <p className="mt-2 text-sm">You haven't requested any time off yet.</p>
        </div>
      )}

      {!isCreating && requests.length > 0 && (
        <div className="bg-surface border border-border rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-surface-hover border-b border-border text-xs uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-6 py-4 font-medium">Type</th>
                <th className="px-6 py-4 font-medium">Duration</th>
                <th className="px-6 py-4 font-medium">Days</th>
                <th className="px-6 py-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {requests.map((req) => (
                <tr key={req.id} className="hover:bg-surface-hover/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-foreground">{req.leave_type}</td>
                  <td className="px-6 py-4">
                    {req.start_date} to {req.end_date}
                  </td>
                  <td className="px-6 py-4 font-mono">{req.total_days}</td>
                  <td className="px-6 py-4">
                    <Badge variant={
                      req.status === 'APPROVED' ? 'success' :
                      req.status === 'REJECTED' || req.status === 'CANCELLED' ? 'destructive' : 'warning'
                    }>
                      {req.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
