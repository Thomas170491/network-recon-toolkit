import os 
import json
from datetime import datetime 

def save_results_to_json(target :str , open_ports : list) :
    """
    Save scan results to a JSON file.
    open_ports format: [(port, service, warning), ...]
    """
    # Create a results directory if it doesn't exist
    os.makedirs("results", exist_ok="True")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build data structure
    data = {
        "target " : target,
        "time" : timestamp,
        "open_ports" : []
    }

    for port, service, warning in open_ports :
        data["open_ports"].append({
            "port": port,
            "service": service,
            "warning": warning
        })

    # File name
    filename = f"results/scan_{target}_{timestamp}.json"

    # Save JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[INFO] Results saved to {filename}")



