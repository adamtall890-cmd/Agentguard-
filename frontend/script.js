document.getElementById('btn-run').addEventListener('click', async () => {
    const refundId = document.getElementById('refund-id').value;
    const btn = document.getElementById('btn-run');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';

    try {
        const response = await fetch('/outcome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refund_id: refundId })
        });
        const data = await response.json();

        // 1. Injection de vos objets JSON d'origine tels quels
        document.getElementById('json-agent').textContent = JSON.stringify(data.agent, null, 2);
        document.getElementById('json-guard').textContent = JSON.stringify(data.verification, null, 2);

        // 2. Extraction de la règle de validation d'origine
        const isVerified = data.verification && (data.verification.verified === true || data.verification === true);
        
        // Mise à jour de vos compteurs
        document.getElementById('total-checks').innerText = parseInt(document.getElementById('total-checks').innerText) + 1;

        const verdictWrapper = document.getElementById('verdict-wrapper');
        let statusText = "";

        if (isVerified) {
            verdictWrapper.innerHTML = `<div class="alert-box alert-verified">🔒 Verified Completion Detected</div>`;
            document.getElementById('verified-count').innerText = parseInt(document.getElementById('verified-count').innerText) + 1;
            statusText = "Verified";
        } else {
            verdictWrapper.innerHTML = `<div class="alert-box alert-fake">🚨 FAKE COMPLETION DETECTED</div>`;
            document.getElementById('fake-count').innerText = parseInt(document.getElementById('fake-count').innerText) + 1;
            statusText = "Fake Completion";
        }

        // 3. Injection de la ligne dans votre tableau historique
        const now = new Date().toTimeString().split(' ')[0];
        const historyRows = document.getElementById('history-rows');
        const newRow = `<tr>
            <td>${now}</td>
            <td>${refundId}</td>
            <td style="color: ${isVerified ? 'var(--color-verified)' : 'var(--color-fake)'}">${statusText}</td>
        </tr>`;
        historyRows.innerHTML = newRow + historyRows.innerHTML;

    } catch (error) {
        document.getElementById('json-agent').textContent = JSON.stringify({ error: "Node connection failure" }, null, 2);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Run Workflow';
    }
});
