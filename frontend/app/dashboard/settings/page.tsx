"use client";

import { useAuthStore } from "@/store/authStore";
import { ShieldCheck, User } from "lucide-react";

export default function SettingsPage() {
  const { user } = useAuthStore();

  return (
    <div className="p-6 md:p-8 max-w-5xl mx-auto space-y-8 mt-2">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-primary" />
            Settings
          </h1>
          <p className="text-muted-foreground mt-1">Manage your account and preferences.</p>
        </div>
      </div>

      <div className="bg-surface border border-border rounded-xl shadow-sm p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <User className="w-5 h-5 text-muted-foreground" />
            Profile Information
          </h2>
          <p className="text-sm text-muted-foreground mt-1 mb-4">
            Your current profile information as stored in the system.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Email</label>
              <div className="px-3 py-2 bg-surface-hover rounded-md border border-border text-foreground font-medium">
                {user?.email || "N/A"}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Role</label>
              <div className="px-3 py-2 bg-surface-hover rounded-md border border-border text-foreground font-medium">
                {user?.roles?.[0] || "N/A"}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Tenant / Organization</label>
              <div className="px-3 py-2 bg-surface-hover rounded-md border border-border text-foreground font-medium">
                {user?.domain || "N/A"}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">User ID</label>
              <div className="px-3 py-2 bg-surface-hover rounded-md border border-border text-foreground font-medium text-xs break-all">
                {user?.id || "N/A"}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-surface border border-border rounded-xl shadow-sm p-12 text-center">
        <h3 className="text-lg font-semibold text-foreground mb-2">More settings coming soon</h3>
        <p className="text-muted-foreground">
          Additional account preferences and organization settings will be available in a future update.
        </p>
      </div>
    </div>
  );
}
