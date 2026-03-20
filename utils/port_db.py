

# Map common ports to default service names
PORTS = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
}

# Map known banner keywords to service labels
BANNER_KEYWORDS = {
    "SSH": "SSH",
    "OpenSSH": "SSH",
    "HTTP": "HTTP",
    "nginx": "HTTP",
    "Apache": "HTTP",
    "FTP": "FTP",
    "PostgreSQL": "PostgreSQL",
    "MySQL": "MySQL",
}