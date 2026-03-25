import os
import json
from datetime import datetime


def save_results_to_json(target: str, open_ports: list, os_guess=None):
    """
    Save scan results to a JSON file.
    open_ports format: [(port, service, warning), ...]
    """

    # Create results directory
    os.makedirs("results", exist_ok=True)

    # Safe timestamp for filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Build data structure
    data = {
        "target": target,
        "scan_time": timestamp,
        "os_guess": os_guess,
        "open_ports": open_ports
    }



    # File name
    filename = f"results/scan_{target}_{timestamp}.json"

    # Save JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[INFO] Results saved to {filename}")