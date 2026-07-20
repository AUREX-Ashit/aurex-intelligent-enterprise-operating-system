# services/scoring_engine.py
from typing import Tuple, List, Dict
from schemas.extraction import ESGMetrics
from schemas.scoring import SDGMappingDetail

class ESGScoringEngine:
    """Calculates granular ESG metrics performance scores and executes UN SDG mappings."""

    async def calculate_esg_scores(self, metrics: ESGMetrics, custom_weights: Dict[str, float] = None) -> Tuple[float, float, float, float, List[SDGMappingDetail]]:
        # Default weight ratios across E, S, G
        weights = {"e": 0.40, "s": 0.30, "g": 0.30}
        if custom_weights:
            weights.update(custom_weights)

        # 1. Environmental Scoring Base (Max 100)
        e_points = 50.0  # Base line
        if metrics.scope_1_emissions_mt is not None and metrics.scope_1_emissions_mt < 5000:
            e_points += 20.0  # Carbon efficiency reward
        if metrics.renewable_energy_ratio is not None:
            e_points += (metrics.renewable_energy_ratio * 30.0) # Integration ratio performance points
        e_score = min(round(e_points, 1), 100.0)

        # 2. Social Scoring Base (Max 100)
        s_points = 60.0
        if metrics.female_executive_ratio is not None:
            s_points += (metrics.female_executive_ratio * 20.0)
        if metrics.employee_turnover_rate is not None and metrics.employee_turnover_rate < 0.10:
            s_points += 20.0  # Talent retention offset bonus
        s_score = min(round(s_points, 1), 100.0)

        # 3. Governance Scoring Base (Max 100)
        g_points = 50.0
        if metrics.independent_directors_ratio is not None:
            g_points += (metrics.independent_directors_ratio * 30.0)
        if metrics.anti_corruption_policy:
            g_points += 10.0
        if metrics.whistleblower_hotline_active:
            g_points += 10.0
        g_score = min(round(g_points, 1), 100.0)

        # Composite Aggregate calculation
        composite_esg_score = round(
            (e_score * weights["e"]) + (s_score * weights["s"]) + (g_score * weights["g"]), 
            1
        )

        # Map metrics to UN Sustainable Development Goals
        sdg_mappings: List[SDGMappingDetail] = []
        
        # SDG 13: Climate Action
        if metrics.scope_1_emissions_mt is not None:
            sdg_mappings.append(SDGMappingDetail(
                sdg_id=13,
                sdg_name="Climate Action",
                relevance_score=0.95,
                evidence_text=f"Direct reported scope emissions level of {metrics.scope_1_emissions_mt} MT registered on systems."
            ))

        # SDG 7: Affordable and Clean Energy
        if metrics.renewable_energy_ratio is not None and metrics.renewable_energy_ratio > 0.0:
            sdg_mappings.append(SDGMappingDetail(
                sdg_id=7,
                sdg_name="Affordable and Clean Energy",
                relevance_score=0.90,
                evidence_text=f"Renewable clean green power infrastructure accounts for {metrics.renewable_energy_ratio * 100:.0f}% of consumption."
            ))

        # SDG 5: Gender Equality
        if metrics.female_executive_ratio is not None:
            sdg_mappings.append(SDGMappingDetail(
                sdg_id=5,
                sdg_name="Gender Equality",
                relevance_score=0.88,
                evidence_text=f"Headcount index shows diversity and active integration with {metrics.female_executive_ratio * 100:.0f}% female executives."
            ))

        return e_score, s_score, g_score, composite_esg_score, sdg_mappings


def get_scoring_engine() -> ESGScoringEngine:
    return ESGScoringEngine()
