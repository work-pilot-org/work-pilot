const fs = require('fs');
const path = require('path');

const writePage = (dir, content) => {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'page.tsx'), content);
};

// HR Module
writePage('d:/work-pilot-clone/frontend/app/dashboard/hr/organization', `
"use client";
import { useState } from "react";
import { RequireRole } from "@/components/RequireRole";
import { Users } from "lucide-react";
import { EmptyState } from "@/components/common/EmptyState";
export default function OrganizationPage() {
  const [activeTab, setActiveTab] = useState("DEPARTMENTS");
  return (
    <RequireRole allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Management</h1>
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button onClick={() => setActiveTab("DEPARTMENTS")} className={\`\${activeTab === "DEPARTMENTS" ? "border-indigo-500 text-indigo-600" : "border-transparent text-gray-500"} whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium\`}>Departments</button>
            <button onClick={() => setActiveTab("DESIGNATIONS")} className={\`\${activeTab === "DESIGNATIONS" ? "border-indigo-500 text-indigo-600" : "border-transparent text-gray-500"} whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium\`}>Designations</button>
          </nav>
        </div>
        <EmptyState title={\`No \${activeTab.toLowerCase()} found\`} description="Please create one to get started." icon={<Users className="w-6 h-6" />} />
      </div>
    </RequireRole>
  );
}
`);

// IT Module Assets
writePage('d:/work-pilot-clone/frontend/app/dashboard/it/assets', `
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
`);

// Workflows 
writePage('d:/work-pilot-clone/frontend/app/dashboard/workflows/[id]', `
"use client";
import { useParams } from "next/navigation";
export default function WorkflowDetails() {
  const params = useParams();
  return <div className="p-6">Workflow Details: {params.id}</div>;
}
`);

writePage('d:/work-pilot-clone/frontend/app/dashboard/workflows/[id]/execute', `
"use client";
import { useParams } from "next/navigation";
import { RequireRole } from "@/components/RequireRole";
export default function WorkflowExecute() {
  const params = useParams();
  return <div className="p-6">Execute Workflow: {params.id}</div>;
}
`);

// Dashboard 
writePage('d:/work-pilot-clone/frontend/app/dashboard', `
"use client";
import { useAuthStore } from "@/store/authStore";
import { useEffect, useState } from "react";
export default function DashboardPage() {
  const { user } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => { setTimeout(() => setIsLoading(false), 500) }, []);
  
  if (isLoading) return <div className="p-12 text-center text-gray-500 animate-pulse">Loading statistics...</div>;
  
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">Welcome back, {user?.first_name || user?.name || 'User'}!</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Pending Approvals</h3>
          <p className="text-3xl font-semibold mt-2">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Active Tickets</h3>
          <p className="text-3xl font-semibold mt-2">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Upcoming Leave</h3>
          <p className="text-3xl font-semibold mt-2">None</p>
        </div>
      </div>
      <div className="mt-8 bg-white p-6 rounded-lg shadow-sm border border-gray-100 min-h-[300px]">
        <h3 className="text-lg font-medium mb-4">Recent Activity Feed</h3>
        <p className="text-gray-500 text-sm italic">No recent activity to display.</p>
      </div>
    </div>
  );
}
`);

console.log("Pages generated successfully.");
