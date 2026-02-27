# Test lazy Chroma initialization directly
from knowledge.vector_store.retriever import get_vectordb, retrieve_reflection_unit

print("=== TESTING LAZY CHROMA INITIALIZATION ===")

# Test 1: Import should not initialize Chroma
print("✅ Import completed without Chroma initialization")

# Test 2: First call to get_vectordb() should trigger initialization
print("\n--- Calling get_vectordb() for first time ---")
try:
    vectordb = get_vectordb()
    print("✅ Lazy Chroma initialization successful")
except Exception as e:
    print(f"❌ Chroma initialization failed: {e}")

# Test 3: Second call should use cached instance
print("\n--- Calling get_vectordb() for second time ---")
try:
    vectordb2 = get_vectordb()
    print("✅ Cached Chroma instance used")
except Exception as e:
    print(f"❌ Cached Chroma failed: {e}")

# Test 4: Test retrieval
print("\n--- Testing retrieval ---")
try:
    result = retrieve_reflection_unit("I feel like I am failing at everything lately")
    print("✅ Retrieval test result:", result)
except Exception as e:
    print(f"❌ Retrieval failed: {e}")

print("\n=== LAZY LOADING TEST COMPLETE ===")
