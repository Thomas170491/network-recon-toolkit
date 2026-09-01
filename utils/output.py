import os
import json,csv 
from datetime import datetime


def save_results_to_json(target: str, open_ports: list, os_guess=None):
    """
    Save scan results to a JSON file.
    open_ports contains structured scan-result dictionaries.
    """

    # Create results directory
    os.makedirs("results/json-scans", exist_ok=True)

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
    filename = f"results/json-scans/scan_{target}_{timestamp}.json"

    # Save JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[INFO] Results saved to {filename}")

def save_results_to_csv(target :str, open_ports : dict, os_guess=None) :
    os.makedirs("results/csv-scans", exist_ok=True)
    timestamp_csv = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"results/csv-scans/scan_{target}_{timestamp_csv}.csv"

    with open(filename, 'w', newline="") as f:
        writer=csv.writer(f)

         # Metadata
        writer.writerow(["Target", target])
        writer.writerow(["Scan Time", timestamp_csv])
        writer.writerow(["OS Guess", os_guess if os_guess else "Unknown"])
        writer.writerow([])

        # Header
        writer.writerow([
                "Port",
                "Protocol",
                "Service",
                "Warning",
                "CVEs",
            ])

        # Data
        for entry in open_ports:
           writer.writerow([
            entry.get("port"),
            entry.get("protocol"),
            entry.get("service"),
            entry.get("warning"),
            ", ".join(entry.get("cves", [])),
        ])
    print(f"\n[INFO] Results saved to {filename}")





