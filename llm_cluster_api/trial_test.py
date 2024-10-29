from llm_cluster_api.src.message_decoder.message_decoder import MessageDecoder
from src.db.arango_model_storage import ArangoModelStorage

#model = ArangoModelStorage(url='http://localhost:8529',username='root', password='123')
#mistral = model.get_model('mistral')

im = MessageDecoder('register a workout for chest with 10 repetitions of the exercise bench press', model='mistral')
print(im.extract_data())