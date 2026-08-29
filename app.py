from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio

from agent.runner import run_task
from engine.outcome import verify_outcome
from agent.autonomous_worker import AutonomousWorker

app = FastAPI(
    title="AgentGuard",
    version="1.0"
)

# Sert les fichiers HTML/CSS/JS d'origine
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def dashboard():
    return FileResponse("frontend/index.html")


@app.get("/api")
def api():
    return {
        "message": "AgentGuard API",
        "version": "1.0"
    }


class OutcomeRequest(BaseModel):
    refund_id: str


@app.post("/outcome")
def outcome(data: OutcomeRequest):
    # --- AJOUT SÉCURISÉ : On fait tourner l'agent autonome dans son coin ---
    try:
        worker = AutonomousWorker()
        prompt = f"Traiter l'action CRM pour le lead ID {data.refund_id}"
        
        # On crée une boucle isolée pour l'agent pour ne pas perturber le serveur
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agent_claim = loop.run_until_complete(worker.run_workflow(prompt))
        loop.close()
    except Exception:
        agent_claim = {"error": "Autonomous worker isolated execution issue"}

    # --- CODE D'ORIGINE INTACT : Vos 3 composants fonctionnent comme avant ---
    task = {
        "action": "CREATE_LEAD",
        "lead_id": data.refund_id,
        "worker_claim": agent_claim  # On injecte la donnée en bonus sans casser la structure
    }

    agent_result = run_task(task)

    verification = verify_outcome(data.refund_id)

    return {
        "task": task,
        "agent": agent_result,
        "verification": verification
    }
