import { EmptyState } from "@/components/common/EmptyState";
import { Laptop } from "lucide-react";

export function ITDashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">IT Administration</h1>
      </div>
      <EmptyState 
        title="IT Dashboard Unavailable"
        description="The IT administration dashboard is not currently available."
        icon={<Laptop className="w-6 h-6" />}
      />
    </div>
  );
}
