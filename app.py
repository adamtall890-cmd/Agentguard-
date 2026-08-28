from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent.runner import run_task
from engine.outcome import verify_outcome
from agent.autonomous_worker import AutonomousWorker  # Branchement de votre nouvel agent asynchrone

app = FastAPI(
    title="AgentGuard",
    version="1.0"
)

# Sert les fichiers HTML/CSS/JS
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
async def outcome(data: OutcomeRequest):
    """
    Cette route intercepte le clic sur le bouton 'Run Workflow' de l'interface.
    Elle fait travailler le nouvel agent de manière autonome, puis execute la vérification AgentGuard.
    """
    # 1. Initialisation de l'agent autonome réel
    worker = AutonomousWorker()
    
    # 2. L'agent execute sa boucle de réflexion et de traitement CRM de manière asynchrone
    # On lui passe l'identifiant pour la tâche
    prompt = f"Traiter l'action CRM pour le lead ID {data.refund_id}"
    agent_claim = await worker.run_workflow(prompt)

    # 3. Récupération de la structure de tâche classique pour assurer la compatibilité
    task = {
        "action": "CREATE_LEAD",
        "lead_id": data.refund_id,
        "worker_claim": agent_claim
    }

    # 4. Execution des scripts de simulation et de verdict
    agent_result = run_task(task)
    verification = verify_outcome(data.refund_id)

    return {
        "task": task,
        "agent": agent_result,
        "verification": verification
    }
