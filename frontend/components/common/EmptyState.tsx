import * as React from "react";
import { FileQuestion } from "lucide-react";

export interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}

export function EmptyState({ 
  title = "No results found", 
  description = "We couldn't find what you're looking for.", 
  icon, 
  action, 
  className = "" 
}: EmptyStateProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-12 text-center rounded-lg border border-dashed border-border/60 bg-surface-hover/30 ${className}`}>
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-surface-hover text-muted-foreground/60">
        {icon || <FileQuestion className="h-6 w-6" />}
      </div>
      <h3 className="mb-2 text-lg font-semibold text-foreground">{title}</h3>
      <p className="mb-6 max-w-sm text-sm text-muted-foreground">{description}</p>
      {action && <div>{action}</div>}
    </div>
  );
}
