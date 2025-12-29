function fillDemo(type) {
    if (type === 'stable') {
        setVal('income_total', 450000);
        setVal('years_employed', 6);
        setVal('income_type', 'State servant');
        setVal('cnt_children', 0);
        setVal('flag_own_car', 'Y');
        setVal('flag_own_realty', 'Y');
    } else {
        setVal('income_total', 120000);
        setVal('years_employed', 0.5);
        setVal('income_type', 'Student');
        setVal('cnt_children', 0);
        setVal('flag_own_car', 'N');
        setVal('flag_own_realty', 'N');
    }
}

function setVal(id, val) {
    const el = document.getElementById(id);
    if (el) el.value = val;
}

const creditForm = document.getElementById('creditForm');
if (creditForm) {
    creditForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const btn = document.getElementById('assessBtn');
        btn.innerText = "Analyzing...";
        btn.disabled = true;

        const data = {
            income_total: document.getElementById('income_total').value,
            years_employed: document.getElementById('years_employed').value,
            income_type: document.getElementById('income_type').value,
            cnt_children: document.getElementById('cnt_children').value,
            flag_own_car: document.getElementById('flag_own_car').value,
            flag_own_realty: document.getElementById('flag_own_realty').value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                updateDashboard(result);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server.');
        } finally {
            btn.innerText = "Assess Creditworthiness";
            btn.disabled = false;
        }
    });
}

function updateDashboard(data) {
    const resultCard = document.getElementById('resultCard');
    if (!resultCard) return;

    resultCard.style.opacity = '1';
    resultCard.style.pointerEvents = 'all';

    document.getElementById('scoreValue').innerText = data.credit_score;
    document.getElementById('decisionText').innerText = data.decision;
    document.getElementById('riskLevel').innerText = `Risk Level: ${data.risk_level} (Default Prob: ${data.prob_default_percent}%)`;
    document.getElementById('explanationText').innerText = data.explanation;

    const circle = document.getElementById('scoreCircle');
    const decisionText = document.getElementById('decisionText');
    let color = '#ec4899';

    if (data.decision.includes('APPROVE') && !data.decision.includes('Conditional')) {
        color = '#22c55e';
    } else if (data.decision.includes('Conditional')) {
        color = '#f59e0b';
    } else {
        color = '#ef4444';
    }

    circle.style.borderColor = color;
    circle.style.boxShadow = `0 0 20px ${color}`;
    decisionText.style.color = color;
}
