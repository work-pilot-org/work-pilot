"use client";

import { useAuthStore } from "@/store/authStore";
import { Users, Clock, Calendar, CheckCircle } from "lucide-react";
import { StatCard } from "@/components/common/StatCard";

export function HRDashboard() {
  const { user } = useAuthStore();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">
        HR Overview, {user?.name || "HR Admin"}!
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard 
          title="Total Employees" 
          value="—" 
          icon={Users} 
        />
        <StatCard 
          title="Present Today" 
          value="—" 
          icon={CheckCircle} 
          colorClass="text-green-600"
        />
        <StatCard 
          title="On Leave" 
          value="—" 
          icon={Calendar} 
          colorClass="text-purple-600"
        />
        <StatCard 
          title="Pending Reviews" 
          value="—" 
          icon={Clock} 
          colorClass="text-orange-600"
        />
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-sm border border-gray-100 min-h-[300px]">
        <h3 className="text-lg font-medium mb-4">HR Activity Feed</h3>
        <p className="text-gray-500 text-sm italic">No recent activity to display.</p>
      </div>
    </div>
  );
}
