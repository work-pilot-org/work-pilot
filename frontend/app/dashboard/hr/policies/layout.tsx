"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  CalendarDays,
  Clock,
  Briefcase,
  CalendarHeart,
  UserCheck
} from "lucide-react";

const tabs = [
  { name: "Leave", href: "/dashboard/hr/policies/leave", icon: CalendarHeart },
  { name: "Attendance", href: "/dashboard/hr/policies/attendance", icon: Clock },
  { name: "Shift", href: "/dashboard/hr/policies/shift", icon: Briefcase },
  { name: "Holiday", href: "/dashboard/hr/policies/holiday", icon: CalendarDays },
  { name: "Probation", href: "/dashboard/hr/policies/probation", icon: UserCheck },
];

export default function PoliciesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Company Policies</h1>
      </div>
      
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
