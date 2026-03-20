import argparse 
from utils.tcp_scan import scan_port_range

def main() : 
    parser = argparse.ArgumentParser(description = "Network Recon Toolkit")
    parser.add_argument("target", help= "Target IP or hostname")
    parser.add_argument("ports", help= "Port range (eg. 1-1024)")

    args = parser.parse_args()  #Reads what users input in  the terminal

    try :
        start,end = map(int, args.ports.split("-"))

        if start < 1 or end > 65535 or start > end :
            raise ValueError
    
    except ValueError :
        print("Invalid port range. Use format like 1-1024 and valid port numbers (1-65535).")
        return  
    
    open_ports = scan_port_range(args.target, start, end)

    print("\nScan complete.")

    for port, banner in sorted(open_ports):
        print(f"Port {port} → {banner}")
  


    
if __name__ == "__main__" :
        main()





    
    
