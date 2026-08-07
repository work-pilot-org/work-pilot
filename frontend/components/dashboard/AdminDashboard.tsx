"use client";

import { useAuthStore } from "@/store/authStore";
import { Building2, Users, Briefcase, Settings } from "lucide-react";
import { StatCard } from "@/components/common/StatCard";

export function AdminDashboard() {
  const { user } = useAuthStore();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">
        Admin Dashboard, {user?.name || "Administrator"}!
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard 
          title="Total Departments" 
          value="—" 
          icon={Building2} 
        />
        <StatCard 
          title="Total Employees" 
          value="—" 
          icon={Users} 
        />
        <StatCard 
          title="Active Projects" 
          value="—" 
          icon={Briefcase} 
        />
        <StatCard 
          title="System Settings" 
          value="OK" 
          icon={Settings} 
        />
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-sm border border-gray-100 min-h-[300px]">
        <h3 className="text-lg font-medium mb-4">Organization Activity Feed</h3>
        <p className="text-gray-500 text-sm italic">No recent activity to display.</p>
      </div>
    </div>
  );
}
