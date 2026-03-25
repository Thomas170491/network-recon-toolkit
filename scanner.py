import argparse
from utils.tcp_scan import scan_port_range
from utils.udp_scan import scan_udp_range
from utils.output import save_results_to_json
from utils.os_detection import detect_os


def main():
    parser = argparse.ArgumentParser(description="Network Recon Toolkit")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("ports", help="Port range (eg. 1-1024)")
    parser.add_argument("--banner", action="store_true", help="Grab service banners")
    parser.add_argument("--os", action="store_true", help="Perform OS detection")
    parser.add_argument("--udp", action="store_true", help="Scan UDP ports")
    parser.add_argument("--output", choices=["json", "csv"], default="json", help="Output format")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds")

    args = parser.parse_args()

    # Validate port range
    try:
        start, end = map(int, args.ports.split("-"))
        if start < 1 or end > 65535 or start > end:
            raise ValueError
    except ValueError:
        print("Invalid port range. Use format like 1-1024 and valid port numbers (1-65535).")
        return

    open_ports = []

    # --- TCP Scan ---
    tcp_ports = scan_port_range(
        args.target,
        start,
        end,
        threads=args.threads,
        timeout=args.timeout,
        banner=args.banner
    )

    for port, service, warning in tcp_ports:
        open_ports.append({
            "port": port,
            "protocol": "TCP",
            "service": service,
            "warning": warning
        })

    # --- UDP Scan ---
    if args.udp:
        udp_ports = scan_udp_range(
            args.target,
            start,
            end,
            threads=args.threads,
            timeout=args.timeout
        )

        for port in udp_ports:
            open_ports.append({
                "port": port,
                "protocol": "UDP",
                "service": "Unknown",
                "warning": None
            })

    # --- OS Detection ---
    os_guess = None
    if args.os:
        os_guess = detect_os(args.target)

    # --- Print Summary ---
    print("\nScan complete.\n")
    for entry in sorted(open_ports, key=lambda x: (x["protocol"], x["port"])):
        line = f"[OPEN] {entry['protocol']} Port {entry['port']}"
        if entry["service"]:
            line += f" -> {entry['service']}"
        if entry["warning"]:
            line += f" -> {entry['warning']}"
        print(line)

    if os_guess:
        print(f"\nDetected OS: {os_guess}")

    # --- Save JSON ---
    if args.output == "json":
        save_results_to_json(args.target, open_ports, os_guess)


if __name__ == "__main__":
    main()