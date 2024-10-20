from src.interpretation_functions.interpretation_functions import Interpretation_module
from src.llm.LLModel import LLModel
from src.db.arango_model_storage import ArangoModelStorage

model = ArangoModelStorage(url='http://localhost:8529',username='root', password='123')
mistral = model.get_model('mistral')

im = Interpretation_module('add student with name pedro and note 10', model=mistral)
print(im.extract_data())