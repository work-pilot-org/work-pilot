import * as React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", error, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={`flex h-10 w-full rounded-lg border bg-surface/50 px-3 py-2 text-sm shadow-[var(--shadow-subtle)] transition-all file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground/70 focus-visible:outline-none focus-visible:ring-1 focus-visible:bg-surface disabled:cursor-not-allowed disabled:opacity-50 ${
          error ? "border-destructive focus-visible:ring-destructive" : "border-border/60 focus-visible:ring-primary focus-visible:border-primary"
        } ${className}`}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export { Input };
