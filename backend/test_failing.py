from knowledge.vector_store.retriever import retrieve_reflection_unit

print("Testing retrieval with failing pattern...")
try:
    result = retrieve_reflection_unit("I feel like I am failing at everything lately")
    print("Result:", result)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
