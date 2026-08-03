"use client";

import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";
import { useState, useRef, useEffect } from "react";
import { LogOut, Bell, Search, User, ChevronDown } from "lucide-react";
import { Input } from "@/components/ui/Input";

export default function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const profileRef = useRef<HTMLDivElement>(null);

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
    <header className="h-14 bg-white border-b border-border flex items-center justify-between px-6 sticky top-0 z-10 shadow-sm">
      {/* Mobile Title / Logo area */}
      <div className="font-semibold text-gray-900 md:hidden tracking-tight">
        WorkPilot
      </div>
      
      {/* Search area */}
      <div className="hidden md:flex flex-1 max-w-md items-center relative">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input 
          type="search" 
          placeholder="Search..." 
          className="w-full bg-muted/50 pl-9 border-transparent focus-visible:bg-white focus-visible:border-border"
        />
      </div>

      <div className="flex-1 md:hidden"></div>

      {/* Right side actions */}
      <div className="flex items-center gap-4 ml-auto">
        <button className="text-muted-foreground hover:text-foreground transition-colors relative p-1" aria-label="Notifications">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full border-2 border-white"></span>
        </button>

        <div className="h-5 w-px bg-border hidden sm:block"></div>
        
        {/* Profile Dropdown */}
        <div className="relative" ref={profileRef}>
          <button 
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="flex items-center gap-2 hover:bg-muted/50 p-1.5 rounded-md transition-colors"
          >
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-semibold text-sm">
              {user?.name?.charAt(0).toUpperCase() || "U"}
            </div>
            <div className="text-sm hidden sm:flex flex-col items-start">
              <span className="font-medium text-foreground leading-none">{user?.name || "User"}</span>
              <span className="text-xs text-muted-foreground mt-1">{user?.domain || "Admin"}</span>
            </div>
            <ChevronDown className="w-4 h-4 text-muted-foreground hidden sm:block" />
          </button>

          {isProfileOpen && (
            <div className="absolute right-0 mt-1 w-56 bg-white rounded-md shadow-lg border border-border py-1 z-50">
              <div className="px-4 py-2 border-b border-border">
                <p className="text-sm font-medium text-foreground truncate">{user?.name}</p>
                <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
              </div>
              <div className="py-1">
                <button className="w-full text-left px-4 py-2 text-sm text-foreground hover:bg-muted flex items-center gap-2">
                  <User className="w-4 h-4 text-muted-foreground" />
                  Profile Settings
                </button>
              </div>
              <div className="py-1 border-t border-border">
                <button
                  onClick={handleLogout}
                  disabled={isLoggingOut}
                  className="w-full text-left px-4 py-2 text-sm text-destructive hover:bg-red-50 flex items-center gap-2 disabled:opacity-50"
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
