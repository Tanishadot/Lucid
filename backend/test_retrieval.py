from knowledge.vector_store.retriever import retrieve_reflection_unit

print("Testing retrieval unit...")
try:
    result = retrieve_reflection_unit('I feel tired after being with people')
    print("Result:", result)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
