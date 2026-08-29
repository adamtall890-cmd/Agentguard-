document.getElementById('btn-run').addEventListener('click', async () => {
    const refundId = document.getElementById('refund-id').value;
    const btn = document.getElementById('btn-run');
    const logAgent = document.getElementById('log-agent');
    const logGuard = document.getElementById('log-guard');
    const badgeAgent = document.getElementById('badge-agent');
    const badgeGuard = document.getElementById('badge-guard');

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Testing Pipeline...';

    try {
        const response = await fetch('/outcome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refund_id: refundId })
        });
        const data = await response.json();

        // 1. Affiche l'exécution réelle issue de vos dossiers backend
        badgeAgent.className = "status-badge badge-verified";
        badgeAgent.innerText = "Executed";
        logAgent.style.color = '#3B82F6';
        logAgent.innerHTML = `[AGENT EXECUTION LOGS]\nAction: ${data.task.action}\nResult Output: ${JSON.stringify(data.agent)}`;

        // 2. Traitement de la vérification de votre outil engine/outcome.py
        const verificationResult = data.verification;
        
        // Gestion de vos structures d'alerte d'origine (booléen ou objet)
        let isVerified = false;
        if (verificationResult === true || verificationResult === "true") {
            isVerified = true;
        } else if (verificationResult && typeof verificationResult === 'object' && verificationResult.verified === true) {
            isVerified = true;
        }

        // Incrémentation du compteur global
        document.getElementById('count-total').innerText = parseInt(document.getElementById('count-total').innerText) + 1;

        if (isVerified) {
            badgeGuard.className = "status-badge badge-verified";
            badgeGuard.innerText = "Verified";
            logGuard.style.color = '#10B981';
            logGuard.innerHTML = `[VERDICT: SECURE]\nOutcome matching verification metrics.\nNo manipulation detected in target ledger.`;
            document.getElementById('count-verified').innerText = parseInt(document.getElementById('count-verified').innerText) + 1;
        } else {
            badgeGuard.className = "status-badge badge-fake";
            badgeGuard.innerText = "Spoof Detected";
            logGuard.style.color = '#EF4444';
            logGuard.innerHTML = `[CRITICAL ALERT: FRAUD DETECTED]\nState validation failed.\nAgent state logs mismatch with system event logs.`;
            document.getElementById('count-fake').innerText = parseInt(document.getElementById('count-fake').innerText) + 1;
        }

    } catch (error) {
        logAgent.innerHTML = '❌ Connection node error.';
        logGuard.innerHTML = error.message;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Run Verification Workflow';
    }
});
