"use client";

import { useEffect, useState } from "react";
import { itRepository } from "@/repositories/itRepository";
import { AssetResponse } from "@/types/it";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Laptop, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export function MyAssets() {
  const router = useRouter();
  const [assets, setAssets] = useState<AssetResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAssets = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await itRepository.getMyAssets();
      setAssets(data);
    } catch (err: any) {
      setError(err.message || "Failed to load assets");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAssets();
  }, []);

  if (isLoading && assets.length === 0) return <LoadingState message="Loading your assigned assets..." />;
  if (error && assets.length === 0) return <ErrorState message={error} />;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">My Assets</h2>
          <p className="text-muted-foreground mt-1">View IT assets assigned to you.</p>
        </div>
      </div>

      {assets.length === 0 && (
        <div className="bg-surface border border-border rounded-xl p-12 text-center text-muted-foreground flex flex-col items-center">
          <Laptop className="w-12 h-12 mb-4 text-muted" />
          <p className="text-lg font-medium text-foreground">No Assets Assigned</p>
          <p className="mt-2 text-sm">You do not have any IT assets assigned to you currently.</p>
        </div>
      )}

      {assets.length > 0 && (
        <div className="bg-surface border border-border rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-surface-hover border-b border-border text-xs uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="px-6 py-4 font-medium">Asset Name</th>
                <th className="px-6 py-4 font-medium">Category</th>
                <th className="px-6 py-4 font-medium">Serial Number</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {assets.map((asset) => (
                <tr key={asset.id} className="hover:bg-surface-hover/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-foreground">
                    <div className="flex items-center gap-3">
                      <Laptop className="w-4 h-4 text-muted-foreground" />
                      {asset.name}
                    </div>
                  </td>
                  <td className="px-6 py-4">{asset.category}</td>
                  <td className="px-6 py-4 font-mono text-xs text-muted-foreground">{asset.serial_number || "—"}</td>
                  <td className="px-6 py-4">
                    <Badge variant={asset.status === 'ASSIGNED' ? 'success' : 'secondary'}>
                      {asset.status}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button variant="ghost" size="sm" onClick={() => router.push(`/dashboard/employee/assets/${asset.id}`)}>
                      View <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
