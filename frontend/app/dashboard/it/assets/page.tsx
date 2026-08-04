
"use client";
import { EmptyState } from "@/components/common/EmptyState";
import { HeadphonesIcon } from "lucide-react";
export default function AssetsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">Asset Inventory</h1>
      {/* Backend Blocked: Missing Asset APIs */}
      <EmptyState title="Backend Blocker" description="IT Asset Management APIs are missing from the backend." icon={<HeadphonesIcon className="w-6 h-6" />} />
    </div>
  );
}
