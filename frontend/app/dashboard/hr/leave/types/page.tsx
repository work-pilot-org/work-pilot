"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { LeaveTypeResponse } from "@/types/hr";
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
import { Settings2, Plus, X } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

export default function LeaveTypesPage() {
  const [leaveTypes, setLeaveTypes] = useState<LeaveTypeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    days_per_year: 0,
    is_paid: true,
    carry_forward: false,
  });

  const fetchTypes = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getLeaveTypes();
      setLeaveTypes(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load leave types.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTypes();
  }, []);

  if (isLoading) return <LoadingState message="Loading leave types..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchTypes} />;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await hrRepository.createLeaveType(formData);
      setIsModalOpen(false);
      setFormData({ name: "", description: "", days_per_year: 0, is_paid: true, carry_forward: false });
      fetchTypes();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to create leave type");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Leave Types</h1>
        <Button onClick={() => setIsModalOpen(true)} className="gap-2">
          <Plus className="w-4 h-4" />
          Add Leave Type
        </Button>
      </div>

      {leaveTypes.length === 0 ? (
        <EmptyState 
          title="No leave types found"
          description="There are currently no leave types configured."
          icon={<Settings2 className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Days per Year</TableHead>
              <TableHead>Paid</TableHead>
              <TableHead>Carry Forward</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {leaveTypes.map((type) => (
              <TableRow key={type.id}>
                <TableCell className="font-bold">{type.name.replace("_", " ")}</TableCell>
                <TableCell className="text-muted-foreground">{type.description || "-"}</TableCell>
                <TableCell>{type.days_per_year}</TableCell>
                <TableCell>{type.is_paid ? "Yes" : "No"}</TableCell>
                <TableCell>{type.carry_forward ? "Yes" : "No"}</TableCell>
                <TableCell>
                  <Badge variant={type.is_active ? "success" : "secondary"}>
                    {type.is_active ? "Active" : "Inactive"}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh]">
            <div className="flex items-center justify-between p-4 border-b">
              <h2 className="text-lg font-semibold">Add Leave Type</h2>
              <Button variant="ghost" size="sm" onClick={() => setIsModalOpen(false)} className="h-8 w-8 p-0">
                <X className="w-4 h-4" />
              </Button>
            </div>
            
            <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-4 space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Type Name *</Label>
                <Input 
                  id="name" 
                  required 
                  placeholder="e.g. SICK" 
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value.toUpperCase()})}
                />
                <p className="text-xs text-muted-foreground">Must match backend enum (e.g. SICK, CASUAL, EARNED)</p>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Input 
                  id="description" 
                  placeholder="Optional description" 
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="days">Days per Year *</Label>
                <Input 
                  id="days" 
                  type="number" 
                  required 
                  min="0"
                  value={formData.days_per_year}
                  onChange={(e) => setFormData({...formData, days_per_year: parseInt(e.target.value) || 0})}
                />
              </div>
              
              <div className="flex items-center gap-2">
                <input 
                  type="checkbox" 
                  id="is_paid" 
                  checked={formData.is_paid}
                  onChange={(e) => setFormData({...formData, is_paid: e.target.checked})}
                  className="rounded border-gray-300 text-primary focus:ring-primary"
                />
                <Label htmlFor="is_paid" className="cursor-pointer">Is Paid Leave</Label>
              </div>
              
              <div className="flex items-center gap-2">
                <input 
                  type="checkbox" 
                  id="carry_forward" 
                  checked={formData.carry_forward}
                  onChange={(e) => setFormData({...formData, carry_forward: e.target.checked})}
                  className="rounded border-gray-300 text-primary focus:ring-primary"
                />
                <Label htmlFor="carry_forward" className="cursor-pointer">Allow Carry Forward</Label>
              </div>
            </form>
            
            <div className="p-4 border-t bg-gray-50 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleSubmit} disabled={isSubmitting}>
                {isSubmitting ? "Saving..." : "Save Leave Type"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
