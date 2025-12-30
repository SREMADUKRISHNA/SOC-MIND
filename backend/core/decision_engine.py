import time
import uuid
import random
from backend.models.alert import Alert
from backend.models.decision import Decision, ReasoningChain
from backend.utils.logger import logger

class VSMKDecisionCore:
    def __init__(self):
        logger.info("Initializing VSMK-DecisionCore...")
        # Simulated 'Knowledge Base'
        self.critical_keywords = ["ransomware", "root", "unauthorized_access", "exfiltration"]
        self.noisy_sources = ["legacy_firewall", "printer_logs"]
        self.high_fidelity_sources = ["edr_agent", "cloud_guard"]

    def analyze(self, alert: Alert) -> Decision:
        logger.info(f"Analyzing alert {alert.id} from {alert.source}...")
        
        # 1. Calculate Signal Strength
        signal_strength = 0.5
        if alert.severity == "CRITICAL":
            signal_strength += 0.4
        elif alert.severity == "HIGH":
            signal_strength += 0.2
        
        if any(kw in str(alert.raw_data).lower() for kw in self.critical_keywords):
            signal_strength += 0.3
            
        signal_strength = min(1.0, signal_strength)

        # 2. Calculate False Positive Probability
        fp_prob = 0.2
        if alert.source in self.noisy_sources:
            fp_prob += 0.4
        elif alert.source in self.high_fidelity_sources:
            fp_prob -= 0.1
        
        # Random noise to simulate real-world variance
        fp_prob += random.uniform(-0.05, 0.05)
        fp_prob = max(0.0, min(1.0, fp_prob))

        # 3. Determine Verdict
        confidence = (signal_strength * (1 - fp_prob))
        verdict = "IGNORE"
        if confidence > 0.8:
            verdict = "ESCALATE"
        elif confidence > 0.4:
            verdict = "INVESTIGATE"

        # 4. Generate Reasoning
        explanation = self._generate_explanation(alert, verdict, signal_strength, fp_prob)
        
        reasoning = ReasoningChain(
            signal_strength=round(signal_strength, 2),
            false_positive_probability=round(fp_prob, 2),
            historical_similarity=round(random.uniform(0.1, 0.9), 2), # Simulated
            business_impact=alert.severity if alert.severity else "MEDIUM",
            confidence_score=round(confidence, 2),
            explanation=explanation,
            factors=[alert.source, alert.type]
        )

        decision = Decision(
            decision_id=str(uuid.uuid4()),
            alert_id=alert.id,
            timestamp=time.time(),
            verdict=verdict,
            reasoning=reasoning
        )
        
        logger.info(f"Decision for {alert.id}: {verdict} (Confidence: {confidence:.2f})")
        return decision

    def _generate_explanation(self, alert, verdict, signal, fp) -> str:
        lines = []
        lines.append(f"VSMK-DecisionCore evaluated alert '{alert.type}' from source '{alert.source}'.")
        
        if verdict == "ESCALATE":
            lines.append(f"CRITICAL: High signal strength ({signal:.2f}) combined with low false positive probability ({fp:.2f}) necessitates immediate escalation.")
            lines.append("Key indicators of compromise found in raw data.")
        elif verdict == "INVESTIGATE":
            lines.append(f"Anomaly detected. Signal strength ({signal:.2f}) is significant, but false positive chance ({fp:.2f}) requires human verification.")
        else:
            lines.append(f"Suppressed. Alert exhibits characteristics of noise (FP Prob: {fp:.2f}) or low operational impact.")
            
        return " ".join(lines)
