
"use client";
import { useParams } from "next/navigation";
import { RequireRole } from "@/components/RequireRole";
export default function WorkflowExecute() {
  const params = useParams();
  return <div className="p-6">Execute Workflow: {params.id}</div>;
}
