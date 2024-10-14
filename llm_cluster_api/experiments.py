# from src.LLM_provider_storage import LLMProviderStorage


# print(LLMProviderStorage.list_all_models())

from src.llm.comprehension_services.token_classification_service import TokenClassificationService
from src.llm.comprehension_services.sentiment_analysis_service import SentimentAnalysisService
from src.llm.comprehension_services.text_similarity_service import TextSimilarityService
from uuid import UUID

# print(TokenClassificationService.make_call(model="vblagoje/bert-english-uncased-finetuned-pos", text="rediz"))
# a = SentimentAnalysisService.make_call(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", text="rediz")
# print(type(a[0]["score"]))

print(TextSimilarityService.make_call(model="sentence-transformers/all-MiniLM-L6-v2", text_1="shit", text_2="dog"))
print(TokenClassificationService.make_call(model="vblagoje/bert-english-uncased-finetuned-pos", text="beatle"))
print(SentimentAnalysisService.make_call(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", text="zoom"))