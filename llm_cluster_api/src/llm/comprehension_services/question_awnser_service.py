from src.LLM_provider_storage import LLMProviderStorage
from src.llm.LLModelQA import LLModelQA
from uuid import UUID

from src.db.arango_qa_model_storage import ArangoQAModelStorage

class QuestionAwnserService:

    @classmethod
    def make_call(cls, prompt_uid : UUID, inputs : dict, model_name : str) -> str:

        db = ArangoQAModelStorage()
        model = db.get_model(model_name)        
        prompt = model.get_prompt(prompt_uid)

        return LLMProviderStorage.get_provider_with_model(model_name).make_question_awnser_call(prompt.apply_input(inputs), model_name)