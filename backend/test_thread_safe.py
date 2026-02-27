# Test thread-safe lazy initialization
import threading
import time
from knowledge.vector_store.retriever import get_vectordb, retrieve_reflection_unit

def test_thread_safe_initialization():
    """Test that multiple threads don't create multiple instances"""
    print("=== TESTING THREAD-SAFE LAZY INITIALIZATION ===")
    
    results = []
    
    def worker(thread_id):
        try:
            start = time.time()
            vectordb = get_vectordb()
            end = time.time()
            results.append({
                'thread_id': thread_id,
                'vectordb_id': id(vectordb),
                'time': end - start
            })
            print(f"Thread {thread_id}: Got vectordb in {end - start:.2f}s")
        except Exception as e:
            print(f"Thread {thread_id}: Error {e}")
    
    # Create multiple threads to test thread safety
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
    
    # Start all threads simultaneously
    for t in threads:
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Check results
    print("\n=== THREAD SAFETY RESULTS ===")
    vectordb_ids = [r['vectordb_id'] for r in results]
    unique_ids = set(vectordb_ids)
    
    if len(unique_ids) == 1:
        print("✅ Thread-safe: All threads got the same instance")
        print(f"✅ Single Chroma instance created: {list(unique_ids)[0]}")
    else:
        print("❌ NOT thread-safe: Multiple instances created")
        print(f"❌ Unique instances: {unique_ids}")
    
    print(f"✅ Total threads: {len(results)}")
    times = [f"{r['time']:.2f}s" for r in results]
    print(f"✅ Initialization times: {times}")
    
    # Test retrieval
    print("\n=== TESTING RETRIEVAL ===")
    try:
        result = retrieve_reflection_unit("I feel like I am failing at everything lately")
        print(f"✅ Retrieval result: {result}")
    except Exception as e:
        print(f"❌ Retrieval failed: {e}")

if __name__ == "__main__":
    test_thread_safe_initialization()
