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
  ShieldCheck,
  Mail,
  BarChart3,
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
    icon: LayoutDashboard,
    allowedRoles: ["EMPLOYEE", "MANAGER", "HR_ADMIN", "IT_ADMIN", "ORG_ADMIN"]
  },
  
  // EMPLOYEE SPECIFIC ROUTES
  { name: "My Profile", href: "/dashboard/employee/profile", icon: Users, allowedRoles: ["EMPLOYEE"] },
  { name: "Attendance", href: "/dashboard/employee/attendance", icon: Calendar, allowedRoles: ["EMPLOYEE"] },
  { name: "My Leave", href: "/dashboard/employee/leave", icon: Calendar, allowedRoles: ["EMPLOYEE"] },
  { name: "My Tickets", href: "/dashboard/employee/tickets", icon: LayoutDashboard, allowedRoles: ["EMPLOYEE"] },
  { name: "My Assets", href: "/dashboard/employee/assets", icon: Briefcase, allowedRoles: ["EMPLOYEE"] },
  { name: "Access Requests", href: "/dashboard/employee/access", icon: ShieldCheck, allowedRoles: ["EMPLOYEE"] },
  { name: "Knowledge", href: "/dashboard/employee/knowledge", icon: Building2, allowedRoles: ["EMPLOYEE"] },

  // MANAGER SPECIFIC ROUTES
  { name: "My Team", href: "/dashboard/manager/team", icon: Users, allowedRoles: ["MANAGER"] },
  { name: "Team Attendance", href: "/dashboard/manager/attendance", icon: Calendar, allowedRoles: ["MANAGER"] },
  { name: "Leave & Approvals", href: "/dashboard/manager/leave", icon: ShieldCheck, allowedRoles: ["MANAGER"] },
  { name: "Team Tickets", href: "/dashboard/manager/tickets", icon: LayoutDashboard, allowedRoles: ["MANAGER"] },
  { name: "Team Analytics", href: "/dashboard/manager/analytics", icon: BarChart3, allowedRoles: ["MANAGER"] },

  // HR ADMIN ROUTES
  { 
    name: "HR Admin", 
    href: "/dashboard/hr", 
    icon: Users,
    allowedRoles: ["HR_ADMIN"],
    children: [
      { name: "Employees", href: "/dashboard/hr/employees", icon: Users, allowedRoles: ["HR_ADMIN"] },
      { name: "Departments", href: "/dashboard/hr/departments", icon: Building2, allowedRoles: ["HR_ADMIN"] },
      { name: "Attendance", href: "/dashboard/hr/attendance", icon: UserCheck, allowedRoles: ["HR_ADMIN"] },
      { name: "Leave", href: "/dashboard/hr/leave", icon: Calendar, allowedRoles: ["HR_ADMIN"] },
      { name: "Leave Policies", href: "/dashboard/hr/policies", icon: ShieldCheck, allowedRoles: ["HR_ADMIN"] },
      { name: "Onboarding", href: "/dashboard/hr/onboarding", icon: UserCheck, allowedRoles: ["HR_ADMIN"] },
      { name: "Offboarding", href: "/dashboard/hr/offboarding", icon: UserCheck, allowedRoles: ["HR_ADMIN"] },
      { name: "Analytics", href: "/dashboard/hr/analytics", icon: BarChart3, allowedRoles: ["HR_ADMIN"] },
    ]
  },

  // IT ADMIN ROUTES
  {
    name: "IT Admin",
    href: "/dashboard/it",
    icon: LayoutDashboard,
    allowedRoles: ["IT_ADMIN"],
    children: [
      { name: "Tickets", href: "/dashboard/it/tickets", icon: LayoutDashboard, allowedRoles: ["IT_ADMIN"] },
      { name: "Assets", href: "/dashboard/it/assets", icon: Briefcase, allowedRoles: ["IT_ADMIN"] },
      { name: "Devices", href: "/dashboard/it/devices", icon: Briefcase, allowedRoles: ["IT_ADMIN"] },
      { name: "Access Requests", href: "/dashboard/it/access", icon: ShieldCheck, allowedRoles: ["IT_ADMIN"] },
      { name: "Software / Licenses", href: "/dashboard/it/software", icon: Briefcase, allowedRoles: ["IT_ADMIN"] },
      { name: "Knowledge", href: "/dashboard/it/knowledge", icon: Building2, allowedRoles: ["IT_ADMIN"] },
      { name: "Analytics", href: "/dashboard/it/analytics", icon: BarChart3, allowedRoles: ["IT_ADMIN"] },
    ]
  },

  // ORG ADMIN ROUTES
  { 
    name: "Organization", 
    href: "/dashboard/organization", 
    icon: Building2,
    allowedRoles: ["ORG_ADMIN"],
    children: [
      { name: "Overview", href: "/dashboard/organization/overview", icon: BarChart3, allowedRoles: ["ORG_ADMIN"] },
      { name: "Employees", href: "/dashboard/organization/employees", icon: Users, allowedRoles: ["ORG_ADMIN"] },
      { name: "Invitations", href: "/dashboard/organization/invitations", icon: Mail, allowedRoles: ["ORG_ADMIN"] },
      { name: "Analytics", href: "/dashboard/organization/analytics", icon: BarChart3, allowedRoles: ["ORG_ADMIN"] },
    ]
  },
  
  // CROSS-ROLE ROUTES
  {
    name: "Workflows",
    href: "/dashboard/workflows",
    icon: Briefcase,
    allowedRoles: ["ORG_ADMIN"],
  },
  {
    name: "Notifications",
    href: "/dashboard/notifications",
    icon: Mail,
    allowedRoles: ["EMPLOYEE", "MANAGER", "HR_ADMIN", "IT_ADMIN", "ORG_ADMIN"]
  },
  {
    name: "AI Assistant",
    href: "/dashboard/chat",
    icon: Briefcase,
    allowedRoles: ["EMPLOYEE", "MANAGER", "HR_ADMIN", "IT_ADMIN", "ORG_ADMIN"],
  },
  {
    name: "Settings",
    href: "/dashboard/settings",
    icon: ShieldCheck,
    allowedRoles: ["EMPLOYEE", "MANAGER", "HR_ADMIN", "IT_ADMIN", "ORG_ADMIN"]
  }
];


