"use client";

import { useRef, type ReactNode } from "react";
import { useOverlay } from "@/hooks/useOverlay";
import { cn } from "@/lib/utils";

export interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  className?: string;
}

export function Modal({ open, onClose, title, children, className }: ModalProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  useOverlay({ open, onClose, containerRef });

  if (!open) return null;

  return (
    <div
      role="presentation"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
      onClick={onClose}
    >
      <div
        ref={containerRef}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        tabIndex={-1}
        onClick={(event) => event.stopPropagation()}
        className={cn(
          "w-full max-w-lg rounded-lg border border-border bg-surface p-6 shadow-lg outline-none",
          className,
        )}
      >
        {title && <h2 className="mb-4 text-lg font-bold text-foreground">{title}</h2>}
        {children}
      </div>
    </div>
  );
}
