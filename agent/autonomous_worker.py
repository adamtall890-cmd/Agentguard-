import os
import httpx
import asyncio
from typing import Dict, Any

class AutonomousWorker:
    def __init__(self, api_key: str = None):
        # Configuration du cerveau de l'agent (Clé API récupérée de l'environnement)
        self.api_key = api_key or os.getenv("LLM_API_KEY", "mock_key_for_now")
        # Base URL de votre propre serveur Render pour les appels internes
        self.server_url = "http://127.0.0.1:5000"

    async def analyze_task(self, prompt: str) -> Dict[str, Any]:
        """
        Analyse l'ordre textuel et décide de l'action CRM à mener.
        Dans une version finale, ce bloc appelle l'API de Gemini/OpenAI.
        """
        print(f"🤖 Agent reçu l'ordre : '{prompt}'")
        await asyncio.sleep(1) # Simulation du temps de réflexion de l'IA
        
        # Logique décisionnelle autonome basique pour le test de structure
        if "crm" in prompt.lower() or "client" in prompt.lower():
            return {
                "action": "UPDATE_CRM",
                "payload": {"client_name": "Adam", "location": "Abidjan", "status": "Active"}
            }
        return {"action": "UNKNOWN", "payload": {}}

    async def execute_crm_payload(self, payload: Dict[str, Any]) -> bool:
        """
        L'agent utilise son outil (Tool) pour modifier réellement le CRM via le connecteur.
        """
        async with httpx.AsyncClient() as client:
            try:
                # L'agent appelle le connecteur de votre application AgentGuard
                response = await client.post(f"{self.server_url}/connectors", json=payload)
                if response.status_code == 200:
                    print("✅ Agent : Données transmises avec succès au connecteur CRM.")
                    return True
                return False
            except Exception as e:
                print(f"❌ Erreur d'exécution de l'agent : {e}")
                return False

    async def run_workflow(self, prompt: str):
        """
        Boucle principale d'exécution de l'agent.
        """
        # 1. L'agent réfléchit et extrait les paramètres
        decision = await self.analyze_task(prompt)
        
        if decision["action"] == "UPDATE_CRM":
            # 2. L'agent exécute l'action de manière autonome
            success = await self.execute_crm_payload(decision["payload"])
            
            # 3. L'agent génère sa déclaration de réussite (Claim)
            # C'est cette déclaration qu'AgentGuard va intercepter et vérifier !
            claim = {
                "worker_id": "autonomous_worker_v1",
                "task_completed": success,
                "declared_outcome": "CRM updated successfully with Adam from Abidjan"
            }
            return claim
        return {"error": "Task layout not supported"}

# Bloc d'activation autonome pour les tests en direct
if __name__ == "__main__":
    worker = AutonomousWorker()
    # On simule un ordre de travail réel reçu par l'agent
    asyncio.run(worker.run_workflow("Ajouter le client Adam de Abidjan dans le CRM"))
