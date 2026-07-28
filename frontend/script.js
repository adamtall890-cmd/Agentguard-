const button = document.getElementById("runButton");

button.addEventListener("click", async () => {

    const scenario = document.getElementById("scenario").value;

    document.getElementById("agentStatus").innerHTML =
        "⏳ Agent is executing workflow...";

    document.getElementById("verification").innerHTML =
        "⏳ AgentGuard is verifying business outcome...";

    try {

        const response = await fetch("/outcome", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refund_id: scenario
            })
        });

        const data = await response.json();

        document.getElementById("agentStatus").innerHTML = `
            <span class="success">✅ SUCCESS</span><br>
            Agent reported the workflow completed.
        `;

        if (data.verified) {

            document.getElementById("verification").innerHTML = `
                <span class="success">🟢 VERIFIED</span><br><br>

                ✓ Business outcome confirmed<br>
                ✓ Expected state matches reality<br>
                ✓ Workflow completed successfully
            `;

        } else {

            document.getElementById("verification").innerHTML = `
                <span class="error">🔴 FAKE COMPLETION</span><br><br>

                Agent reported SUCCESS<br>
                Reality check failed<br><br>

                <strong>Reason:</strong><br>
                ${data.reason}
            `;

        }

    }

    catch(error){

        document.getElementById("verification").innerHTML = `
            <span class="error">Server unreachable</span>
        `;

    }

});
