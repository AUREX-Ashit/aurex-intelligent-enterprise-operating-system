# routers/extraction.py
from fastapi import APIRouter, Request, Depends, HTTPException, status
from services.ai_orchestrator import AIOrchestrator, get_ai_orchestrator
from schemas.extraction import ExtractionRequest, ExtractionResponse

router = APIRouter(prefix="/ai", tags=["Data Extraction"])

@router.post(
    "/extract", 
    response_model=ExtractionResponse, 
    status_code=status.HTTP_200_OK,
    summary="Extract ESG Metrics from corp files"
)
async def extract_esg_metrics(
    request: Request,
    payload: ExtractionRequest,
    orchestrator: AIOrchestrator = Depends(get_ai_orchestrator)
):
    """Integrates intelligent parsing OCR on designated ESG filings to extract metrics."""
    # Retrieve tenant ID from the middleware state
    tenant_id = getattr(request.state, "tenant_id", "default_tenant")
    
    try:
        extraction_model = await orchestrator.execute_extraction_flow(tenant_id, payload)
        return extraction_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Data Extraction Flow Error: {str(e)}"
        )
