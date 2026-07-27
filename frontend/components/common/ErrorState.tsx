import * as React from "react";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";

export interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({ 
  title = "Something went wrong", 
  message = "An error occurred while loading this content.", 
  onRetry, 
  className = "" 
}: ErrorStateProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center bg-red-50/50 rounded-lg border border-red-100 ${className}`}>
      <AlertCircle className="mb-4 h-10 w-10 text-destructive" />
      <h3 className="mb-2 text-lg font-semibold text-gray-900">{title}</h3>
      <p className="mb-6 max-w-sm text-sm text-gray-500">{message}</p>
      {onRetry && (
        <Button variant="outline" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
}
