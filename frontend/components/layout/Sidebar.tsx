"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import { 
  LayoutDashboard, 
  Users, 
  Briefcase,
  ChevronDown,
  ChevronRight,
  UserCheck,
  Calendar,
  Building2,
} from "lucide-react";
import { useState } from "react";
import { RequirePermission } from "@/components/RequirePermission";

export type Permission = string; // Future: define specific permission strings

export interface NavItem {
  name: string;
  href: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  icon: any;
  requiredPermissions?: Permission[];
  children?: Omit<NavItem, 'children'>[];
}

const navConfig: NavItem[] = [
  { 
    name: "Dashboard", 
    href: "/dashboard", 
    icon: LayoutDashboard 
    // globally accessible, no requiredPermissions
  },
  { 
    name: "HR", 
    href: "/dashboard/hr", 
    icon: Users,
    requiredPermissions: ["hr:manage"],
    children: [
      { name: "Employees", href: "/dashboard/hr", icon: Users, requiredPermissions: ["employee:manage"] },
      { name: "Attendance", href: "/dashboard/hr/attendance", icon: UserCheck, requiredPermissions: ["attendance:read"] },
      { name: "Leave", href: "/dashboard/hr/leave", icon: Calendar, requiredPermissions: ["hr:manage"] },
      { name: "Organization", href: "/dashboard/hr/organization", icon: Building2, requiredPermissions: ["organization:manage"] },
    ]
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const [expandedNav, setExpandedNav] = useState<string[]>(["HR"]);

  // Future RBAC Filter: 
  // const userPermissions = user?.permissions || [];
  // const visibleNavItems = navConfig.filter(item => hasPermission(item, userPermissions));
  
  const visibleNavItems = navConfig; // Currently rendering everything without filtering

  const toggleExpand = (name: string) => {
    setExpandedNav(prev => 
      prev.includes(name) ? prev.filter(n => n !== name) : [...prev, name]
    );
  };

  return (
    <aside className="w-64 bg-[#f8f9fa] border-r border-border hidden md:flex flex-col h-full z-20">
      <div className="p-4 border-b border-border flex items-center gap-3 bg-white">
        <div className="w-8 h-8 bg-primary rounded flex items-center justify-center shadow-sm">
          <Briefcase className="w-4 h-4 text-white" />
        </div>
        <div>
          <h2 className="font-semibold text-foreground tracking-tight leading-tight">WorkPilot</h2>
          <p className="text-[11px] text-muted-foreground font-medium uppercase tracking-wider">
            {user?.domain ? user.domain : "WORKSPACE"}
          </p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {visibleNavItems.map((item) => {
            const isExactActive = pathname === item.href;
            const isChildActive = item.href !== "/dashboard" && pathname.startsWith(`${item.href}/`);
            const isActive = isExactActive || isChildActive;
            const isExpanded = expandedNav.includes(item.name);
            const Icon = item.icon;
            const hasChildren = item.children && item.children.length > 0;
            
            const navItemContent = (
              <li key={item.name} className="flex flex-col">
                <div className="flex items-center">
                  <Link
                    href={hasChildren ? "#" : item.href}
                    onClick={(e) => {
                      if (hasChildren) {
                        e.preventDefault();
                        toggleExpand(item.name);
                      }
                    }}
                    className={`flex-1 flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-all ${
                      isActive && !hasChildren
                        ? "bg-primary/10 text-primary"
                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className={`w-4 h-4 ${isActive && !hasChildren ? "text-primary" : "text-muted-foreground"}`} />
                      {item.name}
                    </div>
                    {hasChildren && (
                      isExpanded ? <ChevronDown className="w-4 h-4 opacity-50" /> : <ChevronRight className="w-4 h-4 opacity-50" />
                    )}
                  </Link>
                </div>

                {hasChildren && isExpanded && (
                  <ul className="mt-1 mb-2 ml-6 space-y-1 border-l border-border pl-2">
                    {item.children!.map((child) => {
                      const isChildLinkActive = pathname === child.href;
                      const childNode = (
                        <li key={child.name}>
                          <Link
                            href={child.href}
                            className={`flex items-center gap-3 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                              isChildLinkActive
                                ? "bg-primary/10 text-primary"
                                : "text-muted-foreground hover:bg-muted hover:text-foreground"
                            }`}
                          >
                            {child.name}
                          </Link>
                        </li>
                      );
                      
                      if (child.requiredPermissions && child.requiredPermissions.length > 0) {
                        return (
                          <RequirePermission key={child.name} requiredPermissions={child.requiredPermissions}>
                            {childNode}
                          </RequirePermission>
                        );
                      }
                      return childNode;
                    })}
                  </ul>
                )}
              </li>
            );

            if (item.requiredPermissions && item.requiredPermissions.length > 0) {
              return (
                <RequirePermission key={item.name} requiredPermissions={item.requiredPermissions}>
                  {navItemContent}
                </RequirePermission>
              );
            }
            return navItemContent;
          })}
        </ul>
      </nav>

    </aside>
  );
}
