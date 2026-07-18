import Link from "next/link";
import { Fragment } from "react";
import { cn } from "@/lib/utils";

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

/**
 * DS-001 Navigation Components — Breadcrumb. Satisfies SD-001-034
 * (Universal Header Structure: every screen shows title, context, and
 * breadcrumb in a fixed position) for screens nested under the admin
 * shell. Takes explicit items rather than deriving labels from the URL,
 * since route slugs (e.g. "audit-compliance") are not fit for display.
 */
export function Breadcrumb({ items, className }: { items: BreadcrumbItem[]; className?: string }) {
  return (
    <nav aria-label="Breadcrumb" className={cn("text-sm", className)}>
      <ol className="flex flex-wrap items-center gap-1.5 text-muted-foreground">
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          return (
            <Fragment key={`${item.label}-${index}`}>
              {index > 0 && <span aria-hidden="true">/</span>}
              <li>
                {item.href && !isLast ? (
                  <Link href={item.href} className="transition hover:text-foreground">
                    {item.label}
                  </Link>
                ) : (
                  <span
                    aria-current={isLast ? "page" : undefined}
                    className={cn(isLast && "font-semibold text-foreground")}
                  >
                    {item.label}
                  </span>
                )}
              </li>
            </Fragment>
          );
        })}
      </ol>
    </nav>
  );
}
