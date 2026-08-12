"use client";

import React, { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { Button } from "./Button";

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
}

export function Drawer({ isOpen, onClose, title, description, children }: DrawerProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
          />
          
          {/* Drawer Panel */}
          <motion.div
            initial={{ x: "100%", boxShadow: "none" }}
            animate={{ 
              x: 0, 
              boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)" 
            }}
            exit={{ x: "100%", boxShadow: "none" }}
            transition={{ type: "spring", bounce: 0, duration: 0.4 }}
            className="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col bg-surface border-l border-border shadow-xl"
          >
            {/* Header */}
            <div className="flex items-start justify-between border-b border-border px-6 py-5">
              <div>
                {title && <h2 className="text-lg font-semibold text-foreground">{title}</h2>}
                {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
              </div>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={onClose} 
                className="h-8 w-8 rounded-full p-0 border-transparent hover:bg-surface-hover"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            
            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
