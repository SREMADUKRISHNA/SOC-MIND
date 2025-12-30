import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.api.server import run_server
from scripts.ingestion.ingest_alerts import run_ingestion
from backend.replay.replay_engine import VSMKReplayGraph
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python backend/main.py [server|ingest|replay] [args]")
        return

    command = sys.argv[1]

    if command == "server":
        run_server()
    elif command == "ingest":
        count = 5
        if len(sys.argv) > 2:
            count = int(sys.argv[2])
        run_ingestion(count)
    elif command == "replay":
        if len(sys.argv) < 3:
            print("Usage: python backend/main.py replay <decision_id>")
            return
        decision_id = sys.argv[2]
        graph = VSMKReplayGraph()
        data = graph.replay_decision(decision_id)
        print(json.dumps(data, indent=2))
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
