"use client";

import { useAuthStore } from "@/store/authStore";
import { Users, ClipboardList, TrendingUp, Calendar } from "lucide-react";
import { StatCard } from "@/components/common/StatCard";

export function ManagerDashboard() {
  const { user } = useAuthStore();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">
        Manager Overview, {user?.name || "Manager"}!
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard 
          title="Team Members" 
          value="—" 
          icon={Users} 
        />
        <StatCard 
          title="Pending Approvals" 
          value="—" 
          icon={ClipboardList} 
          colorClass="text-orange-600"
        />
        <StatCard 
          title="Team Leave Today" 
          value="—" 
          icon={Calendar} 
        />
        <StatCard 
          title="Productivity" 
          value="—" 
          icon={TrendingUp} 
          colorClass="text-green-600"
        />
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-sm border border-gray-100 min-h-[300px]">
        <h3 className="text-lg font-medium mb-4">Team Activity Feed</h3>
        <p className="text-gray-500 text-sm italic">No recent activity to display.</p>
      </div>
    </div>
  );
}
