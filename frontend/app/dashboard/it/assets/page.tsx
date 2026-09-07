"use client";

import { useEffect, useState } from "react";
import { itRepository } from "@/repositories/itRepository";
import { AssetResponse } from "@/types/it";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { MonitorSmartphone, Search, Plus, Filter } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function AssetsPage() {
  const [assets, setAssets] = useState<AssetResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchKeyword, setSearchKeyword] = useState("");

  const fetchAssets = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await itRepository.getAssets({ search: searchKeyword || undefined });
      setAssets(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load assets.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchAssets();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchKeyword]);

  if (isLoading && assets.length === 0) return <LoadingState message="Loading assets..." className="py-12" />;
  if (error && assets.length === 0) return <ErrorState message={error} onRetry={fetchAssets} />;

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Asset Inventory</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage hardware and software assets across the organization.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button className="shadow-sm">
            <Plus className="mr-2 h-4 w-4" />
            Add Asset
          </Button>
        </div>
      </div>

      {/* Asset Management Area */}
      <div className="flex flex-col space-y-6">
        
        {/* Toolbar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface p-4 rounded-xl border border-border-strong shadow-sm">
          <div className="relative max-w-md w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search assets..." 
              className="flex h-10 w-full rounded-md border border-border bg-transparent px-9 py-2 text-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="h-10 border-border text-muted-foreground bg-transparent">
              <Filter className="mr-2 h-4 w-4" />
              Filter by Status
            </Button>
          </div>
        </div>

        {assets.length === 0 ? (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-12">
            <EmptyState 
              title="No assets found"
              description="There are no assets matching your criteria."
              icon={<MonitorSmartphone className="w-8 h-8 text-muted-foreground" />}
            />
          </div>
        ) : (
          <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Asset Name</TableHead>
                  <TableHead>Serial Number</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assets.map((asset) => (
                  <TableRow key={asset.id} className="group">
                    <TableCell>
                      <span className="font-medium text-foreground group-hover:text-primary transition-colors">
                        {asset.name}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-foreground">{asset.serial_number}</span>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-foreground">{asset.category}</span>
                    </TableCell>
                    <TableCell>
                      <Badge 
                        variant={
                          asset.status === "AVAILABLE" ? "success"
                            : asset.status === "ASSIGNED" ? "secondary"
                            : asset.status === "UNDER_MAINTENANCE" ? "warning"
                            : "destructive"
                        }
                      >
                        {asset.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {new Date(asset.created_at).toLocaleDateString()}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}
