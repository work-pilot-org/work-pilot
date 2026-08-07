"use client";

import { ReactNode } from "react";
import { Button } from "@/components/ui/Button";

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
    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-full">
      <h3 className="text-sm font-medium text-gray-500 mb-4">{title}</h3>
      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {actions.map((action, idx) => (
          <Button
            key={idx}
            variant="outline"
            className={`flex flex-col h-auto py-4 items-center justify-center gap-2 hover:bg-gray-50 ${action.colorClass || ""}`}
            onClick={action.onClick}
          >
            {action.icon}
            <span className="text-xs text-gray-700 whitespace-normal text-center">{action.label}</span>
          </Button>
        ))}
      </div>
    </div>
  );
}
