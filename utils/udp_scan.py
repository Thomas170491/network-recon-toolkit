import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_udp_port(target :str , port :int , timeout :float = 1.0 ) :    
    """
    Scan a single UDP port. Returns the port number if open or filtered.
    Note: UDP is tricky — we assume open if no ICMP port unreachable is received.
    """
    try :
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s :
            s.settimeout(timeout)

            #Send an empty UDP Packet
            s.sendto(b'\x00', (target,port))

            try :
                #Wait for a response (any response means port is open)
                data,_ = s.recvfrom(1024)
                return port
            except socket.timeout:
                #No response -> open/filtered
                return port
            except ConnectionRefusedError :
                #ICMP Port Unreachable -> port is closed
                return None
    except Exception :
        return None



def scan_udp_range(target: str, start: int, end: int, threads: int = 100, timeout: float = 1.0):
    """
    Scan a range of UDP ports using multithreading.
    Returns a list of open/filtered ports.
    """
    print(f"Scanning UDP ports {start}-{end} on {target}...\n")
    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scan_udp_port, target, port, timeout)
            for port in range(start, end + 1)
        ]

        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
                print(f"[OPEN/Filtered] UDP Port {result}")

    return open_ports
