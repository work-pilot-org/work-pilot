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
import { Card, CardContent } from "@/components/ui/Card";
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
      const res = await invitationRepository.resendInvitation(id);
      
      if (res.email_sent === false && res.invite_link) {
        toast.error(
          (t) => (
            <div className="flex flex-col space-y-2">
              <span className="font-semibold text-sm">Resent, but the email could not be delivered.</span>
              {res.email_error && (
                <span className="text-xs text-destructive bg-destructive/10 p-1 rounded border border-destructive/20">{res.email_error}</span>
              )}
              <span className="text-xs text-muted-foreground">You can copy the invitation link and send it manually.</span>
              <button 
                onClick={() => {
                  navigator.clipboard.writeText(res.invite_link!);
                  toast.success("Link copied!", { id: t.id });
                }}
                className="mt-2 bg-primary text-primary-foreground text-xs px-2 py-1 rounded w-fit hover:bg-primary/90"
              >
                Copy Link
              </button>
            </div>
          ),
          { duration: 10000 }
        );
      } else {
        toast.success("Invitation resent successfully");
      }
      
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
    <div className="space-y-6 mt-4 pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold tracking-tight text-foreground">Invitations</h2>
          <p className="text-sm text-muted-foreground mt-1">Manage organization invitations and onboarding status.</p>
        </div>
        <Button onClick={() => setIsInviteModalOpen(true)} className="shadow-sm">
          <Mail className="mr-2 h-4 w-4" />
          Invite Employee
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <p className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground mb-4">Total Sent</p>
            <h3 className="text-3xl font-bold text-foreground tracking-tight">{invitations.length}</h3>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <p className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground mb-4">Pending</p>
            <h3 className="text-3xl font-bold text-warning tracking-tight">{invitations.filter(i => i.status === 'PENDING').length}</h3>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <p className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground mb-4">Accepted</p>
            <h3 className="text-3xl font-bold text-success tracking-tight">{invitations.filter(i => i.status === 'ACCEPTED').length}</h3>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <p className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground mb-4">Expired/Revoked</p>
            <h3 className="text-3xl font-bold text-foreground tracking-tight">{invitations.filter(i => i.status === 'EXPIRED' || i.status === 'REVOKED').length}</h3>
          </CardContent>
        </Card>
      </div>

      {invitations.length === 0 ? (
        <Card>
          <CardContent className="p-12">
            <EmptyState
              title="No invitations found"
              description="There are currently no invitations for this organization."
              icon={<Mail className="w-8 h-8 text-muted-foreground/60" />}
            />
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-0">
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
                    <TableCell className="font-medium text-foreground">{inv.email}</TableCell>
                    <TableCell>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-surface-hover text-foreground border border-border/40">
                        {inv.role.replace("_", " ")}
                      </span>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{new Date(inv.created_at).toLocaleDateString()}</TableCell>
                    <TableCell className="text-muted-foreground">{new Date(inv.expires_at).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <Badge variant={getStatusVariant(inv.status) as any} className="font-medium">
                        {inv.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right space-x-2">
                      {inv.status === "PENDING" && (
                        <div className="flex justify-end gap-2">
                          <Button variant="outline" size="sm" onClick={() => handleResend(inv.id)} className="h-8 shadow-sm">
                            Resend
                          </Button>
                          <Button variant="destructive" size="sm" onClick={() => handleRevoke(inv.id)} className="h-8 shadow-sm">
                            Revoke
                          </Button>
                        </div>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      <InviteEmployeeModal
        isOpen={isInviteModalOpen}
        onClose={() => setIsInviteModalOpen(false)}
        onSuccess={fetchInvitations}
      />
    </div>
  );
}
