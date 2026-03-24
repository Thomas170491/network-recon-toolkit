import subprocess
import re
import platform

def detect_os(target: str) -> str:
    """
    Simple OS detection using TTL from ping.
    Returns a guessed OS based on typical TTL values.
    """
    try:
        # Choose ping command depending on OS
        system_os = platform.system()
        if system_os == "Windows":
            cmd = ["ping", "-n", "1", target]
        else:
            cmd = ["ping", "-c", "1", target]

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        # Find TTL in output
        ttl_match = re.search(r"TTL[=|:](\d+)", output, re.IGNORECASE)
        if not ttl_match:
            return "Unknown"

        ttl = int(ttl_match.group(1))

        # Guess OS based on TTL
        if ttl <= 64:
            return "Linux/Unix"
        elif ttl <= 128:
            return "Windows"
        elif ttl <= 255:
            return "Network device"
        else:
            return "Unknown"

    except Exception:
        return "Unknown"