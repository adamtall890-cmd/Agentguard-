const API = "https://agentguard-production-8f4f.up.railway.app/outcome";

let total = 0;
let verified = 0;
let failed = 0;

async function runWorkflow() {

    const scenario = document.getElementById("scenario").value;

    const mapping = {
        "lead_ok": "refund_ok",
        "lead_partial": "refund_partial",
        "lead_missing": "refund_missing"
    };

    const refund_id = mapping[scenario];

    const response = await fetch(API, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            refund_id
        })

    });

    const data = await response.json();

    document.getElementById("agent").textContent =
        JSON.stringify(data.agent, null, 2);

    document.getElementById("verification").textContent =
        JSON.stringify(data.verification, null, 2);

    total++;

    document.getElementById("total").innerText = total;

    const status = document.getElementById("status");

    if (data.verification.verified) {

        verified++;

        document.getElementById("verified").innerText = verified;

        status.className = "status ok";

        status.innerHTML =
            "✅ VERIFIED";

    } else {

        failed++;

        document.getElementById("failed").innerText = failed;

        status.className = "status fail";

        status.innerHTML =
            "🚨 FAKE COMPLETION DETECTED";

    }

    const tbody = document.getElementById("history");

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${new Date().toLocaleTimeString()}</td>
        <td>${refund_id}</td>
        <td>${data.verification.verified ? "Verified" : "Fake Completion"}</td>
    `;

    tbody.prepend(row);

}