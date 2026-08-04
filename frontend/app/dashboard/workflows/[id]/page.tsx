
"use client";
import { useParams } from "next/navigation";
export default function WorkflowDetails() {
  const params = useParams();
  return <div className="p-6">Workflow Details: {params.id}</div>;
}
