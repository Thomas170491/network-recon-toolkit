import re 
from vuln_db import VULNERABILITIES

def extract_software_and_version(service_label : str) :
    """
    Extract software name and version from service label.
    Example: 'SSH (OpenSSH 6.6.1)' -> ('OpenSSH', '6.6.1')

    """

    match = re.search(r"\(.*?\)", service_label)

    if not match :
        return None, None
    
    content = match.group(1)
    parts = content.split()

    if len(parts) >= 2 :
        software = parts[0]
        version = parts[1]
        return software, version
    
    return None, None

def version_to_tuple(version :str ) :
    numbers = re.findall(r"\d+", version )
    return tuple(map(int,numbers))

def check_vulnerability(service_label: str) -> str:
    software, version = extract_software_and_version(service_label)

    if not software or not version:
        return ""

    if software in VULNERABILITIES:
        current_version = version_to_tuple(version)

        for threshold, warning in VULNERABILITIES[software]:
            threshold_version = version_to_tuple(threshold)

            if current_version <= threshold_version:
                return warning

    return ""