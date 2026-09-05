import { useEffect, useState } from "react";
import { invitationRepository } from "@/repositories/invitationRepository";
import { InvitationResponse } from "@/types/invitation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Mail, CheckCircle2, Clock, XCircle } from "lucide-react";
import toast from "react-hot-toast";
import { InviteEmployeeModal } from "./InviteEmployeeModal";

export function InvitationsTab({ refreshTrigger = 0 }: { refreshTrigger?: number }) {
  const [invitations, setInvitations] = useState<InvitationResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isInviteModalOpen, setIsInviteModalOpen] = useState(false);

  const fetchInvitations = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await invitationRepository.listInvitations();
      setInvitations(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load invitations.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchInvitations();
  }, [refreshTrigger]);

  const handleResend = async (id: string) => {
    try {
      await invitationRepository.resendInvitation(id);
      toast.success("Invitation resent successfully");
      fetchInvitations();
    } catch (error: unknown) {
      toast.error(error instanceof Error ? error.message :  "Failed to resend invitation");
    }
  };

  const handleRevoke = async (id: string) => {
    if (!window.confirm("Are you sure you want to revoke this invitation?")) return;
    try {
      await invitationRepository.revokeInvitation(id);
      toast.success("Invitation revoked successfully");
      fetchInvitations();
    } catch (error: unknown) {
      toast.error(error instanceof Error ? error.message :  "Failed to revoke invitation");
    }
  };

  if (isLoading) {
    return <LoadingState message="Loading invitations..." className="py-12" />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchInvitations} />;
  }

  const getStatusVariant = (status: string) => {
    switch (status) {
      case "PENDING":
        return "warning";
      case "ACCEPTED":
        return "success";
      case "EXPIRED":
        return "secondary";
      case "REVOKED":
        return "destructive";
      default:
        return "default";
    }
  };

  return (
    <div className="space-y-8 mt-2">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">Invitations</h2>
          <p className="text-sm text-gray-500 mt-1">Manage organization invitations and onboarding status.</p>
        </div>
        <Button onClick={() => setIsInviteModalOpen(true)} className="shadow-sm">
          <Mail className="mr-2 h-4 w-4" />
          Invite Employee
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <p className="text-sm font-medium text-gray-500 mb-2">Total Sent</p>
          <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{invitations.length}</h3>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <p className="text-sm font-medium text-gray-500 mb-2">Pending</p>
          <h3 className="text-3xl font-bold text-amber-600 tracking-tight">{invitations.filter(i => i.status === 'PENDING').length}</h3>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <p className="text-sm font-medium text-gray-500 mb-2">Accepted</p>
          <h3 className="text-3xl font-bold text-emerald-600 tracking-tight">{invitations.filter(i => i.status === 'ACCEPTED').length}</h3>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-gray-100 flex flex-col justify-center transition-all hover:shadow-md">
          <p className="text-sm font-medium text-gray-500 mb-2">Expired/Revoked</p>
          <h3 className="text-3xl font-bold text-gray-900 tracking-tight">{invitations.filter(i => i.status === 'EXPIRED' || i.status === 'REVOKED').length}</h3>
        </div>
      </div>

      {invitations.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-12">
          <EmptyState
            title="No invitations found"
            description="There are currently no invitations for this organization."
            icon={<Mail className="w-8 h-8 text-gray-400" />}
          />
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-gray-50 hover:bg-gray-50">
                <TableHead className="font-semibold text-gray-900 py-4">Email</TableHead>
                <TableHead className="font-semibold text-gray-900 py-4">Role</TableHead>
                <TableHead className="font-semibold text-gray-900 py-4">Sent Date</TableHead>
                <TableHead className="font-semibold text-gray-900 py-4">Expiry Date</TableHead>
                <TableHead className="font-semibold text-gray-900 py-4">Status</TableHead>
                <TableHead className="text-right font-semibold text-gray-900 py-4">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {invitations.map((inv) => (
                <TableRow key={inv.id} className="hover:bg-gray-50 transition-colors">
                  <TableCell className="font-medium text-gray-900 py-4">{inv.email}</TableCell>
                  <TableCell className="py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-800">
                      {inv.role.replace("_", " ")}
                    </span>
                  </TableCell>
                  <TableCell className="text-gray-500 py-4">{new Date(inv.created_at).toLocaleDateString()}</TableCell>
                  <TableCell className="text-gray-500 py-4">{new Date(inv.expires_at).toLocaleDateString()}</TableCell>
                  <TableCell className="py-4">
                    <Badge variant={getStatusVariant(inv.status) as any} className="font-medium">
                      {inv.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-2 py-4">
                    {inv.status === "PENDING" && (
                      <div className="flex justify-end gap-2">
                        <Button variant="outline" size="sm" onClick={() => handleResend(inv.id)} className="h-8 shadow-sm">
                          Resend
                        </Button>
                        <Button variant="destructive" size="sm" onClick={() => handleRevoke(inv.id)} className="h-8 shadow-sm bg-red-50 text-red-600 border-red-200 hover:bg-red-100 hover:border-red-300 hover:text-red-700">
                          Revoke
                        </Button>
                      </div>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      <InviteEmployeeModal
        isOpen={isInviteModalOpen}
        onClose={() => setIsInviteModalOpen(false)}
        onSuccess={fetchInvitations}
      />
    </div>
  );
}
