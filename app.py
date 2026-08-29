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

# Configuration standard du dossier frontend pour distribuer les fichiers
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
    """
    Route principale corrigée pour exécuter la boucle asynchrone de l'agent 
    sans bloquer les fonctions synchrones d'origine.
    """
    # 1. Initialisation de votre agent autonome
    worker = AutonomousWorker()
    prompt = f"Traiter l'action CRM pour le lead ID {data.refund_id}"
    
    # 2. On force l'exécution de la fonction asynchrone de l'agent de manière isolée
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    agent_claim = loop.run_until_complete(worker.run_workflow(prompt))
    loop.close()

    # 3. Structure de tâche classique conservée pour vos modules d'origine
    task = {
        "action": "CREATE_LEAD",
        "lead_id": data.refund_id,
        "worker_claim": agent_claim
    }

    # 4. Exécution de vos fonctions d'origine (Zéro modification, sécurité maximale)
    agent_result = run_task(task)
    verification = verify_outcome(data.refund_id)

    return {
        "task": task,
        "agent": agent_result,
        "verification": verification
    }
