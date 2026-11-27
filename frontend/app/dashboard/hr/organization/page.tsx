"use client";

import { useState, useEffect } from "react";
import { RequireRole } from "@/components/RequireRole";
import { Users, Building2, Briefcase, Plus, MoreVertical, Edit2, Trash2 } from "lucide-react";
import { EmptyState } from "@/components/common/EmptyState";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { hrRepository } from "@/repositories/hrRepository";
import { DepartmentResponse } from "@/types/hr";
import { Button } from "@/components/ui/Button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { DropdownMenu } from "@/components/ui/DropdownMenu";

export default function OrganizationPage() {
  const [activeTab, setActiveTab] = useState<"DEPARTMENTS" | "DESIGNATIONS">("DEPARTMENTS");
  const [departments, setDepartments] = useState<DepartmentResponse[]>([]);
  const [designations, setDesignations] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [deps, desigs] = await Promise.all([
        hrRepository.getDepartments().catch(() => []),
        hrRepository.getDesignations().catch(() => [])
      ]);
      setDepartments(deps);
      setDesignations(desigs);
    } catch (err: unknown) {
      setError("Failed to load organizational structure.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading organization context..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;

  return (
    <RequireRole allowedRoles={["ORG_ADMIN", "HR_ADMIN"]}>
      <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground">Organization Management</h1>
            <p className="text-muted-foreground mt-1 text-sm">Configure departments, teams, and standardized job designations.</p>
          </div>
          <Button className="shadow-sm">
            <Plus className="mr-2 h-4 w-4" />
            Add {activeTab === "DEPARTMENTS" ? "Department" : "Designation"}
          </Button>
        </div>

        {/* Tabs & Content */}
        <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden flex flex-col">
          <div className="px-6 border-b border-border bg-surface-hover/30">
            <nav className="flex space-x-6">
              <button 
                onClick={() => setActiveTab("DEPARTMENTS")} 
                className={`flex items-center gap-2 py-4 px-1 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === "DEPARTMENTS" 
                    ? "border-primary text-primary" 
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                <Building2 className="w-4 h-4" />
                Departments
              </button>
              <button 
                onClick={() => setActiveTab("DESIGNATIONS")} 
                className={`flex items-center gap-2 py-4 px-1 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === "DESIGNATIONS" 
                    ? "border-primary text-primary" 
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                <Briefcase className="w-4 h-4" />
                Designations
              </button>
            </nav>
          </div>

          <div className="p-0">
            {activeTab === "DEPARTMENTS" && (
              departments.length === 0 ? (
                <div className="p-12">
                  <EmptyState 
                    title="No departments configured" 
                    description="Create your first department to organize employees." 
                    icon={<Building2 className="w-8 h-8 text-muted-foreground" />} 
                  />
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Department Name</TableHead>
                      <TableHead>Manager ID</TableHead>
                      <TableHead>Code</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {departments.map((dept: any) => (
                      <TableRow key={dept.id} className="group hover:bg-surface-hover">
                        <TableCell className="font-medium text-foreground">{dept.name}</TableCell>
                        <TableCell className="text-muted-foreground">{dept.manager_id || "Unassigned"}</TableCell>
                        <TableCell className="text-muted-foreground">{dept.code || "—"}</TableCell>
                        <TableCell className="text-right">
                          <DropdownMenu 
                            items={[
                              { label: "Edit Department", onClick: () => {} },
                              { label: "Assign Manager", onClick: () => {} },
                              { label: "Delete", onClick: () => {} }
                            ]}
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )
            )}

            {activeTab === "DESIGNATIONS" && (
              designations.length === 0 ? (
                <div className="p-12">
                  <EmptyState 
                    title="No designations found" 
                    description="Create standard job titles and roles for your organization." 
                    icon={<Briefcase className="w-8 h-8 text-muted-foreground" />} 
                  />
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Designation Title</TableHead>
                      <TableHead>Department Focus</TableHead>
                      <TableHead>Level</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {designations.map((desig: any) => (
                      <TableRow key={desig.id} className="group hover:bg-surface-hover">
                        <TableCell className="font-medium text-foreground">{desig.name || desig.title}</TableCell>
                        <TableCell className="text-muted-foreground">{desig.department || "General"}</TableCell>
                        <TableCell className="text-muted-foreground">{desig.level || "—"}</TableCell>
                        <TableCell className="text-right">
                          <DropdownMenu 
                            items={[
                              { label: "Edit Designation", onClick: () => {} },
                              { label: "Delete", onClick: () => {} }
                            ]}
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )
            )}
          </div>
        </div>
      </div>
    </RequireRole>
  );
}
