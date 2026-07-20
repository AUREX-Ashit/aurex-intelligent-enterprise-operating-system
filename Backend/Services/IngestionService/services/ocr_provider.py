from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import uuid
from config.settings import settings

class OCRProvider(ABC):
    """
    Abstract Base Class contract for Document Analysis & layout extraction engines.
    """
    
    @abstractmethod
    async def submittal_ocr_analysis(self, document_uri: str, tenant_id: str) -> str:
        """
        Dispatches document to OCR extraction endpoint. Returns a unique tracking ticket task ID.
        """
        pass

    @abstractmethod
    async def get_ocr_results(self, task_id: str, tenant_id: str) -> Dict[str, Any]:
        """
        Queries status/results of dispatched OCR analysis.
        """
        pass


class AzureDocumentIntelligenceStub(OCRProvider):
    """
    Production-grade dry-run implementation mocking Azure Document Intelligence Studio actions ("prebuilt-layout").
    """
    def __init__(self, model_name: str = "prebuilt-layout"):
        self.model_name = model_name

    async def submittal_ocr_analysis(self, document_uri: str, tenant_id: str) -> str:
        # Returns simulated Azure operation tracking headers
        # In actual deployment:
        # from azure.ai.formrecognizer.aio import DocumentAnalysisClient
        # from azure.core.credentials import AzureKeyCredential
        # client = DocumentAnalysisClient(settings.ocr.endpoint, AzureKeyCredential(...))
        # poller = await client.begin_analyze_document_from_url(self.model_name, document_uri)
        
        mock_operation_id = f"azure-docintel-session-{uuid.uuid4()}"
        return mock_operation_id

    async def get_ocr_results(self, task_id: str, tenant_id: str) -> Dict[str, Any]:
        # Emits structured, annotated results mimicking form recognizer response data
        return {
            "status": "succeeded",
            "model_id": self.model_name,
            "analyzer_version": "2024-02-29-preview",
            "pages": [
                {
                    "page_number": 1,
                    "angle": 0.0,
                    "width": 8.5,
                    "height": 11.0,
                    "span_count": 2,
                    "lines": [
                        {"text": "CorpStage ESG Sustainability Audit Report 2026", "confidence": 0.99},
                        {"text": "Total Greenhouse Gas (GHG) Scope 1 Direct Emissions: 14,250 metric tons CO2e", "confidence": 0.98},
                        {"text": "Target Net-Zero Goal Year: 2030", "confidence": 0.99}
                    ]
                }
            ],
            "tables": [
                {
                    "row_count": 3,
                    "column_count": 2,
                    "cells": [
                        {"row_index": 0, "column_index": 0, "content": "Metric Name"},
                        {"row_index": 0, "column_index": 1, "content": "Value"},
                        {"row_index": 1, "column_index": 0, "content": "Scope 1 Emissions"},
                        {"row_index": 1, "column_index": 1, "content": "14250 mt"},
                        {"row_index": 2, "column_index": 0, "content": "Scope 2 (Market-based)"},
                        {"row_index": 2, "column_index": 1, "content": "8120 mt"}
                    ]
                }
            ],
            "metadata": {
                "inferred_language": "en",
                "extracted_tenant": tenant_id
            }
        }
