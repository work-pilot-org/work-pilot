"use client";

import { useAuthStore } from "@/store/authStore";
import { LayoutDashboard } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/common/EmptyState";

export default function DashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Welcome Section */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">
            Welcome, {user?.name?.split(' ')[0] || "Admin"}
          </CardTitle>
          <CardDescription className="max-w-2xl text-base mt-2">
            Manage your organization's resources, monitor system status, and access workflows from your central dashboard.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Link href="/dashboard/hr" passHref legacyBehavior>
            <Button variant="primary">Go to HR Module</Button>
          </Link>
        </CardContent>
      </Card>

      {/* KPI Cards (Empty State because no backend data exists currently) */}
      <div className="grid grid-cols-1">
        <EmptyState
          title="No Metrics Available"
          description="Dashboard statistics and KPI metrics have not been configured for your workspace yet."
          icon={<LayoutDashboard className="h-6 w-6" />}
        />
      </div>
    </div>
  );
}
