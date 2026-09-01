# vuln_db.py
# Small local vulnerability/reference database for common services.
#
# This is intentionally limited and is not a replacement for
# authoritative vulnerability sources such as NVD or vendor advisories.

VULNERABILITIES = {
    "OpenSSH": [
        {
            "max_version": "7.0",
            "warning": "⚠️ Very outdated OpenSSH - multiple known vulnerabilities",
            "cves": [],
        },
        {
            "max_version": "7.9",
            "warning": "⚠️ Outdated OpenSSH, consider updating",
            "cves": [],
        },
    ],

    "Apache": [
        {
            "max_version": "2.2",
            "warning": "⚠️ Apache 2.2 is end-of-life and vulnerable",
            "cves": [],
        },
        {
            "version": "2.4.49",
            "match": "exact",
            "warning": "⚠️ Apache 2.4.49 vulnerable to path traversal",
            "cves": ["CVE-2021-41773"],
        },
    ],
        

    "nginx": [
        {
            "max_version": "1.18",
            "warning": "⚠️ Old nginx version, consider updating",
            "cves": [],
        },
    ],

    "MySQL": [
        {
            "max_version": "5.7",
            "warning": "⚠️ MySQL 5.7 is outdated",
            "cves": [],
        },
    ],

    "PostgreSQL": [
        {
            "max_version": "10",
            "warning": "⚠️ PostgreSQL version is outdated",
            "cves": [],
        },
    ],

    "vsFTPd": [
        {
            "max_version": "3.0.3",
            "warning": "⚠️ vsFTPd version may contain known vulnerabilities",
            "cves": [],
        },
    ],

    "ProFTPD": [
        {
            "max_version": "1.3.5",
            "warning": "⚠️ ProFTPD outdated - multiple CVEs exist",
            "cves": [],
        },
    ],

    "Microsoft-IIS": [
        {
            "max_version": "7.5",
            "warning": "⚠️ Old IIS version, consider upgrading",
            "cves": [],
        },
    ],
}