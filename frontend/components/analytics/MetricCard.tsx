import React from "react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
}

export function MetricCard({ title, value, subtitle, icon }: MetricCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6 flex flex-col justify-center">
      <div className="flex justify-between items-start">
        <div className="text-gray-500 text-sm font-medium">{title}</div>
        {icon && <div className="text-gray-400">{icon}</div>}
      </div>
      <div className="mt-2 text-3xl font-semibold text-gray-900">{value}</div>
      {subtitle && <div className="mt-1 text-sm text-gray-500">{subtitle}</div>}
    </div>
  );
}
