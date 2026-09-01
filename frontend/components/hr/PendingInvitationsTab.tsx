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
import { Mail } from "lucide-react";
import toast from "react-hot-toast";
import { InviteEmployeeModal } from "./InviteEmployeeModal";

export function PendingInvitationsTab({ refreshTrigger = 0 }: { refreshTrigger?: number }) {
  const [invitations, setInvitations] = useState<InvitationResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isInviteModalOpen, setIsInviteModalOpen] = useState(false);

  const fetchInvitations = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await invitationRepository.listPendingInvitations();
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
    <div className="space-y-6 mt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold tracking-tight text-gray-900">Pending Invitations</h2>
        <Button onClick={() => setIsInviteModalOpen(true)}>
          Invite Employee
        </Button>
      </div>

      {invitations.length === 0 ? (
        <EmptyState
          title="No pending invitations"
          description="There are currently no active invitations for this organization."
          icon={<Mail className="w-6 h-6" />}
        />
      ) : (
        <div className="border rounded-lg overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Sent Date</TableHead>
                <TableHead>Expiry Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {invitations.map((inv) => (
                <TableRow key={inv.id}>
                  <TableCell className="font-medium">{inv.email}</TableCell>
                  <TableCell>{inv.role.replace("_", " ")}</TableCell>
                  <TableCell>{new Date(inv.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>{new Date(inv.expires_at).toLocaleDateString()}</TableCell>
                  <TableCell>
                    <Badge variant={getStatusVariant(inv.status) as any}>
                      {inv.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    {inv.status === "PENDING" && (
                      <>
                        <Button variant="outline" size="sm" onClick={() => handleResend(inv.id)}>
                          Resend
                        </Button>
                        <Button variant="destructive" size="sm" onClick={() => handleRevoke(inv.id)}>
                          Revoke
                        </Button>
                      </>
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
