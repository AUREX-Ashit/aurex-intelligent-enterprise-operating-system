# services/ai_orchestrator.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_db
from models.extraction import ESGExtractionModel
from models.validation import ESGValidationModel
from models.scoring import ESGScoringModel
from repositories.extraction_repository import ESGExtractionRepository
from repositories.validation_repository import ESGValidationRepository
from repositories.scoring_repository import ESGScoringRepository
from services.extraction_engine import ESGExtractionEngine, get_extraction_engine
from services.validation_engine import ESGValidationEngine, get_validation_engine
from services.scoring_engine import ESGScoringEngine, get_scoring_engine
from schemas.extraction import ExtractionRequest
from schemas.validation import ValidationRequest
from schemas.scoring import ScoringRequest

class AIOrchestrator:
    """The master cognitive brain of CorpStage. Orchestrates services and commits state data databases."""
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        extractor: ESGExtractionEngine = Depends(get_extraction_engine),
        validator: ESGValidationEngine = Depends(get_validation_engine),
        scorer: ESGScoringEngine = Depends(get_scoring_engine)
    ):
        self.db = db
        self.extractor = extractor
        self.validator = validator
        self.scorer = scorer
        
        # Instantiate repositories
        self.extract_repo = ESGExtractionRepository(db)
        self.valid_repo = ESGValidationRepository(db)
        self.score_repo = ESGScoringRepository(db)

    async def execute_extraction_flow(self, tenant_id: str, request: ExtractionRequest) -> ESGExtractionModel:
        """Executes full unstructured-to-structured OCR and parsing logic."""
        # Run AI intelligence engine
        extracted_metrics, confidence = await self.extractor.extract_esg_data(
            request.document_name, 
            request.file_uri or "", 
            tenant_id
        )

        # Persist structured extraction to isolated database partitioned by Tenant ID
        db_payload = {
            "document_name": request.document_name,
            "status": "completed",
            "extracted_metrics": extracted_metrics.model_dump(),
            "overall_confidence": confidence,
            "extracted_by": "ai_orchestrator"
        }
        
        extraction_model = await self.extract_repo.create(tenant_id, db_payload)
        return extraction_model

    async def execute_validation_flow(self, tenant_id: str, request: ValidationRequest) -> ESGValidationModel:
        """Runs governance checks and verification protocols on extraction models."""
        # Find extraction result
        ext_result = await self.extract_repo.get_by_id(tenant_id, request.extraction_id)
        if not ext_result:
            raise ValueError(f"No extraction record found matching specified ID: {request.extraction_id}")

        # Cast JSON metrics representation into standard Pydantic schema
        from schemas.extraction import ESGMetrics
        metrics_schema = ESGMetrics(**ext_result.extracted_metrics)

        # Trigger governance rule analyzer
        verified, rules_run_log, anomalies = await self.validator.validate_metrics(metrics_schema)

        # Store results
        db_payload = {
            "extraction_id": request.extraction_id,
            "governance_verified": verified,
            "rules_run": [r.model_dump() for r in rules_run_log],
            "anomalies_detected": [a.model_dump() for a in anomalies],
            "is_reviewed": False,
            "reviewed_by": None
        }
        
        validation_model = await self.valid_repo.create(tenant_id, db_payload)
        return validation_model

    async def execute_scoring_flow(self, tenant_id: str, request: ScoringRequest) -> ESGScoringModel:
        """Assembles dimension metrics and maps output target sets to global SDGs."""
        ext_result = await self.extract_repo.get_by_id(tenant_id, request.extraction_id)
        if not ext_result:
            raise ValueError(f"No extraction records found matching specified ID: {request.extraction_id}")

        from schemas.extraction import ESGMetrics
        metrics_schema = ESGMetrics(**ext_result.extracted_metrics)

        # Calculate scores
        e, s, g, aggregate, sdg_mapping = await self.scorer.calculate_esg_scores(
            metrics_schema, 
            custom_weights=request.weightings
        )

        # Persist scoring record
        db_payload = {
            "extraction_id": request.extraction_id,
            "environmental_score": e,
            "social_score": s,
            "governance_score": g,
            "composite_esg_score": aggregate,
            "sdg_mapping": [sdg.model_dump() for sdg in sdg_mapping]
        }
        
        scoring_model = await self.score_repo.create(tenant_id, db_payload)
        return scoring_model


def get_ai_orchestrator(
    db: AsyncSession = Depends(get_db),
    extractor: ESGExtractionEngine = Depends(get_extraction_engine),
    validator: ESGValidationEngine = Depends(get_validation_engine),
    scorer: ESGScoringEngine = Depends(get_scoring_engine)
) -> AIOrchestrator:
    return AIOrchestrator(db=db, extractor=extractor, validator=validator, scorer=scorer)
