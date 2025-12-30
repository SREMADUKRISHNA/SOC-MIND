from dataclasses import dataclass, asdict
from typing import Dict, Any
import json
import time

@dataclass
class Alert:
    id: str
    timestamp: float
    source: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL
    type: str
    raw_data: Dict[str, Any]

    def to_json(self):
        return json.dumps(asdict(self))
    
    @staticmethod
    def from_dict(data: Dict):
        return Alert(
            id=data.get("id"),
            timestamp=data.get("timestamp", time.time()),
            source=data.get("source"),
            severity=data.get("severity"),
            type=data.get("type"),
            raw_data=data.get("raw_data", {})
        )
