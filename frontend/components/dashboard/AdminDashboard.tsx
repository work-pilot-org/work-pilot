"use client";

import { useAuthStore } from "@/store/authStore";
import { Building2, Users, LayoutDashboard, Settings, Plus, FileText, ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { itRepository } from "@/repositories/itRepository";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
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
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto w-full pb-12">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-2">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Organization Overview
          </h1>
          <p className="text-sm font-medium text-muted-foreground mt-1">
            Welcome back, {user?.name || "Administrator"} • Here's the current operational state
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="primary">
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            <Card className="hover:border-primary/30 transition-colors group cursor-pointer relative overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Total Employees</span>
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <Users className="h-4 w-4 text-primary" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-foreground tracking-tight">
                  {employeeCount !== null ? employeeCount : "—"}
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground/30 absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 group-hover:text-primary transition-all transform translate-x-2 group-hover:translate-x-0" />
              </CardContent>
            </Card>

            <Card className="hover:border-warning/30 transition-colors group cursor-pointer relative overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Active IT Tickets</span>
                  <div className="w-8 h-8 rounded-full bg-warning/10 flex items-center justify-center">
                    <LayoutDashboard className="h-4 w-4 text-warning" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-foreground tracking-tight">
                  {ticketCount !== null ? ticketCount : "—"}
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground/30 absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 group-hover:text-warning transition-all transform translate-x-2 group-hover:translate-x-0" />
              </CardContent>
            </Card>

            <Card className="opacity-70 bg-surface/50">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">Active Projects</span>
                  <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                    <Building2 className="h-4 w-4 text-muted-foreground" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-muted-foreground tracking-tight">—</div>
                <span className="text-[10px] font-medium text-muted-foreground/70 uppercase tracking-widest mt-2 block">No data available</span>
              </CardContent>
            </Card>

            <Card className="opacity-70 bg-surface/50">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">System Status</span>
                  <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                    <Settings className="h-4 w-4 text-muted-foreground" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-foreground tracking-tight">OK</div>
              </CardContent>
            </Card>

          </div>

          {/* Quick Links / Split View */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <Card className="col-span-2 flex flex-col">
              <CardHeader className="border-b border-border/40 pb-4">
                <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                  Organization Activity
                </CardTitle>
              </CardHeader>
              <CardContent className="flex-1 p-12 flex flex-col items-center justify-center text-center bg-surface-hover/20">
                <FileText className="w-8 h-8 text-muted-foreground/40 mb-4" />
                <p className="text-sm font-semibold text-foreground">No recent activity</p>
                <p className="text-[13px] text-muted-foreground mt-1">The activity feed requires backend integration.</p>
              </CardContent>
            </Card>

            <Card className="col-span-1">
              <CardHeader className="border-b border-border/40 pb-4">
                <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 px-3 pb-4">
                <div className="flex flex-col gap-1">
                  <Link href="/dashboard/organization" className="flex items-center justify-between p-3.5 rounded-xl hover:bg-surface-hover/80 transition-colors border border-transparent hover:border-border/40 group">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                        <Users className="w-4 h-4 text-primary" />
                      </div>
                      <span className="text-sm font-semibold text-foreground">Manage Team</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground/50 group-hover:text-foreground transition-colors" />
                  </Link>
                  
                  <Link href="/dashboard/it/tickets" className="flex items-center justify-between p-3.5 rounded-xl hover:bg-surface-hover/80 transition-colors border border-transparent hover:border-border/40 group">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-warning/5 flex items-center justify-center group-hover:bg-warning/10 transition-colors">
                        <LayoutDashboard className="w-4 h-4 text-warning" />
                      </div>
                      <span className="text-sm font-semibold text-foreground">IT Helpdesk</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground/50 group-hover:text-foreground transition-colors" />
                  </Link>
                  
                  <Link href="/dashboard/chat" className="flex items-center justify-between p-3.5 rounded-xl hover:bg-surface-hover/80 transition-colors border border-transparent hover:border-border/40 group">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                        <Settings className="w-4 h-4 text-primary" />
                      </div>
                      <span className="text-sm font-semibold text-foreground">AI Workspace</span>
                    </div>
                    <ArrowRight className="w-4 h-4 text-muted-foreground/50 group-hover:text-foreground transition-colors" />
                  </Link>
                </div>
              </CardContent>
            </Card>
            
          </div>
        </>
      )}
    </div>
  );
}
