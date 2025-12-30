from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import json
import time

@dataclass
class ReasoningChain:
    signal_strength: float
    false_positive_probability: float
    historical_similarity: float
    business_impact: str # LOW, MEDIUM, HIGH, CRITICAL
    confidence_score: float
    explanation: str
    factors: List[str]

@dataclass
class Decision:
    decision_id: str
    alert_id: str
    timestamp: float
    verdict: str # IGNORE, INVESTIGATE, ESCALATE
    reasoning: ReasoningChain

    def to_dict(self):
        return {
            "decision_id": self.decision_id,
            "alert_id": self.alert_id,
            "timestamp": self.timestamp,
            "verdict": self.verdict,
            "reasoning": asdict(self.reasoning)
        }

    def to_json(self):
        return json.dumps(self.to_dict())
