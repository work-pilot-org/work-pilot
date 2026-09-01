"use client";

import { useAuthStore } from "@/store/authStore";
import { Building2, Users, LayoutDashboard, Settings, Plus, FileText, ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { itRepository } from "@/repositories/itRepository";
import { Button } from "@/components/ui/Button";
import Link from "next/link";
import { LoadingState } from "@/components/common/LoadingState";

export function AdminDashboard() {
  const { user } = useAuthStore();
  const [employeeCount, setEmployeeCount] = useState<number | null>(null);
  const [ticketCount, setTicketCount] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchMetrics() {
      setIsLoading(true);
      try {
        // We only need the counts, but for now we fetch the arrays since that's what the backend provides
        const [empRes, itRes] = await Promise.all([
          hrRepository.getEmployees().catch(() => []),
          itRepository.getTickets().catch(() => [])
        ]);
        setEmployeeCount(empRes.length);
        setTicketCount(itRes.filter(t => t.status === "OPEN" || t.status === "IN_PROGRESS").length);
      } catch (err) {
        console.error("Failed to load metrics", err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchMetrics();
  }, []);

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">
            Welcome back, {user?.name || "Administrator"}
          </h1>
          <p className="text-muted-foreground mt-1 text-sm">
            Here's what is happening in your organization today.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm">
            <Plus className="mr-2 h-4 w-4" />
            Quick Action
          </Button>
        </div>
      </div>
      
      {isLoading ? (
        <LoadingState message="Loading dashboard metrics..." className="py-12" />
      ) : (
        <>
          {/* Top Metrics Area */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm hover:border-primary/50 transition-colors group cursor-pointer">
              <div className="flex items-center justify-between mb-4">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Users className="h-5 w-5 text-primary" />
                </div>
                <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <div className="text-3xl font-bold text-foreground">
                {employeeCount !== null ? employeeCount : "—"}
              </div>
              <p className="text-sm font-medium text-muted-foreground mt-1">Total Employees</p>
            </div>

            <div className="bg-surface border border-border-strong rounded-xl p-5 shadow-sm hover:border-primary/50 transition-colors group cursor-pointer">
              <div className="flex items-center justify-between mb-4">
                <div className="w-10 h-10 rounded-lg bg-warning/10 flex items-center justify-center">
                  <LayoutDashboard className="h-5 w-5 text-warning" />
                </div>
                <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <div className="text-3xl font-bold text-foreground">
                {ticketCount !== null ? ticketCount : "—"}
              </div>
              <p className="text-sm font-medium text-muted-foreground mt-1">Active IT Tickets</p>
            </div>

            <div className="bg-surface border border-border rounded-xl p-5 shadow-sm opacity-60">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center">
                  <Building2 className="h-5 w-5 text-muted-foreground" />
                </div>
              </div>
              <div className="text-3xl font-bold text-foreground">—</div>
              <p className="text-sm font-medium text-muted-foreground mt-1">Active Projects</p>
              <span className="text-[10px] text-muted-foreground mt-2 block">No data available</span>
            </div>

            <div className="bg-surface border border-border rounded-xl p-5 shadow-sm opacity-60">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center">
                  <Settings className="h-5 w-5 text-muted-foreground" />
                </div>
              </div>
              <div className="text-3xl font-bold text-foreground">OK</div>
              <p className="text-sm font-medium text-muted-foreground mt-1">System Status</p>
            </div>

          </div>

          {/* Quick Links / Split View */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
            
            <div className="col-span-2 bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden flex flex-col">
              <div className="px-6 py-5 border-b border-border bg-surface-hover/30">
                <h3 className="text-base font-semibold text-foreground">Organization Activity</h3>
                <p className="text-xs text-muted-foreground mt-1">Recent events and system logs</p>
              </div>
              <div className="flex-1 p-12 flex flex-col items-center justify-center text-center">
                <FileText className="w-8 h-8 text-muted-foreground/50 mb-3" />
                <p className="text-sm font-medium text-foreground">No recent activity</p>
                <p className="text-xs text-muted-foreground mt-1">The activity feed requires backend integration.</p>
              </div>
            </div>

            <div className="col-span-1 space-y-4">
              <div className="bg-surface border border-border-strong rounded-xl shadow-sm p-5">
                <h3 className="text-sm font-semibold text-foreground mb-4">Quick Links</h3>
                <div className="space-y-2">
                  <Link href="/dashboard/organization" className="flex items-center justify-between p-3 rounded-lg hover:bg-surface-hover border border-transparent transition-colors group">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/5 flex items-center justify-center">
                        <Users className="w-4 h-4 text-primary" />
                      </div>
                      <span className="text-sm font-medium text-foreground">Manage Team</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </Link>
                  <Link href="/dashboard/it/tickets" className="flex items-center justify-between p-3 rounded-lg hover:bg-surface-hover border border-transparent transition-colors group">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-warning/5 flex items-center justify-center">
                        <LayoutDashboard className="w-4 h-4 text-warning" />
                      </div>
                      <span className="text-sm font-medium text-foreground">IT Helpdesk</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </Link>
                  <Link href="/dashboard/chat" className="flex items-center justify-between p-3 rounded-lg hover:bg-surface-hover border border-transparent transition-colors group">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center">
                        <Settings className="w-4 h-4 text-indigo-500" />
                      </div>
                      <span className="text-sm font-medium text-foreground">AI Workspace</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </Link>
                </div>
              </div>
            </div>
            
          </div>
        </>
      )}
    </div>
  );
}
