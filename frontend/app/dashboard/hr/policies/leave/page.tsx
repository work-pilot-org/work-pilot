"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeavePolicyResponse } from "@/types/hr";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { CalendarHeart, ShieldCheck, Search, Plus, Filter } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { DropdownMenu } from "@/components/ui/DropdownMenu";

export default function LeavePolicyPage() {
  const [policies, setPolicies] = useState<LeavePolicyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPolicies = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getLeavePolicies();
      setPolicies(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave policies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  if (isLoading) return <LoadingState message="Loading policies..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchPolicies} />;

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Leave Policies</h1>
          <p className="text-muted-foreground mt-1 text-sm">Configure organizational leave entitlements and rules.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm">
            <Plus className="mr-2 h-4 w-4" />
            Create Policy
          </Button>
        </div>
      </div>

      <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden flex flex-col">
        
        {/* Toolbar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 border-b border-border bg-surface-hover/30">
          <div className="relative max-w-md w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search policies..." 
              className="flex h-9 w-full rounded-md border border-border bg-surface px-9 py-2 text-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary shadow-sm"
            />
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="h-9 border-border bg-surface text-muted-foreground shadow-sm">
              <Filter className="mr-2 h-4 w-4" />
              Filter
            </Button>
          </div>
        </div>

        {/* Content */}
        {policies.length === 0 ? (
          <div className="p-12">
            <EmptyState 
              title="No Leave Policies"
              description="There are currently no leave policies configured for this workspace."
              icon={<CalendarHeart className="w-8 h-8 text-muted-foreground" />}
            />
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Policy Rule</TableHead>
                <TableHead>Entitlement (Cas/Sick/Earn)</TableHead>
                <TableHead>Carry Forward</TableHead>
                <TableHead>Notice Period</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {policies.map((policy) => (
                <TableRow key={policy.id} className="group hover:bg-surface-hover">
                  <TableCell>
                    <div className="flex flex-col">
                      <span className="font-semibold text-foreground group-hover:text-primary transition-colors flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4 text-muted-foreground" />
                        {policy.name}
                      </span>
                      {policy.description && (
                        <span className="text-xs text-muted-foreground font-medium mt-1 ml-6 max-w-xs truncate">
                          {policy.description}
                        </span>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="text-sm font-medium text-muted-foreground">
                    <span className="text-foreground">{policy.casual_leave_days}</span> <span className="mx-1 opacity-50">/</span>
                    <span className="text-foreground">{policy.sick_leave_days}</span> <span className="mx-1 opacity-50">/</span>
                    <span className="text-foreground">{policy.earned_leave_days}</span>
                  </TableCell>
                  <TableCell>
                    {policy.carry_forward_enabled ? (
                      <Badge variant="outline" className="border-success/30 text-success bg-success/5">
                        Yes (Max: {policy.max_carry_forward})
                      </Badge>
                    ) : (
                      <span className="text-sm text-muted-foreground">No</span>
                    )}
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {policy.minimum_notice_days} days
                  </TableCell>
                  <TableCell>
                    <Badge variant={policy.is_active ? "success" : "secondary"}>
                      {policy.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu 
                      items={[
                        { label: "Edit Policy", onClick: () => {} },
                        { label: "View Assignments", onClick: () => {} },
                        { label: "Deactivate", onClick: () => {} }
                      ]}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
