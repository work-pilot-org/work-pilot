import * as React from "react";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
}

const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className = "", variant = "default", ...props }, ref) => {
    
    const baseStyles = "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2";
    
    const variants = {
      default: "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/90",
      secondary: "border-border/50 bg-surface text-foreground hover:bg-surface-hover",
      destructive: "border-destructive/20 bg-destructive/10 text-destructive hover:bg-destructive/20",
      outline: "border-border/60 text-foreground",
      success: "border-success/20 bg-success/10 text-success hover:bg-success/20",
      warning: "border-warning/20 bg-warning/10 text-warning hover:bg-warning/20",
    };

    const variantStyles = variants[variant] || variants.default;

    return (
      <div
        ref={ref}
        className={`${baseStyles} ${variantStyles} ${className}`}
        {...props}
      />
    );
  }
);
Badge.displayName = "Badge";

export { Badge };
