from langchain_chroma import Chroma
from knowledge.vector_store.retriever import DummyEmbeddings

print("Testing vector store directly...")
try:
    db = Chroma(persist_directory='knowledge/vector_store/db', embedding_function=DummyEmbeddings())
    docs = db.get()
    print("Number of documents:", len(docs['documents']))
    if docs['documents']:
        print("First document:", docs['documents'][0][:100])
        print("First metadata:", docs['metadatas'][0] if docs['metadatas'] else 'No metadata')
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
