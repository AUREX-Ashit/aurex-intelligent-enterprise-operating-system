import type { InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  invalid?: boolean;
}

export function Input({ className, invalid = false, ...props }: InputProps) {
  return (
    <input
      {...props}
      aria-invalid={invalid || undefined}
      className={cn(
        "h-10 w-full rounded-md border bg-surface px-3 text-sm text-foreground outline-none transition placeholder:text-muted disabled:cursor-not-allowed disabled:opacity-60",
        invalid
          ? "border-danger focus:border-danger focus:ring-2 focus:ring-danger/20"
          : "border-border focus:border-brand focus:ring-2 focus:ring-brand/20",
        className,
      )}
    />
  );
}
