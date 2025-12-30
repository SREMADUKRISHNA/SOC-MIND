from backend.utils.storage import StorageManager
from backend.utils.logger import logger
import json

class VSMKReplayGraph:
    def __init__(self):
        self.storage = StorageManager()

    def get_timeline(self):
        """Returns a list of all decisions with their associated alert data."""
        decisions = self.storage.load_all_decisions()
        timeline = []
        for dec in decisions:
            alert = self.storage.load_alert(dec['alert_id'])
            item = {
                "timestamp": dec['timestamp'],
                "decision_id": dec['decision_id'],
                "verdict": dec['verdict'],
                "alert": alert,
                "reasoning": dec['reasoning']
            }
            timeline.append(item)
        return timeline

    def replay_decision(self, decision_id: str):
        """Returns detailed replay data for a specific decision."""
        logger.info(f"Replaying decision {decision_id}...")
        decision = self.storage.load_decision(decision_id)
        if not decision:
            return {"error": "Decision not found"}
        
        alert = self.storage.load_alert(decision['alert_id'])
        
        replay_data = {
            "meta": {
                "engine": "VSMK-ReplayGraph",
                "mode": "AUDIT"
            },
            "incident_context": {
                "alert_source": alert.get('source', 'Unknown'),
                "alert_time": alert.get('timestamp'),
                "raw_alert": alert
            },
            "decision_path": {
                "step_1_signal_analysis": {
                    "score": decision['reasoning']['signal_strength'],
                    "description": "Signal strength analysis based on severity and keywords."
                },
                "step_2_false_positive_check": {
                    "probability": decision['reasoning']['false_positive_probability'],
                    "factors": decision['reasoning']['factors']
                },
                "step_3_final_verdict": {
                    "outcome": decision['verdict'],
                    "confidence": decision['reasoning']['confidence_score'],
                    "explanation": decision['reasoning']['explanation']
                }
            }
        }
        return replay_data
