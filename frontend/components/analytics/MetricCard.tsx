import React from "react";
import { Card, CardContent } from "@/components/ui/Card";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
}

export function MetricCard({ title, value, subtitle, icon }: MetricCardProps) {
  return (
    <Card>
      <CardContent className="p-6 flex flex-col justify-center h-full">
        <div className="flex justify-between items-start">
          <div className="text-muted-foreground text-[11px] font-bold uppercase tracking-widest">{title}</div>
          {icon && <div className="text-muted-foreground/70">{icon}</div>}
        </div>
        <div className="mt-2 text-3xl font-bold tracking-tight text-foreground">{value}</div>
        {subtitle && <div className="mt-1 text-sm text-muted-foreground">{subtitle}</div>}
      </CardContent>
    </Card>
  );
}