export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const [expandedNav, setExpandedNav] = useState<string[]>(["HR", "IT Service"]);

  const visibleNavItems = navConfig;

  const toggleExpand = (name: string) => {
    setExpandedNav(prev => 
      prev.includes(name) ? prev.filter(n => n !== name) : [...prev, name]
    );
  };

  return (
    <aside className="w-64 bg-surface border-r border-border hidden md:flex flex-col h-full z-20 shadow-sm transition-all duration-300">
      <div className="h-16 px-6 border-b border-border flex items-center gap-3">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center shadow-sm">
          <Briefcase className="w-4 h-4 text-white" />
        </div>
        <div className="flex flex-col">
          <h2 className="font-semibold text-foreground tracking-tight leading-none text-lg">WorkPilot</h2>
          <p className="text-[10px] text-muted-foreground font-semibold uppercase tracking-widest mt-1">
            {user?.domain ? user.domain : "WORKSPACE"}
          </p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto py-6">
        <div className="px-4 mb-2">
          <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Main Menu</p>
        </div>
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
                    className={`flex-1 flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all group ${
                      isActive && !hasChildren
                        ? "bg-primary text-primary-foreground shadow-sm"
                        : "text-muted-foreground hover:bg-surface-hover hover:text-foreground"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className={`w-4 h-4 transition-colors ${isActive && !hasChildren ? "text-primary-foreground" : "text-muted-foreground group-hover:text-foreground"}`} />
                      {item.name}
                    </div>
                    {hasChildren && (
                      isExpanded ? <ChevronDown className="w-4 h-4 opacity-50 transition-transform" /> : <ChevronRight className="w-4 h-4 opacity-50 transition-transform" />
                    )}
                  </Link>
                </div>

                {hasChildren && (
                  <div className={`overflow-hidden transition-all duration-200 ease-in-out ${isExpanded ? 'max-h-96 opacity-100 mt-1' : 'max-h-0 opacity-0'}`}>
                    <ul className="mb-2 ml-4 space-y-1 border-l-2 border-border pl-3">
                      {item.children!.map((child) => {
                        const isChildLinkActive = pathname === child.href;
                        const childNode = (
                          <li key={child.name}>
                            <Link
                              href={child.href}
                              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                                isChildLinkActive
                                  ? "bg-primary/10 text-primary font-semibold"
                                  : "text-muted-foreground hover:bg-surface-hover hover:text-foreground"
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
                  </div>
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
