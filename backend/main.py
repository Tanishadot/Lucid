from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="LUCID Backend")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "LUCID backend running"}