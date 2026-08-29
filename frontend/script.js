document.getElementById('btn-run').addEventListener('click', async () => {
    const selectedWorkflow = document.getElementById('refund-id').value;
    const btn = document.getElementById('btn-run');
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';

    try {
        const response = await fetch('/outcome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refund_id: selectedWorkflow })
        });
        const data = await response.json();

        // Affichage brut de vos objets JSON d'origine
        document.getElementById('json-agent').textContent = JSON.stringify(data.agent, null, 2);
        document.getElementById('json-guard').textContent = JSON.stringify(data.verification, null, 2);

        // Analyse de la réponse pour vos compteurs
        const isVerified = data.verification && (data.verification.verified === true || data.verification === true);
        
        document.getElementById('total-checks').innerText = parseInt(document.getElementById('total-checks').innerText) + 1;

        if (isVerified) {
            document.getElementById('verified-count').innerText = parseInt(document.getElementById('verified-count').innerText) + 1;
        } else {
            document.getElementById('fake-count').innerText = parseInt(document.getElementById('fake-count').innerText) + 1;
        }

    } catch (error) {
        document.getElementById('json-agent').textContent = JSON.stringify({ error: "Node connection failure" }, null, 2);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Run Workflow';
    }
});
