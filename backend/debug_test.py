from core.reflection_engine.retrieval_engine import run_reflection

print("Testing retrieval engine...")
try:
    result = run_reflection('test')
    print("Result:", result)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
