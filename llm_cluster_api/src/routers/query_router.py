from src.LLM_provider_storage import LLMProviderStorage
from fastapi import APIRouter, HTTPException
from src.db.arango_qa_model_storage import ArangoQAModelStorage
from src.llm.comprehension_services.question_awnser_service import QuestionAwnserService
from src.llm.comprehension_services.sentiment_analysis_service import SentimentAnalysisService
from src.llm.comprehension_services.token_classification_service import TokenClassificationService
from src.llm.comprehension_services.text_similarity_service import TextSimilarityService

from src.llm.comprehension_services.comprehension_functions import ComprehensionFunctions

from src.models.model import Model
from src.models.query import QueryComprehension, QueryQA

from src.decorators.business_rule_exception_check import business_rule_exception_check

query_router = APIRouter()

@query_router.post('/query', tags=["Query"])
@business_rule_exception_check
def query_qa(inputs : QueryQA):        
        model_name = inputs.model_name

        return {
            "data":
                QuestionAwnserService.make_call(
                    model_name=model_name,
                    prompt_uid=inputs.prompt_uid,
                    inputs={
                        "variables": inputs.variables or []
                    }
                )
        }


@query_router.post('/query/comprehension', tags=["Query"])
@business_rule_exception_check
def query_cf(inputs : QueryComprehension):

        model_name = inputs.model_name

        if inputs.func == ComprehensionFunctions.QUESTION_AWNSER:
            raise HTTPException(status_code=400, detail="Refer to /query/{model_name} if you want to make QA calls.")

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
                      
        return "It should be a unreachable point"


