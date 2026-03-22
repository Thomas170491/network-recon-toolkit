# vuln_db.py
# Simple vulnerability database for common services
# Format:
# "Software": [("version_threshold", "warning message")]

VULNERABILITIES = {
    "OpenSSH": [
        ("7.0", "⚠️ Very outdated OpenSSH - multiple known vulnerabilities"),
        ("7.9", "⚠️ Outdated OpenSSH, consider updating"),
    ],
    
    "Apache": [
        ("2.2", "⚠️ Apache 2.2 is end-of-life and vulnerable"),
        ("2.4.49", "⚠️ Apache 2.4.49 vulnerable to path traversal (CVE-2021-41773)"),
    ],
    
    "nginx": [
        ("1.18", "⚠️ Old nginx version, consider updating"),
    ],
    
    "MySQL": [
        ("5.7", "⚠️ MySQL 5.7 is outdated"),
    ],
    
    "PostgreSQL": [
        ("10", "⚠️ PostgreSQL version is outdated"),
    ],
    
    "vsFTPd": [
        ("3.0.3", "⚠️ vsFTPd version may contain known vulnerabilities"),
    ],
    
    "ProFTPD": [
        ("1.3.5", "⚠️ ProFTPD outdated - multiple CVEs exist"),
    ],
    
    "Microsoft-IIS": [
        ("7.5", "⚠️ Old IIS version, consider upgrading"),
    ],
}