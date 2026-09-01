from utils.service_parser import parse_service_banner, extract_version
from utils.vuln_checker import (
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