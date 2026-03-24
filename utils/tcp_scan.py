import socket
from concurrent.futures import ThreadPoolExecutor,as_completed
from utils.banner import grab_banner
from utils.service_parser import parse_service_banner
from utils.vuln_checker  import check_vulnerability


def scan_port(target :str , port :int) :
    try:
        #Creation of a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :

            #Set a timeout so the scan doesn't hang too long
            s.settimeout(0.5)

            #Try to connect to the target on the given port
            #commect_ex returns 0 if the connection is successful (port is open)
            result = s.connect_ex(( target,port))

            if result ==0 : 
                return port
            
    except Exception :
        pass

    return None

def scan_port_range(target: str, start: int, end: int):
    
    print(f"Scanning {target} from port {start} to {end}...\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        
        # Submit all tasks and store futures
        futures = [
            executor.submit(scan_port, target, port)
            for port in range(start, end + 1)
        ]

        # Process results as they complete (NOT in order)
        for future in as_completed(futures):
            result = future.result()
            if result:
                #Grab banner
                banner = grab_banner(target,result)

                #Detect ervice and version
                service = parse_service_banner(banner, result)

                #Check vulnerabilities
                warning = check_vulnerability(service)

                #Store results 
                open_ports.append((result, service,warning))
        print("\nScan complete.\n")

        for port, service, warning in sorted(open_ports):
            if warning:
                print(f"[OPEN] Port {port} -> {service} -> {warning}")
            else :    
                print(f"[OPEN] Port {port} -> {service}")


    return open_ports






