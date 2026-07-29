import Link from "next/link";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";

const SECTIONS = [
  { href: "/health", label: "Health", description: "Backend connectivity check." },
  { href: "/person-management", label: "Person Management", description: "Coming soon." },
  { href: "/organization", label: "Organization", description: "Coming soon." },
  { href: "/workspace", label: "Workspace", description: "Coming soon." },
  { href: "/settings", label: "Settings", description: "Coming soon." },
] as const;

export default function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">
          Aurex Enterprise Operating System
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">Frontend foundation.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {SECTIONS.map((section) => (
          <Link key={section.href} href={section.href}>
            <Card className="h-full transition hover:border-brand">
              <CardTitle>{section.label}</CardTitle>
              <CardDescription>{section.description}</CardDescription>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
