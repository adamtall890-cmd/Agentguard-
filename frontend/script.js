document.getElementById('btn-run').addEventListener('click', async () => {
    const refundId = document.getElementById('refund-id').value;
    
    try {
        const response = await fetch('/outcome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refund_id: refundId })
        });
        const data = await response.json();

        // Affichage de vos vrais JSON d'origine
        document.getElementById('json-agent').textContent = JSON.stringify(data.agent, null, 2);
        document.getElementById('json-guard').textContent = JSON.stringify(data.verification, null, 2);

        // Compteur global
        document.getElementById('total-checks').innerText = parseInt(document.getElementById('total-checks').innerText) + 1;

        // Extraction précise de votre règle d'alerte d'origine
        const verdictDiv = document.getElementById('verdict');
        
        if (data.verification.verified === true) {
            document.getElementById('verified-count').innerText = parseInt(document.getElementById('verified-count').innerText) + 1;
            verdictDiv.innerHTML = '<div style="background: rgba(16, 185, 129, 0.2); color: #10B981; padding: 15px; border-radius: 8px; font-weight: bold; margin: 15px 0; text-align: center;">🔒 VERIFIED COMPLETION DETECTED</div>';
        } else {
            document.getElementById('fake-count').innerText = parseInt(document.getElementById('fake-count').innerText) + 1;
            verdictDiv.innerHTML = '<div style="background: rgba(239, 68, 68, 0.2); color: #EF4444; padding: 15px; border-radius: 8px; font-weight: bold; margin: 15px 0; text-align: center;">🚨 FAKE COMPLETION DETECTED</div>';
        }

    } catch (error) {
        document.getElementById('json-agent').textContent = JSON.stringify({ error: "Connection error" }, null, 2);
    }
});
