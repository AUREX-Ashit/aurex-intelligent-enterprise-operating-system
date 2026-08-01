"use client";

import { useMembershipManagement } from "@/features/membership/state/useMembershipManagement";
import { EstablishMembershipSection } from "@/features/membership/components/EstablishMembershipSection";
import { MyPortfolioSection } from "@/features/membership/components/MyPortfolioSection";
import { UnderstandMembershipSection } from "@/features/membership/components/UnderstandMembershipSection";

export function MembershipManagementScreen() {
  const { establishState, understandState, portfolioState, establish, understand, changeTerms, loadPortfolio } =
    useMembershipManagement();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Membership Management</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Establish, understand, and maintain Membership Context (C-007).
        </p>
      </div>

      <MyPortfolioSection state={portfolioState} onLoad={loadPortfolio} />
      <UnderstandMembershipSection state={understandState} onUnderstand={understand} onChangeTerms={changeTerms} />
      <EstablishMembershipSection state={establishState} onEstablish={establish} />
    </div>
  );
}
