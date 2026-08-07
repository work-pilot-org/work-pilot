"use client";

import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  colorClass?: string;
}

export function StatCard({ title, value, icon: Icon, trend, trendUp, colorClass = "text-gray-900" }: StatCardProps) {
  return (
    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
      <div className="flex justify-between items-start">
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <div className={`p-2 rounded-lg bg-gray-50`}>
          <Icon className="w-5 h-5 text-gray-400" />
        </div>
      </div>
      <div className="mt-4">
        <p className={`text-3xl font-semibold ${colorClass}`}>{value}</p>
        {trend && (
          <p className={`text-xs font-medium mt-1 ${trendUp ? 'text-green-600' : 'text-red-600'}`}>
            {trendUp ? '↑' : '↓'} {trend}
          </p>
        )}
      </div>
    </div>
  );
}
