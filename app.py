from fastapi import FastAPI

app = FastAPI(title="AgentGuard")

@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.1"
    }