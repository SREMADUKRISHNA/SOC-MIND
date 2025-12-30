document.addEventListener('DOMContentLoaded', () => {
    fetchTimeline();
});

async function fetchTimeline() {
    try {
        const response = await fetch('/api/timeline');
        const data = await response.json();
        renderSidebar(data);
    } catch (error) {
        console.error('Error fetching timeline:', error);
    }
}

function renderSidebar(incidents) {
    const list = document.getElementById('incident-list');
    list.innerHTML = '';

    incidents.forEach(inc => {
        const el = document.createElement('div');
        el.className = 'incident-item';
        el.onclick = () => loadReplay(inc.decision_id, el);
        
        const date = new Date(inc.timestamp * 1000).toLocaleString();
        
        el.innerHTML = `
            <div class="incident-header">
                <span class="verdict-badge verdict-${inc.verdict}">${inc.verdict}</span>
                <span style="font-size: 0.8rem; color: #94a3b8;">${date}</span>
            </div>
            <div style="font-weight: bold; margin-bottom: 0.25rem;">${inc.alert.type}</div>
            <div style="font-size: 0.9rem; color: #94a3b8;">${inc.alert.source}</div>
        `;
        list.appendChild(el);
    });
}

async function loadReplay(decisionId, element) {
    // UI selection
    document.querySelectorAll('.incident-item').forEach(e => e.classList.remove('active'));
    element.classList.add('active');

    try {
        const response = await fetch(`/api/replay/${decisionId}`);
        const data = await response.json();
        renderReplay(data);
    } catch (error) {
        console.error('Error loading replay:', error);
    }
}

function renderReplay(data) {
    const container = document.getElementById('replay-content');
    container.innerHTML = '';
    
    // Header Info
    const header = document.createElement('div');
    header.style.marginBottom = '2rem';
    header.innerHTML = `
        <h2 style="margin: 0 0 0.5rem 0;">Incident Analysis Replay</h2>
        <div style="color: #94a3b8;">Source: ${data.incident_context.alert_source} | Time: ${new Date(data.incident_context.alert_time * 1000).toLocaleString()}</div>
    `;
    container.appendChild(header);

    const path = data.decision_path;

    // Step 1: Signal Analysis
    container.appendChild(createStepCard(
        "Step 1: Signal Strength Analysis",
        path.step_1_signal_analysis.description,
        [{ label: "Signal Score", value: path.step_1_signal_analysis.score }]
    ));

    // Step 2: False Positive Check
    container.appendChild(createStepCard(
        "Step 2: False Positive Probability",
        `Analyzed factors: ${path.step_2_false_positive_check.factors.join(", ")}`,
        [{ label: "FP Probability", value: path.step_2_false_positive_check.probability }]
    ));

    // Step 3: Final Verdict
    const verdict = path.step_3_final_verdict;
    container.appendChild(createStepCard(
        `Step 3: Final Verdict - ${verdict.outcome}`,
        verdict.explanation,
        [{ label: "Confidence", value: verdict.confidence }]
    ));
}

function createStepCard(title, text, metrics) {
    const card = document.createElement('div');
    card.className = 'step-card';
    
    let metricsHtml = '';
    metrics.forEach(m => {
        metricsHtml += `
            <div class="metric-box">
                <span class="metric-value" style="color: var(--accent-blue)">${m.value}</span>
                <span class="metric-label">${m.label}</span>
            </div>
        `;
    });

    card.innerHTML = `
        <div class="step-title">${title}</div>
        <div class="metric-grid">${metricsHtml}</div>
        <div class="explanation-text">${text}</div>
    `;
    return card;
}
