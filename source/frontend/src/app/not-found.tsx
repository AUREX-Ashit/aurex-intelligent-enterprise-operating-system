import Link from "next/link";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";

export default function NotFound() {
  return (
    <div className="flex flex-1 items-center justify-center py-16">
      <Card className="max-w-md text-center">
        <CardTitle>Page not found</CardTitle>
        <CardDescription>The page you&apos;re looking for doesn&apos;t exist.</CardDescription>
        <Link
          href="/"
          className="mt-6 inline-flex h-10 items-center justify-center rounded-md border border-brand bg-brand px-4 text-sm font-semibold text-brand-foreground transition hover:border-brand-strong hover:bg-brand-strong"
        >
          Return home
        </Link>
      </Card>
    </div>
  );
}
