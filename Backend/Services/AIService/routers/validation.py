# routers/validation.py
from fastapi import APIRouter, Request, Depends, HTTPException, status
from services.ai_orchestrator import AIOrchestrator, get_ai_orchestrator
from repositories.validation_repository import ESGValidationRepository
from schemas.validation import (
    ValidationRequest, 
    ValidationResponse, 
    HumanReviewRequest
)
from models.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/ai", tags=["Compliance Validation"])

@router.post(
    "/validate", 
    response_model=ValidationResponse, 
    status_code=status.HTTP_200_OK,
    summary="Validate extracted ESG Metrics"
)
async def validate_esg_metrics(
    request: Request,
    payload: ValidationRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Enforce governance validation protocols against stored disclosures."""
    tenant_id = getattr(request.state, "tenant_id", "default_tenant")
    
    try:
        validation_model = await orchestrator.execute_validation_flow(tenant_id, payload)
        return validation_model
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(val_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Governance Verification Error: {str(e)}"
        )

@router.post(
    "/review", 
    response_model=ValidationResponse, 
    status_code=status.HTTP_200_OK,
    summary="Auditor validation override and approval"
)
async def process_human_compliance_review(
    request: Request,
    payload: HumanReviewRequest,
    db: AsyncSession = Depends(get_db)
):
    """Updates validation records status dynamically under active tenancy contexts."""
    tenant_id = getattr(request.state, "tenant_id", "default_tenant")
    repo = ESGValidationRepository(db)

    validation_record = await repo.get_by_id(tenant_id, payload.validation_id)
    if not validation_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target validation log ID {payload.validation_id} not registered."
        )

    # Approve overrides existing validation fails
    update_data = {
        "is_reviewed": True,
        "reviewed_by": payload.reviewer_email,
        "governance_verified": payload.is_approved
    }
    
    # If approved, clear the anomalies logs list
    if payload.is_approved:
        update_data["anomalies_detected"] = []

    updated_record = await repo.update(tenant_id, payload.validation_id, update_data)
    return updated_record
