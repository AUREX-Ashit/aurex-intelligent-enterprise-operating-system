import { Spinner } from "@/components/ui/Spinner";

export default function PlatformAdminLoading() {
  return (
    <div className="flex flex-1 items-center justify-center py-16 text-muted-foreground">
      <Spinner className="mr-2 h-5 w-5" />
      <span className="text-sm font-medium">Loading…</span>
    </div>
  );
}
