from fastapi import APIRouter, HTTPException
from src.comprehension_services.sentiment_analysis_service import SentimentAnalysisService
from src.comprehension_services.token_classification_service import TokenClassificationService
from src.comprehension_services.text_similarity_service import TextSimilarityService
from src.comprehension_services.comprehension_functions import ComprehensionFunctions
from src.decorators.business_rule_exception_check import business_rule_exception_check
from src.LLM_provider_storage import LLMProviderStorage
from pydantic import BaseModel
from typing import Optional

query_router = APIRouter()

class QueryComprehension(BaseModel):
    func : ComprehensionFunctions
    inputs : list[str]
    model : Optional[str]

@query_router.get('/models')
@business_rule_exception_check
def get_models():
     return LLMProviderStorage.get_default_provider().list_models()

@query_router.post('/query/comprehension', tags=["Query"])
@business_rule_exception_check
def query_cf(inputs : QueryComprehension):

        model_name = inputs.model

        if 2 < len(inputs.inputs) or 0 >= len(inputs.inputs):
             raise HTTPException(status_code=400, detail=f"Wrong number of string inputs for {str(inputs.func)}, that is {2 if inputs.func == ComprehensionFunctions.TEXT_SIMILARITY else 1}")

        match inputs.func:
            case ComprehensionFunctions.TOKEN_CLASSIFICATION:
                return { "data": TokenClassificationService.make_call(model=model_name,text=inputs.inputs[0] ) }
            case ComprehensionFunctions.TEXT_SIMILARITY:
                # return { "data": TokenClassificationService.make_call(model=model_name,text=inputs.inputs[0] ) }

                return { "data": TextSimilarityService.make_call(model=model_name,text_1=inputs.inputs[0], text_2=inputs.inputs[1] ) }
            case ComprehensionFunctions.SENTIMENT_ANALYSIS:
                return { "data": SentimentAnalysisService.make_call(model=model_name,text=inputs.inputs[0] ) }
                      
        return "This should be a unreachable point"


