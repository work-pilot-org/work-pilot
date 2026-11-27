"use client";

import React, { useState, useRef, useEffect } from "react";
import { MoreVertical } from "lucide-react";
import { Button } from "./Button";

interface DropdownItem {
  label: string;
  onClick: (e: React.MouseEvent) => void;
  variant?: "default" | "danger";
}

interface DropdownMenuProps {
  items: DropdownItem[];
  trigger?: React.ReactNode;
}

export function DropdownMenu({ items, trigger }: DropdownMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      <div 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
      >
        {trigger || (
          <Button variant="outline" size="sm" className="h-8 w-8 p-0 border-border text-muted-foreground hover:bg-surface-hover hover:text-foreground transition-colors rounded-md">
            <MoreVertical className="h-4 w-4" />
          </Button>
        )}
      </div>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-2 w-48 origin-top-right rounded-md bg-surface border border-border-strong shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div className="py-1">
            {items.map((item, index) => (
              <button
                key={index}
                onClick={(e) => {
                  e.stopPropagation();
                  setIsOpen(false);
                  item.onClick(e);
                }}
                className={`block w-full px-4 py-2 text-left text-sm ${
                  item.variant === "danger"
                    ? "text-destructive hover:bg-destructive/10"
                    : "text-foreground hover:bg-surface-hover"
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
