import socket


def probe_digilock_dms(host: str, port: int = 60000, timeout: float = 2.0) -> bool:
    """Return True if a DigiLock Module Server (DMS) RCI is reachable at host:port.

    Connects, reads enough bytes to look for the ``> `` prompt, then closes.
    Does not raise; returns False on any error.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            buf = b''
            while len(buf) < 512:
                chunk = sock.recv(256)
                if not chunk:
                    break
                buf += chunk
                if b'> ' in buf:
                    return True
    except OSError:
        pass
    return False


def probe_digilock_dui(host: str, port: int = 60001, timeout: float = 2.0) -> bool:
    """Return True if a DigiLock User Interface (DUI) RCI is reachable at host:port."""
    return probe_digilock_dms(host, port, timeout)


def list_digilock_dui_ports(
    host: str,
    start_port: int = 60001,
    n: int = 8,
    timeout: float = 2.0,
) -> list[int]:
    """Probe ports ``start_port`` through ``start_port + n - 1`` on host.

    Returns a list of ports that responded with a DigiLock DUI RCI prompt.
    Useful for discovering how many modules are available without connecting
    to the DMS first.
    """
    return [
        port
        for port in range(start_port, start_port + n)
        if probe_digilock_dui(host, port, timeout)
    ]
