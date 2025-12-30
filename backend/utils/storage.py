import json
import os
from typing import List, Dict
from backend.utils.logger import logger
from backend.models.alert import Alert
from backend.models.decision import Decision

class StorageManager:
    def __init__(self, alerts_dir="data/alerts", decisions_dir="data/decisions"):
        self.alerts_dir = alerts_dir
        self.decisions_dir = decisions_dir
        os.makedirs(self.alerts_dir, exist_ok=True)
        os.makedirs(self.decisions_dir, exist_ok=True)

    def save_alert(self, alert: Alert):
        path = os.path.join(self.alerts_dir, f"{alert.id}.json")
        with open(path, 'w') as f:
            f.write(alert.to_json())

    def save_decision(self, decision: Decision):
        path = os.path.join(self.decisions_dir, f"{decision.decision_id}.json")
        with open(path, 'w') as f:
            f.write(decision.to_json())

    def load_decision(self, decision_id: str) -> Dict:
        path = os.path.join(self.decisions_dir, f"{decision_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return json.load(f)

    def load_all_decisions(self) -> List[Dict]:
        decisions = []
        for f_name in os.listdir(self.decisions_dir):
            if f_name.endswith(".json"):
                with open(os.path.join(self.decisions_dir, f_name), 'r') as f:
                    decisions.append(json.load(f))
        # Sort by timestamp descending
        decisions.sort(key=lambda x: x['timestamp'], reverse=True)
        return decisions

    def load_alert(self, alert_id: str) -> Dict:
        # Since we might not know the alert file name if it doesn't match ID exactly, 
        # but here we enforced id=filename.
        path = os.path.join(self.alerts_dir, f"{alert_id}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
