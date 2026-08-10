"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  FileText, 
  Settings2, 
  Scale, 
  CalendarDays, 
  PieChart 
} from "lucide-react";

const tabs = [
  { name: "Requests", href: "/dashboard/hr/leave", icon: FileText },
  { name: "Balances", href: "/dashboard/hr/leave/balances", icon: Scale },
  { name: "Types", href: "/dashboard/hr/leave/types", icon: Settings2 },
  { name: "Holidays", href: "/dashboard/hr/leave/holidays", icon: CalendarDays },
  { name: "Reports", href: "/dashboard/hr/leave/reports", icon: PieChart },
];

export default function LeaveLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="space-y-6">
      <div className="border-b border-border">
        <nav className="-mb-px flex space-x-6 overflow-x-auto" aria-label="Tabs">
          {tabs.map((tab) => {
            const isActive = pathname === tab.href;
            const Icon = tab.icon;
            return (
              <Link
                key={tab.name}
                href={tab.href}
                className={`
                  group inline-flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors
                  ${isActive
                    ? "border-primary text-primary"
                    : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
                  }
                `}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"}`} />
                {tab.name}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="pt-2">
        {children}
      </div>
    </div>
  );
}
