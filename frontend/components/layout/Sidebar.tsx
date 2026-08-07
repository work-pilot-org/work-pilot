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
import { RequireRole } from "@/components/RequireRole";

export interface NavItem {
  name: string;
  href: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  icon: React.ElementType;
  allowedRoles?: string[];
  children?: Omit<NavItem, 'children'>[];
}

const navConfig: NavItem[] = [
  { 
    name: "Dashboard", 
    href: "/dashboard", 
    icon: LayoutDashboard
    // globally accessible — TENANT_ADMIN, MANAGER land here
  },
  { 
    name: "My Workspace",
    href: "/dashboard/employee",
    icon: LayoutDashboard,
    allowedRoles: ["EMPLOYEE"],
  },
  { 
    name: "HR", 
    href: "/dashboard/hr", 
    icon: Users,
    allowedRoles: ["TENANT_ADMIN", "HR_ADMIN", "MANAGER"],
    children: [
      { name: "Employees",    href: "/dashboard/hr",              icon: Users,      allowedRoles: ["TENANT_ADMIN", "HR_ADMIN"] },
      { name: "Attendance",   href: "/dashboard/hr/attendance",   icon: UserCheck,  allowedRoles: ["TENANT_ADMIN", "HR_ADMIN", "MANAGER"] },
      { name: "Leave",        href: "/dashboard/hr/leave",        icon: Calendar,   allowedRoles: ["TENANT_ADMIN", "HR_ADMIN"] },
      { name: "Organization", href: "/dashboard/hr/organization", icon: Building2,  allowedRoles: ["TENANT_ADMIN", "HR_ADMIN"] },
    ]
  },
  {
    name: "IT Service",
    href: "/dashboard/it/tickets",
    icon: LayoutDashboard,
    allowedRoles: ["TENANT_ADMIN", "IT_ADMIN"],
    children: [
      { name: "Helpdesk", href: "/dashboard/it/tickets", icon: LayoutDashboard, allowedRoles: ["TENANT_ADMIN", "IT_ADMIN"] }
    ]
  },
  {
    name: "Workflows",
    href: "/dashboard/workflows",
    icon: Briefcase,
    allowedRoles: ["TENANT_ADMIN", "MANAGER"],
  }
];


export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const [expandedNav, setExpandedNav] = useState<string[]>(["HR"]);

  const visibleNavItems = navConfig;

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
                      
                      if (child.allowedRoles && child.allowedRoles.length > 0) {
                        return (
                          <RequireRole key={child.name} allowedRoles={child.allowedRoles}>
                            {childNode}
                          </RequireRole>
                        );
                      }
                      return childNode;
                    })}
                  </ul>
                )}
              </li>
            );

            if (item.allowedRoles && item.allowedRoles.length > 0) {
              return (
                <RequireRole key={item.name} allowedRoles={item.allowedRoles}>
                  {navItemContent}
                </RequireRole>
              );
            }
            return navItemContent;
          })}
        </ul>
      </nav>

    </aside>
  );
}
