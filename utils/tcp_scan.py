import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.banner import grab_banner
from utils.service_parser import parse_service_banner
from utils.vuln_checker import check_vulnerability


def scan_port(target: str, port: int, timeout: float):
    """
    Scan a single TCP port.
    Return the port number if open, otherwise None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))

            if result == 0:
                return port

    except Exception:
        pass

    return None


def scan_port_range(
    target: str,
    start: int,
    end: int,
    threads: int = 100,
    timeout: float = 1.0,
    banner: bool = False
):
    """
    Scan a range of TCP ports.
    Returns a list of tuples:
    (port, service, warning)
    """
    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scan_port, target, port, timeout)
            for port in range(start, end + 1)
        ]

        for future in as_completed(futures):
            result = future.result()

            if result is not None:
                port = result

                if banner:
                    raw_banner = grab_banner(target, port)
                else:
                    raw_banner = ""

                service = parse_service_banner(raw_banner, port)
                warning = check_vulnerability(service)

                open_ports.append((port, service, warning))

    return open_ports