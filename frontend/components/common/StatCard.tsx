"use client";

import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  colorClass?: string;
}

export function StatCard({ title, value, icon: Icon, trend, trendUp, colorClass = "text-foreground" }: StatCardProps) {
  return (
    <Card>
      <CardContent className="p-6 flex flex-col justify-between h-full">
        <div className="flex justify-between items-start">
          <h3 className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">{title}</h3>
          <div className={`w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center`}>
            <Icon className="w-4 h-4 text-primary" />
          </div>
        </div>
        <div className="mt-4">
          <p className={`text-3xl font-bold tracking-tight ${colorClass}`}>{value}</p>
          {trend && (
            <p className={`text-xs font-medium mt-1 ${trendUp ? 'text-success' : 'text-destructive'}`}>
              {trendUp ? '↑' : '↓'} {trend}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
