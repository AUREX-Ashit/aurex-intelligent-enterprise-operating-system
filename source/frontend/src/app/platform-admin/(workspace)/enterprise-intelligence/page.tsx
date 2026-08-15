import { DiscoveryProviderScreen } from "@/features/discovery-provider/components/DiscoveryProviderScreen";
import { KnowledgeAssetScreen } from "@/features/knowledge-asset/components/KnowledgeAssetScreen";
import { EnterpriseSearchScreen } from "@/features/search/components/EnterpriseSearchScreen";

/**
 * WP-14 BA-04 (Establish Knowledge Asset, C-091) and WP-14 BA-01 (Establish
 * Discovery Provider Configuration, C-090) are both added to this existing
 * `enterprise-intelligence` route rather than a new nav entry — IRA-014
 * §9's own Plan B named this exact extension ("extension of the existing
 * enterprise-intelligence administration surface into a multi-tab/
 * multi-section screen") as one of its two candidate placements, and this
 * is the identical "reuse the existing slot, stack additional Business
 * Activity sections" precedent WP-11's own EnterpriseSearchScreen already
 * established for its own three BAs (see that component's own docstring).
 * WP-11's EnterpriseSearchScreen and WP-14 BA-04's own KnowledgeAssetScreen
 * are both unmodified — this page composes DiscoveryProviderScreen
 * alongside them; no other capability's already-certified screen is
 * touched.
 */
export default function EnterpriseIntelligencePage() {
  return (
    <div className="space-y-10">
      <EnterpriseSearchScreen />
      <hr className="border-border-muted" />
      <KnowledgeAssetScreen />
      <hr className="border-border-muted" />
      <DiscoveryProviderScreen />
    </div>
  );
}
