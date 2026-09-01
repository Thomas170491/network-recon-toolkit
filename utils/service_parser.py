from .port_db import PORTS, BANNER_KEYWORDS
import re 

def parse_service_banner(banner :str ,port :int) -> str : 
    """
    Convert a raw banner or port number into a clean service label.
    """
    banner = banner.strip()

    # Try to detect from banner keywords
    for keyword, service_name in BANNER_KEYWORDS.items() :
        if keyword.lower() in banner.lower() :
            #append version if available
            version = extract_version(banner,service_name) # added in later
            return f"{service_name}{f' ({version})' if version else ''}"
    
    if port in PORTS :
        return PORTS[port]
    
    return 'Unknown'

def extract_version(banner: str, service_name: str) -> str:
    """
    Try to extract a version number from a banner string.
    Currently supports SSH HTTP and FTP.
    """

    # ---- SSH ----
    if service_name == "SSH":
        ssh_match = re.search(r"OpenSSH[_\- ]?([\d\.]+)", banner, re.IGNORECASE)
        if ssh_match:
            return f"OpenSSH {ssh_match.group(1)}"

    # ---- HTTP ----
    if service_name == "HTTP":
    # Prefer server software/version when exposed by the server.
        server_match = re.search(
        r"^Server:\s*([^\r\n]+)",
        banner,
        re.IGNORECASE | re.MULTILINE,
    )

    if server_match:
        server_value = server_match.group(1).strip()

        version_match = re.match(
            r"([A-Za-z0-9._-]+)[/\s-]+(\d+(?:\.\d+)+)",
            server_value,
        )

        if version_match:
            software = version_match.group(1)
            version = version_match.group(2)

            return f"{software} {version}"

    # Fall back to HTTP status when no server/version is available.
    http_match = re.search(
        r"HTTP/[\d\.]+\s+(\d{3})",
        banner,
        re.IGNORECASE,
    )

    if http_match:
        return f"Status {http_match.group(1)}"

    # ---- FTP  ----
    if service_name == "FTP":
        ftp_match = re.search(r"FTP[\s\-]?([\d\.]+)", banner, re.IGNORECASE)
        if ftp_match:
            return ftp_match.group(1)

    # Add more services here if needed

    return None