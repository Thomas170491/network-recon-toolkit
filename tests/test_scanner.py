from utils.service_parser import parse_service_banner, extract_version
from utils.vuln_checker import (
    check_vulnerability_details,
    extract_software_and_version,
    version_to_tuple,
    check_vulnerability,
)


def test_parse_ssh_banner_with_version():
    banner = "SSH-2.0-OpenSSH_6.6.1"

    result = parse_service_banner(
        banner,
        22,
    )

    assert result == "SSH (OpenSSH 6.6.1)"


def test_parse_http_status_banner():
    banner = "HTTP/1.1 200 OK"

    result = parse_service_banner(
        banner,
        80,
    )

    assert result == "HTTP (Status 200)"


def test_fallback_to_known_port():
    result = parse_service_banner(
        "",
        22,
    )

    assert result == "SSH"


def test_unknown_service():
    result = parse_service_banner(
        "",
        65000,
    )

    assert result == "Unknown"


def test_extract_ssh_version():
    result = extract_version(
        "SSH-2.0-OpenSSH_9.3",
        "SSH",
    )

    assert result == "OpenSSH 9.3"


def test_extract_software_and_version():
    software, version = extract_software_and_version(
        "SSH (OpenSSH 6.6.1)"
    )

    assert software == "OpenSSH"
    assert version == "6.6.1"


def test_version_to_tuple():
    assert version_to_tuple("7.9") == (7, 9)
    assert version_to_tuple("2.4.49") == (2, 4, 49)


def test_old_openssh_generates_warning():
    warning = check_vulnerability(
        "SSH (OpenSSH 6.6.1)"
    )

    assert "outdated OpenSSH" in warning


def test_current_openssh_has_no_warning():
    warning = check_vulnerability(
        "SSH (OpenSSH 9.3)"
    )

    assert warning == ""


def test_service_without_version_has_no_warning():
    warning = check_vulnerability(
        "SSH"
    )

    assert warning == ""

def test_vulnerability_details_returns_structured_result():
    result = check_vulnerability_details(
        "SSH (OpenSSH 6.6.1)"
    )

    assert "warning" in result
    assert "cves" in result
    assert isinstance(result["cves"], list)


def test_known_apache_cve_is_returned():
    result = check_vulnerability_details(
        "HTTP (Apache 2.4.49)"
    )

    assert result["warning"]
    assert result["cves"] == [
        "CVE-2021-41773"
    ]


def test_general_warning_does_not_invent_cves():
    result = check_vulnerability_details(
        "SSH (OpenSSH 6.6.1)"
    )

    assert result["warning"]
    assert result["cves"] == []


def test_current_version_returns_empty_vulnerability_result():
    result = check_vulnerability_details(
        "SSH (OpenSSH 9.3)"
    )

    assert result == {
        "warning": "",
        "cves": [],
    }

def test_apache_banner_reaches_cve_detection():
    banner = (
        "HTTP/1.1 200 OK\r\n"
        "Server: Apache/2.4.49\r\n"
        "Content-Length: 0\r\n"
        "\r\n"
    )

    service = parse_service_banner(
        banner,
        80,
    )

    assert service == "HTTP (Apache 2.4.49)"

    result = check_vulnerability_details(service)

    assert result["warning"]
    assert result["cves"] == [
        "CVE-2021-41773"
    ]

def test_apache_older_version_does_not_get_41773():
    result = check_vulnerability_details(
        "HTTP (Apache 2.4.48)"
    )

    assert "CVE-2021-41773" not in result["cves"]

def test_unknown_ssh_version_does_not_crash():
    result = extract_version(
        "SSH custom-server",
        "SSH",
    )

    assert result is None