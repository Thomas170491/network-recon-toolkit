from .port_db import PORTS, BANNER_KEYWORDS

def parse_service_banner(banner :str ,port :int) -> str : 
    """
    Convert a raw banner or port number into a clean service label.
    """
    banner = banner.strip()

    # Try to detect from banner keywords
    for keyword, service_name in BANNER_KEYWORDS.items() :
        if keyword.lower() in banner.lower() :
            #append version if available
            version = extract_version(banner) # added in later
            return f"{service_name}{f' ({version})' if version else ''}"
    
    if port in PORTS :
        return PORTS[port]
    
    return 'Unknown'

def extract_version(banner: str) -> str:
    """
    Try to parse a version number from the banner string.
    Example: "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13" -> "OpenSSH 6.6.1"
    """
    import re

    # SSH example
    ssh_match = re.search(r"OpenSSH[_\- ]?([\d\.]+)", banner, re.IGNORECASE)
    if ssh_match:
        return f"OpenSSH {ssh_match.group(1)}"

    # HTTP example
    http_match = re.search(r"HTTP/[\d\.]+ (\d{3})", banner, re.IGNORECASE)
    if http_match:
        return f"HTTP {http_match.group(1)}"

    return ""