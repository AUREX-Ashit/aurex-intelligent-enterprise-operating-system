import type { ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
}

const variants: Record<NonNullable<ButtonProps["variant"]>, string> = {
  primary: "bg-brand text-brand-foreground border-brand hover:bg-brand-strong hover:border-brand-strong",
  secondary: "bg-surface text-foreground border-border hover:bg-surface-muted",
  ghost: "bg-transparent text-muted-foreground border-transparent hover:bg-surface-muted",
  danger: "bg-danger text-white border-danger hover:opacity-90",
};

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={cn(
        "inline-flex h-10 items-center justify-center rounded-md border px-4 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50",
        variants[variant],
        className,
      )}
    />
  );
}
