# services/validation_engine.py
from typing import Tuple, List
from schemas.extraction import ESGMetrics
from schemas.validation import RuleRunLog, AnomalyReport

class ESGValidationEngine:
    """Enforces compliance rules, handles out-of-bound errors, and tracks anomaly indicators."""
    
    async def validate_metrics(self, metrics: ESGMetrics) -> Tuple[bool, List[RuleRunLog], List[AnomalyReport]]:
        rules: List[RuleRunLog] = []
        anomalies: List[AnomalyReport] = []

        # Rule 1: Emissions completeness check
        if metrics.scope_1_emissions_mt is not None and metrics.scope_1_emissions_mt > 0:
            rules.append(RuleRunLog(
                rule_id="E-101",
                rule_name="Scope 1 Emissions Disclosed",
                passed=True,
                message="Scope 1 direct greenhouse emissions verified successfully."
            ))
        else:
            rules.append(RuleRunLog(
                rule_id="E-101",
                rule_name="Scope 1 Emissions Disclosed",
                passed=False,
                message="Critical environmental disclosure is absent or invalid."
            ))
            anomalies.append(AnomalyReport(
                field="scope_1_emissions_mt",
                disclosed_value=metrics.scope_1_emissions_mt,
                expected_range="> 0.0",
                confidence_decay=0.40,
                description="Regulatory reporting requirements require non-null direct Scope 1 values."
            ))

        # Rule 2: Female Executive Ratio sanity Check
        if metrics.female_executive_ratio is not None:
            if 0.0 <= metrics.female_executive_ratio <= 1.0:
                rules.append(RuleRunLog(
                    rule_id="S-201",
                    rule_name="Female Leadership Percentage Check",
                    passed=True,
                    message="Headcount percentage complies with standard formatting limits."
                ))
            else:
                rules.append(RuleRunLog(
                    rule_id="S-201",
                    rule_name="Female Leadership Percentage Check",
                    passed=False,
                    message="Leadership ratio exhibits out-of-bounds scale markers."
                ))
                anomalies.append(AnomalyReport(
                    field="female_executive_ratio",
                    disclosed_value=metrics.female_executive_ratio,
                    expected_range="0.0 to 1.0",
                    confidence_decay=0.80,
                    description="Leadership ratio cannot be less than zero or span beyond full capacity bounds."
                ))

        # Rule 3: Board Independence Ratio Standard
        if metrics.independent_directors_ratio is not None:
            # Corporate best practice standard: independent board needs to represent above 50%
            if metrics.independent_directors_ratio >= 0.50:
                rules.append(RuleRunLog(
                    rule_id="G-301",
                    rule_name="Board Independence Standards check",
                    passed=True,
                    message="Independent directors represent more than half the board, indicating good governance."
                ))
            else:
                rules.append(RuleRunLog(
                    rule_id="G-301",
                    rule_name="Board Independence Standards check",
                    passed=False,
                    message="Independent director ratios lie below recommended ESG targets of 50.00%."
                ))
                anomalies.append(AnomalyReport(
                    field="independent_directors_ratio",
                    disclosed_value=metrics.independent_directors_ratio,
                    expected_range=">= 0.50",
                    confidence_decay=0.15,
                    description="Board composition indicates low independence which may trigger governance compliance audits."
                ))

        # Rule 4: Anti Corruption Verification
        if metrics.anti_corruption_policy:
            rules.append(RuleRunLog(
                rule_id="G-302",
                rule_name="Anti Corruption Framework Disclosed",
                passed=True,
                message="Disclosed active frameworks against corporate bribery."
            ))
        else:
            rules.append(RuleRunLog(
                rule_id="G-302",
                rule_name="Anti Corruption Framework Disclosed",
                passed=False,
                message="No disclosure or policy details found."
            ))

        # Composite verification output
        governance_verified = all(r.passed for r in rules)

        return governance_verified, rules, anomalies


def get_validation_engine() -> ESGValidationEngine:
    return ESGValidationEngine()
