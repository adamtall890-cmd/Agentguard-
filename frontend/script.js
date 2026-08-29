document.getElementById('btn-run').addEventListener('click', async () => {
    const refundId = document.getElementById('refund-id').value;
    const btn = document.getElementById('btn-run');
    
    // Éléments visuels des zones de logs
    const logAgent = document.getElementById('log-agent');
    const logGuard = document.getElementById('log-guard');
    const badgeAgent = document.getElementById('badge-agent');
    const badgeGuard = document.getElementById('badge-guard');

    // Passage de l'interface en mode "Calcul en cours"
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing worker loop...';
    
    logAgent.style.color = '#F59E0B';
    logAgent.innerHTML = '🤖 AutonomousWorker initialized... Spinning up LLM execution core.';
    logGuard.innerHTML = '🔍 Monitoring memory buffers for execution claims...';

    try {
        // Envoi de la requête réelle à votre serveur FastAPI hébergé sur Render
        const response = await fetch('/outcome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refund_id: refundId })
        });
        
        const data = await response.json();

        // 1. Extraction et affichage de la signature de votre nouvel agent asynchrone
        const claim = data.task.worker_claim;
        badgeAgent.className = "status-badge badge-verified";
        badgeAgent.innerText = "Submitted";
        logAgent.style.color = '#3B82F6';
        logAgent.innerHTML = `[DECLARED CLAIM]\nID: ${claim.worker_id}\nStatus: Task Completed = ${claim.task_completed}\nMessage: "${claim.declared_outcome}"`;

        // 2. Analyse et affichage du verdict de sécurité d'AgentGuard
        const isVerified = data.verification ? data.verification : false; 
        
        // Incrémentation automatique du compteur total sur le dashboard sombre
        document.getElementById('count-total').innerText = parseInt(document.getElementById('count-total').innerText) + 1;

        // Si le moteur valide la trace, on allume en vert. Sinon, alerte fraude en rouge.
        if (isVerified) {
            badgeGuard.className = "status-badge badge-verified";
            badgeGuard.innerText = "Verified";
            logGuard.style.color = '#10B981';
            logGuard.innerHTML = `[SUCCESS] Cryptographic trace matching with database state.\nNo injection or state spoofing detected.\nOutcome validated securely.`;
            document.getElementById('count-verified').innerText = parseInt(document.getElementById('count-verified').innerText) + 1;
        } else {
            badgeGuard.className = "status-badge badge-fake";
            badgeGuard.innerText = "Spoof Detected";
            logGuard.style.color = '#EF4444';
            logGuard.innerHTML = `[CRITICAL ANOMALY] Agent claimed success but no write logs were observed in the target infrastructure.\nRejecting transaction payload.`;
            document.getElementById('count-fake').innerText = parseInt(document.getElementById('count-fake').innerText) + 1;
        }

    } catch (error) {
        logAgent.innerHTML = '❌ Network connection failure with AgentGuard Node.';
        logGuard.innerHTML = error.message;
    } finally {
        // Restauration du bouton à son état d'origine
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Run Verification Workflow';
    }
});
