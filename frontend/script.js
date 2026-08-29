const runButton = document.getElementById('btn-run');
const workflowSelect = document.getElementById('refund-id');

const agentOutput = document.getElementById('json-agent');
const guardOutput = document.getElementById('json-guard');

const totalChecks = document.getElementById('total-checks');
const verifiedCount = document.getElementById('verified-count');
const fakeCount = document.getElementById('fake-count');

const verdictWrapper = document.getElementById('verdict-wrapper');
const historyRows = document.getElementById('history-rows');


runButton.addEventListener('click', async () => {

    /*
     * Récupère la valeur de l'une des 3 options :
     *
     * verified_workflow
     * partial_completion
     * fake_completion
     */

    const refundId = workflowSelect.value;


    /* Sécurité : aucun scénario vide */

    if (!refundId) {
        return;
    }


    /* =========================
       UI : PROCESSING
    ========================= */

    runButton.disabled = true;

    runButton.innerHTML = '◌ Processing...';


    /*
     * On remet le verdict à zéro pendant
     * l'exécution du workflow.
     */

    verdictWrapper.innerHTML = '';


    agentOutput.textContent = JSON.stringify(
        {
            status: "Executing workflow..."
        },
        null,
        2
    );


    guardOutput.textContent = JSON.stringify(
        {
            status: "Waiting for verification..."
        },
        null,
        2
    );


    try {

        /* =========================
           CALL BACKEND
        ========================= */

        const response = await fetch('/outcome', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                refund_id: refundId
            })

        });


        /*
         * Le serveur a répondu avec une erreur HTTP.
         */

        if (!response.ok) {
            throw new Error(
                `Server returned HTTP ${response.status}`
            );
        }


        const data = await response.json();


        /* =========================
           AGENT EXECUTION
        ========================= */

        agentOutput.textContent =
            JSON.stringify(
                data.agent ?? {
                    status: "No agent result returned."
                },
                null,
                2
            );


        /* =========================
           AGENTGUARD VERIFICATION
        ========================= */

        guardOutput.textContent =
            JSON.stringify(
                data.verification ?? {
                    status: "No verification result returned."
                },
                null,
                2
            );


        /* =========================
           DETERMINE VERDICT
        ========================= */

        const isVerified =
            data.verification &&
            (
                data.verification.verified === true ||
                data.verification === true
            );


        /* =========================
           TOTAL CHECKS
        ========================= */

        const currentTotal =
            parseInt(
                totalChecks.innerText,
                10
            ) || 0;


        totalChecks.innerText =
            currentTotal + 1;


        /* =========================
           VERIFIED
        ========================= */

        if (isVerified) {

            const currentVerified =
                parseInt(
                    verifiedCount.innerText,
                    10
                ) || 0;


            verifiedCount.innerText =
                currentVerified + 1;


            verdictWrapper.innerHTML = `
                <div class="alert-box alert-verified">
                    🔒 VERIFIED COMPLETION DETECTED
                </div>
            `;


            addHistoryRow(
                refundId,
                "Verified"
            );

        }


        /* =========================
           FAKE / NOT VERIFIED
        ========================= */

        else {

            const currentFake =
                parseInt(
                    fakeCount.innerText,
                    10
                ) || 0;


            fakeCount.innerText =
                currentFake + 1;


            verdictWrapper.innerHTML = `
                <div class="alert-box alert-fake">
                    🚨 FAKE COMPLETION DETECTED
                </div>
            `;


            addHistoryRow(
                refundId,
                "Fake Completion"
            );

        }

    }


    catch (error) {

        console.error(
            "AgentGuard error:",
            error
        );


        agentOutput.textContent =
            JSON.stringify(
                {
                    error:
                        "Unable to execute workflow.",
                    details:
                        error.message
                },
                null,
                2
            );


        guardOutput.textContent =
            JSON.stringify(
                {
                    error:
                        "Verification could not be completed."
                },
                null,
                2
            );


        verdictWrapper.innerHTML = `
            <div class="alert-box alert-fake">
                ⚠ VERIFICATION ERROR
            </div>
        `;

    }


    finally {

        runButton.disabled = false;

        runButton.innerHTML =
            '▶ Run Workflow';

    }

});


/* =========================
   HISTORY ROW
========================= */

function addHistoryRow(
    workflowId,
    status
) {

    const now =
        new Date()
            .toTimeString()
            .split(' ')[0];


    const row =
        document.createElement('tr');


    const timeCell =
        document.createElement('td');

    timeCell.textContent =
        now;


    const workflowCell =
        document.createElement('td');

    workflowCell.textContent =
        workflowId;


    const statusCell =
        document.createElement('td');

    statusCell.textContent =
        status;


    if (status === 'Verified') {

        statusCell.style.color =
            'var(--color-verified)';

    } else {

        statusCell.style.color =
            'var(--color-fake)';

    }


    row.appendChild(timeCell);
    row.appendChild(workflowCell);
    row.appendChild(statusCell);


    /*
     * Nouvelle vérification en haut
     * de l'historique.
     */

    historyRows.prepend(row);
}
