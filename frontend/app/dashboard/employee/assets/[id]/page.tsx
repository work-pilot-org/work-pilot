"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { itRepository } from "@/repositories/itRepository";
import { AssetResponse } from "@/types/it";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ArrowLeft, Laptop } from "lucide-react";
import { hrRepository } from "@/repositories/hrRepository";
import { itApi } from "@/lib/axios";
import { ApiError } from "@/types/auth";
import axios from "axios";

export default function AssetDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [asset, setAsset] = useState<AssetResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadAsset = async () => {
      try {
        setIsLoading(true);
        // We use itApi directly since getAssetById is not in itRepository yet
        const response = await itApi.get<AssetResponse>(`/assets/${id}`);
        setAsset(response.data);
      } catch (err: unknown) {
        if (axios.isAxiosError(err) && err.response?.data) {
          const detail = (err.response.data as ApiError).detail;
          setError(typeof detail === "string" ? detail : "Failed to fetch asset.");
        } else {
          setError(err instanceof Error ? err.message : "Failed to load asset");
        }
      } finally {
        setIsLoading(false);
      }
    };
    if (id) loadAsset();
  }, [id]);

  if (isLoading) return <LoadingState message="Loading asset details..." />;
  if (error) return <ErrorState message={error} />;
  if (!asset) return <ErrorState message="Asset not found." />;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <Button variant="ghost" onClick={() => router.push("/dashboard/employee/assets")} className="mb-4">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to My Assets
      </Button>

      <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
        <div className="p-6 border-b border-border flex items-center justify-between bg-surface-hover/30">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-primary/10 text-primary rounded-lg flex items-center justify-center border border-primary/20">
              <Laptop className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-foreground">{asset.name}</h2>
              <p className="text-sm font-mono text-muted-foreground mt-1">{asset.serial_number || "No Serial"}</p>
            </div>
          </div>
          <Badge variant={asset.status === 'ASSIGNED' ? 'success' : 'secondary'}>
            {asset.status}
          </Badge>
        </div>

        <div className="p-6 grid grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-2">Category</h3>
            <p className="text-sm text-muted-foreground">{asset.category}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
