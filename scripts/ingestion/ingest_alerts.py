import time
import uuid
import random
from backend.models.alert import Alert
from backend.core.decision_engine import VSMKDecisionCore
from backend.utils.storage import StorageManager
from backend.utils.logger import logger

def generate_simulated_alerts(count=5):
    alert_types = ["Malware Detected", "Brute Force Attempt", "Policy Violation", "Data Exfiltration", "System Crash"]
    sources = ["edr_agent", "legacy_firewall", "cloud_guard", "printer_logs", "email_gateway"]
    severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    alerts = []
    for _ in range(count):
        a = Alert(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            source=random.choice(sources),
            severity=random.choice(severities),
            type=random.choice(alert_types),
            raw_data={"ip": "192.168.1.10", "user": "admin", "process": "powershell.exe"}
        )
        alerts.append(a)
    return alerts

def run_ingestion(count=5):
    logger.info(f"Starting ingestion of {count} simulated alerts...")
    engine = VSMKDecisionCore()
    storage = StorageManager()
    
    alerts = generate_simulated_alerts(count)
    
    for alert in alerts:
        storage.save_alert(alert)
        decision = engine.analyze(alert)
        storage.save_decision(decision)
        
    logger.info("Ingestion complete.")
