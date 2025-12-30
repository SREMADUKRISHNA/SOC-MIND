# SOC-MIND (Security Operations Center – Memory, Insight, Narrative, Decision)

**SOC-MIND** is a specialized decision memory and replay engine designed for modern Security Operations Centers (SOCs). Unlike traditional SIEMs or SOARs that focus on alerting and automation, SOC-MIND focuses on the *cognitive process* of the analyst/AI decision-making.

It records, explains, and allows for the step-by-step replay of why a specific security alert was ignored, investigated, or escalated.

## 🚀 Unique Value Proposition
- **Decision Replay Engine (VSMK-ReplayGraph)**: Reconstructs the exact reasoning state at the moment of decision.
- **Explainable AI (XAI)**: Instead of black-box scoring, provides a human-readable reasoning chain (Signal Strength, FP Probability, Business Impact).
- **Audit Lens**: Perfect for compliance and training new analysts by reviewing past decisions.
- **Offline & Private**: Runs entirely locally with no external API dependencies.

## 📂 Architecture
- **VSMK-DecisionCore**: Rule-guided probabilistic engine that mimics expert analyst intuition.
- **VSMK-ReplayGraph**: reconstructing timeline and context for post-incident review.
- **Frontend**: Lightweight, dependency-free dashboard for visualization.

## 🛠 Usage

### 1. Setup
No installation required other than Python 3. Standard libraries only.

### 2. Ingest Simulated Alerts
Generate synthetic alerts and process them through the decision core:
```bash
python backend/main.py ingest 10
```
This will create JSON artifacts in `data/alerts` and `data/decisions`.

### 3. Start the Dashboard
Launch the visualization server:
```bash
python backend/main.py server
```
Access the UI at: `http://localhost:8000`

### 4. CLI Replay
Replay a specific decision via command line:
```bash
python backend/main.py replay <decision_id>
```

## 🏗 Project Structure
- `backend/`: Python core logic, API server, and engines.
- `frontend/`: HTML/CSS/JS dashboard.
- `data/`: JSON storage for alerts and decisions.
- `scripts/`: Utilities for ingestion and setup.

---
*Built by VSMK CLI Agent*
