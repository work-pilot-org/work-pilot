"use client";

import { useEffect, useState } from "react";
import { itRepository } from "@/repositories/itRepository";
import { AccessRequestResponse, CreateAccessRequest } from "@/types/it";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Plus, ShieldCheck, ArrowRight } from "lucide-react";

export function MyAccessRequests() {
  const [requests, setRequests] = useState<AccessRequestResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isCreating, setIsCreating] = useState(false);
  const [newRequest, setNewRequest] = useState<CreateAccessRequest>({
    request_type: "APPLICATION",
    target_resource: "",
    reason: "",
    requested_by: "00000000-0000-0000-0000-000000000000" // Backend ignores this
  });

  const loadRequests = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await itRepository.getMyAccessRequests();
      setRequests(data);
    } catch (err: any) {
      setError(err.message || "Failed to load access requests");
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
      await itRepository.createAccessRequest(newRequest);
      setIsCreating(false);
      setNewRequest({
        request_type: "APPLICATION",
        target_resource: "",
        reason: "",
        requested_by: "00000000-0000-0000-0000-000000000000"
      });
      await loadRequests();
    } catch (err: any) {
      alert(err.message || "Failed to submit request");
      setIsLoading(false);
    }
  };

  if (isLoading && !isCreating && requests.length === 0) return <LoadingState message="Loading your access requests..." />;
  if (error && requests.length === 0) return <ErrorState message={error} />;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">Access Requests</h2>
          <p className="text-muted-foreground mt-1">Request and manage access to IT resources.</p>
        </div>
        <Button onClick={() => setIsCreating(true)} disabled={isCreating}>
          <Plus className="w-4 h-4 mr-2" /> New Request
        </Button>
      </div>

      {isCreating && (
        <form onSubmit={handleCreate} className="bg-surface border border-border rounded-xl p-6 shadow-sm space-y-4">
          <h3 className="text-lg font-semibold mb-4">Request Access</h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">Resource Type</label>
                <select
                  value={newRequest.request_type}
                  onChange={(e) => setNewRequest({ ...newRequest, request_type: e.target.value as any })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                >
                  <option value="APPLICATION">Application</option>
                  <option value="VPN">VPN</option>
                  <option value="DATABASE">Database</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">Target Resource</label>
                <input
                  required
                  type="text"
                  value={newRequest.target_resource}
                  onChange={(e) => setNewRequest({ ...newRequest, target_resource: e.target.value })}
                  className="w-full h-10 px-3 rounded-md border border-border bg-background text-sm"
                  placeholder="e.g. AWS Production, Jira, Production DB"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Reason for Access</label>
              <textarea
                required
                value={newRequest.reason}
                onChange={(e) => setNewRequest({ ...newRequest, reason: e.target.value })}
                className="w-full p-3 rounded-md border border-border bg-background text-sm min-h-[100px]"
                placeholder="Why do you need this access?"
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
          <ShieldCheck className="w-12 h-12 mb-4 text-muted" />
          <p className="text-lg font-medium text-foreground">No Access Requests Found</p>
          <p className="mt-2 text-sm">You haven't requested any special access yet.</p>
        </div>
      )}

      {!isCreating && requests.length > 0 && (
        <div className="bg-surface border border-border rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-surface-hover border-b border-border text-xs uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-6 py-4 font-medium">Type</th>
                <th className="px-6 py-4 font-medium">Target Resource</th>
                <th className="px-6 py-4 font-medium">Date Requested</th>
                <th className="px-6 py-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {requests.map((req) => (
                <tr key={req.id} className="hover:bg-surface-hover/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-foreground">{req.request_type}</td>
                  <td className="px-6 py-4">{req.target_resource}</td>
                  <td className="px-6 py-4 text-muted-foreground">
                    {new Date(req.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant={
                      req.status === 'APPROVED' ? 'success' :
                      req.status === 'REJECTED' || req.status === 'REVOKED' ? 'destructive' : 'secondary'
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
