import os
from core.config import OPENAI_APIKEY
os.environ["OPENAI_API_KEY"] = OPENAI_APIKEY


from langchain import OpenAI
from langchain.chat_models import ChatOpenAI

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext, StorageContext, Document, load_index_from_storage
def createVectorIndex():
    max_input = 4096
    tokens = 256
    chunk_size = 600
    max_chunk_overlap = 20

    # Load data
    documents = SimpleDirectoryReader('./data').load_data()

    prompt_helper = PromptHelper(max_input_size=max_input, max_chunk_overlap=max_chunk_overlap, chunk_size_limit=chunk_size)
    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, max_tokens=tokens, model_name="text-davinci-003"))

    # configure service context
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    storage_context = StorageContext.from_defaults()

    # build index
    index = GPTVectorStoreIndex.from_documents(documents=documents, service_context=service_context, storage_context=storage_context)
    index.storage_context.persist()
    
    return index

loaded_index = createVectorIndex()

query_engine = loaded_index.as_query_engine()
prompt = input("Bot: HI, what do you want yo know?\nUser: ")
while True:
    resp = query_engine.query(prompt)
    print(resp)
    prompt = input("\nUser: ")


