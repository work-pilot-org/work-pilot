"use client";

import { useAuthStore } from "@/store/authStore";
import { useRouter, usePathname } from "next/navigation";
import { useState, useRef, useEffect } from "react";
import { LogOut, Bell, User, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/Button";

function getContextualInfo(pathname: string) {
  if (pathname.includes("/dashboard/hr")) return { title: "Human Resources", subtitle: "Manage your organization and team members" };
  if (pathname.includes("/dashboard/it")) return { title: "IT Service & Helpdesk", subtitle: "Manage tickets, hardware, and service health" };
  if (pathname.includes("/dashboard/workflows")) return { title: "Workflows & Approvals", subtitle: "Manage your pending actions" };
  if (pathname.includes("/dashboard/chat")) return { title: "WorkPilot AI", subtitle: "Your intelligent assistant" };
  return { title: "Dashboard", subtitle: "Overview and recent activity" };
}

export default function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const profileRef = useRef<HTMLDivElement>(null);

  const context = getContextualInfo(pathname || "");

  const handleLogout = async () => {
    try {
      setIsLoggingOut(true);
      await logout();
      const { getBaseDomainUrl } = await import("@/lib/auth");
      window.location.href = getBaseDomainUrl("/login?logout=true");
    } catch (error) {
      console.error("Logout failed", error);
      setIsLoggingOut(false);
    }
  };

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (profileRef.current && !profileRef.current.contains(event.target as Node)) {
        setIsProfileOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <header className="h-16 bg-surface border-b border-border flex items-center justify-between px-8 sticky top-0 z-30 shadow-sm">
      
      {/* Contextual Information Area */}
      <div className="flex flex-col justify-center">
        <h2 className="text-lg font-semibold text-foreground leading-tight tracking-tight">
          {context.title}
        </h2>
        <span className="text-xs text-muted-foreground font-medium hidden sm:block">
          {context.subtitle}
        </span>
      </div>
      
      <div className="flex-1 md:hidden"></div>

      {/* Right side actions */}
      <div className="flex items-center gap-4 ml-auto">
        <Button variant="outline" size="sm" className="relative h-9 w-9 p-0 rounded-full text-muted-foreground hover:text-foreground border-transparent hover:bg-surface-hover shadow-none">
          <Bell className="w-4 h-4" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full ring-2 ring-surface"></span>
        </Button>

        <div className="h-6 w-px bg-border hidden sm:block"></div>
        
        {/* Profile Dropdown */}
        <div className="relative" ref={profileRef}>
          <button 
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="flex items-center gap-3 hover:bg-surface-hover p-1.5 pr-2 rounded-full transition-colors border border-transparent hover:border-border-strong"
          >
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-sm shadow-sm">
              {user?.name?.charAt(0).toUpperCase() || "U"}
            </div>
            <div className="text-sm hidden sm:flex flex-col items-start mr-1">
              <span className="font-semibold text-foreground leading-none">{user?.name || "User"}</span>
              <span className="text-xs text-muted-foreground mt-0.5">{user?.domain || "Admin"}</span>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-muted-foreground hidden sm:block" />
          </button>

          {isProfileOpen && (
            <div className="absolute right-0 mt-2 w-56 bg-surface rounded-xl shadow-lg border border-border-strong py-1 z-50">
              <div className="px-4 py-3 border-b border-border bg-surface-hover rounded-t-xl mx-1 mt-1">
                <p className="text-sm font-semibold text-foreground truncate">{user?.name}</p>
                <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
              </div>
              <div className="py-2">
                <button className="w-full text-left px-4 py-2 text-sm text-foreground hover:bg-surface-hover flex items-center gap-2 font-medium">
                  <User className="w-4 h-4 text-muted-foreground" />
                  Profile Settings
                </button>
              </div>
              <div className="py-2 border-t border-border">
                <button
                  onClick={handleLogout}
                  disabled={isLoggingOut}
                  className="w-full text-left px-4 py-2 text-sm text-destructive hover:bg-destructive/10 flex items-center gap-2 font-medium disabled:opacity-50 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  {isLoggingOut ? "Signing out..." : "Sign out"}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

