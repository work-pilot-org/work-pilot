"use client";

import { ReactNode } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";

export interface QuickActionItem {
  label: string;
  icon: ReactNode;
  onClick: () => void;
  colorClass?: string;
}

interface QuickActionsProps {
  title?: string;
  actions: QuickActionItem[];
}

export function QuickActions({ title = "Quick Actions", actions }: QuickActionsProps) {
  return (
    <Card className="h-full">
      <CardHeader className="border-b border-border/40 pb-4">
        <CardTitle className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">{title}</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {actions.map((action, idx) => (
            <Button
              key={idx}
              variant="outline"
              className={`flex flex-col h-auto py-4 items-center justify-center gap-2 hover:bg-surface-hover/80 ${action.colorClass || ""}`}
              onClick={action.onClick}
            >
              {action.icon}
              <span className="text-xs text-foreground whitespace-normal text-center font-medium">{action.label}</span>
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
