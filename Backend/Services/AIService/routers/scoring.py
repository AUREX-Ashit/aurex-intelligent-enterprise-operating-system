# routers/scoring.py
from fastapi import APIRouter, Request, Depends, HTTPException, status
from services.ai_orchestrator import AIOrchestrator, get_ai_orchestrator
from schemas.scoring import ScoringRequest, ScoringResponse

router = APIRouter(prefix="/ai", tags=["ESG Analytics"])

@router.post(
    "/scoring", 
    response_model=ScoringResponse, 
    status_code=status.HTTP_200_OK,
    summary="Execute multi-dimensional ESG scoring and SDG target mapping"
)
async def calculate_esg_scoring(
    request: Request,
    payload: ScoringRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Compiles individual E, S, G criteria ratings and maps values against UN SDG goals."""
    tenant_id = getattr(request.state, "tenant_id", "default_tenant")
    
    try:
        scoring_model = await orchestrator.execute_scoring_flow(tenant_id, payload)
        return scoring_model
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=str(val_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ESG Matrix Scoring Error: {str(e)}"
        )
