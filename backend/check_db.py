from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

db = Chroma(persist_directory='knowledge/vector_store/db', embedding_function=OpenAIEmbeddings())
docs = db.get()
print(f'Documents: {len(docs["documents"])}')
print(f'IDs: {len(docs["ids"])}')
print(f'Metadata keys: {list(docs["metadata"][0].keys()) if docs["metadata"] else "None"}')
