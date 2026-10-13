import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { DepartmentResponse, DesignationResponse, BranchResponse, ShiftResponse } from "@/types/hr";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Building2, Briefcase, MapPin, Clock } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent } from "@/components/ui/Card";

export function OrganizationStructureTab({ refreshTrigger = 0 }: { refreshTrigger?: number }) {
  const [activeSubTab, setActiveSubTab] = useState<"DEPARTMENTS" | "DESIGNATIONS" | "BRANCHES" | "SHIFTS">("DEPARTMENTS");
  
  const [departments, setDepartments] = useState<DepartmentResponse[]>([]);
  const [designations, setDesignations] = useState<DesignationResponse[]>([]);
  const [branches, setBranches] = useState<BranchResponse[]>([]);
  const [shifts, setShifts] = useState<ShiftResponse[]>([]);
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStructure = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const [deps, desigs, brans, shfs] = await Promise.all([
        hrRepository.getDepartments().catch(() => []),
        hrRepository.getDesignations().catch(() => []),
        hrRepository.getBranches().catch(() => []),
        hrRepository.getShifts().catch(() => []),
      ]);
      
      setDepartments(deps);
      setDesignations(desigs);
      setBranches(brans);
      setShifts(shfs);
      
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load organization structure.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStructure();
  }, [refreshTrigger]);

  if (isLoading) {
    return <LoadingState message="Loading structure..." className="py-12" />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchStructure} />;
  }

  const renderDepartments = () => (
    <Card>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {departments.length === 0 ? (
              <TableRow><TableCell colSpan={4} className="text-center text-muted-foreground py-12">No departments found.</TableCell></TableRow>
            ) : (
              departments.map((dep) => (
                <TableRow key={dep.id}>
                  <TableCell className="font-medium text-foreground">{dep.id}</TableCell>
                  <TableCell>{dep.name}</TableCell>
                  <TableCell>{dep.description || "-"}</TableCell>
                  <TableCell>
                    <Badge variant={dep.is_active ? "success" : "secondary"}>
                      {dep.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );

  const renderDesignations = () => (
    <Card>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Department ID</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {designations.length === 0 ? (
              <TableRow><TableCell colSpan={4} className="text-center text-muted-foreground py-12">No designations found.</TableCell></TableRow>
            ) : (
              designations.map((des) => (
                <TableRow key={des.id}>
                  <TableCell className="font-medium text-foreground">{des.id}</TableCell>
                  <TableCell>{des.name}</TableCell>
                  <TableCell>{des.department_id || "-"}</TableCell>
                  <TableCell>
                    <Badge variant={des.is_active ? "success" : "secondary"}>
                      {des.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );

  const renderBranches = () => (
    <Card>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Location</TableHead>
              <TableHead>Address</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {branches.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center text-muted-foreground py-12">No branches found.</TableCell></TableRow>
            ) : (
              branches.map((b) => (
                <TableRow key={b.id}>
                  <TableCell className="font-medium text-foreground">{b.id}</TableCell>
                  <TableCell>{b.name}</TableCell>
                  <TableCell>{b.location || "-"}</TableCell>
                  <TableCell>{b.address || "-"}</TableCell>
                  <TableCell>
                    <Badge variant={b.is_active ? "success" : "secondary"}>
                      {b.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );

  const renderShifts = () => (
    <Card>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Start Time</TableHead>
              <TableHead>End Time</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {shifts.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center text-muted-foreground py-12">No shifts found.</TableCell></TableRow>
            ) : (
              shifts.map((s) => (
                <TableRow key={s.id}>
                  <TableCell className="font-medium text-foreground">{s.id}</TableCell>
                  <TableCell>{s.name}</TableCell>
                  <TableCell>{s.start_time}</TableCell>
                  <TableCell>{s.end_time}</TableCell>
                  <TableCell>
                    <Badge variant={s.is_active ? "success" : "secondary"}>
                      {s.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6 mt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold tracking-tight text-foreground">Organization Structure</h2>
      </div>

      <div className="flex gap-2 border-b border-border/40 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveSubTab("DEPARTMENTS")}
          className={`flex items-center px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            activeSubTab === "DEPARTMENTS" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-surface-hover"
          }`}
        >
          <Building2 className="w-4 h-4 mr-2" />
          Departments ({departments.length})
        </button>
        <button
          onClick={() => setActiveSubTab("DESIGNATIONS")}
          className={`flex items-center px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            activeSubTab === "DESIGNATIONS" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-surface-hover"
          }`}
        >
          <Briefcase className="w-4 h-4 mr-2" />
          Designations ({designations.length})
        </button>
        <button
          onClick={() => setActiveSubTab("BRANCHES")}
          className={`flex items-center px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            activeSubTab === "BRANCHES" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-surface-hover"
          }`}
        >
          <MapPin className="w-4 h-4 mr-2" />
          Branches ({branches.length})
        </button>
        <button
          onClick={() => setActiveSubTab("SHIFTS")}
          className={`flex items-center px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            activeSubTab === "SHIFTS" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-surface-hover"
          }`}
        >
          <Clock className="w-4 h-4 mr-2" />
          Shifts ({shifts.length})
        </button>
      </div>

      <div className="mt-4">
        {activeSubTab === "DEPARTMENTS" && renderDepartments()}
        {activeSubTab === "DESIGNATIONS" && renderDesignations()}
        {activeSubTab === "BRANCHES" && renderBranches()}
        {activeSubTab === "SHIFTS" && renderShifts()}
      </div>
    </div>
  );
}
