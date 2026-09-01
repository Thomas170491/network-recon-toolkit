import re

from .vuln_db import VULNERABILITIES


def extract_software_and_version(service_label: str):
    """
    Extract software name and version from a service label.

    Example:
    'SSH (OpenSSH 6.6.1)' -> ('OpenSSH', '6.6.1')
    """
    match = re.search(r"\(([^)]+)\)", service_label)

    if not match:
        return None, None

    content = match.group(1)
    parts = content.split()

    if len(parts) < 2:
        return None, None

    software = parts[0]
    version = parts[1]

    return software, version


def version_to_tuple(version: str):
    numbers = re.findall(r"\d+", version)
    return tuple(map(int, numbers))


def check_vulnerability_details(service_label: str) -> dict:
    """
    Return structured vulnerability information for a detected service.

    The local database is intentionally limited. An empty CVE list means
    the version triggered a general outdated-version warning but no
    specific CVE is mapped by this toolkit.
    """
    software, version = extract_software_and_version(service_label)

    result = {
        "warning": "",
        "cves": [],
    }

    if not software or not version:
        return result

    entries = VULNERABILITIES.get(software)

    if not entries:
        return result

    current_version = version_to_tuple(version)

    for entry in entries:
        match_type = entry.get("match", "max")

        if match_type == "exact":
            expected_version = version_to_tuple(
                entry["version"]
            )

            if current_version == expected_version:
                return {
                    "warning": entry["warning"],
                    "cves": list(entry.get("cves", [])),
                }

        elif match_type == "max":
            threshold_version = version_to_tuple(
                entry["max_version"]
            )

            if current_version <= threshold_version:
                return {
                    "warning": entry["warning"],
                    "cves": list(entry.get("cves", [])),
                }
    return result


def check_vulnerability(service_label: str) -> str:
    """
    Backwards-compatible warning-only interface.
    """
    return check_vulnerability_details(
        service_label
    )["warning"]