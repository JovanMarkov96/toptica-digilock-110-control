import socket

from .errors import ConnectionError110, ParameterError110, ValidationError110


class DigiLockDMS:
    """TCP/IP client for the DigiLock Module Server (DMS) Remote Control Interface.

    The DMS listens on TCP port 60000 (default) and manages the set of DigiLock
    110 hardware modules connected to the host PC.  It exposes metadata about
    connected modules and lets the caller select which module the DUI windows
    (ports 6000x) correspond to.

    For direct laser control use :class:`~toptica_digilock110.dui.DigiLockDUI`
    to connect to the appropriate DUI port (e.g. 60001 for the first module).

    Usage::

        with DigiLockDMS('192.168.0.1') as dms:
            print(dms.get_module_names())
            ports = dms.get_module_port_numbers()
            print(ports)   # e.g. [60001]
    """

    DEFAULT_HOST = '192.168.0.1'
    DEFAULT_PORT = 60000
    _PROMPT = b'> '
    _TERMINATOR = '\r\n'

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                 timeout: float = 5.0) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock: socket.socket | None = None

    # ---- Context manager ----

    def __enter__(self) -> 'DigiLockDMS':
        self.connect()
        return self

    def __exit__(self, *_) -> None:
        self.close()

    # ---- Connection ----

    def connect(self) -> None:
        if self._sock is not None:
            raise ConnectionError110("Already connected. Call close() first.")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._timeout)
            sock.connect((self._host, self._port))
            self._sock = sock
            self._read_until_prompt()
        except OSError as exc:
            self._sock = None
            raise ConnectionError110(
                f"Cannot connect to DMS at {self._host}:{self._port}: {exc}"
            ) from exc

    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None

    # ---- Low-level protocol ----

    def _require_connection(self) -> None:
        if self._sock is None:
            raise ConnectionError110("Not connected. Call connect() or use as context manager.")

    def _read_until_prompt(self) -> str:
        buf = b''
        while not buf.endswith(self._PROMPT):
            try:
                chunk = self._sock.recv(4096)
            except OSError as exc:
                raise ConnectionError110(f"Connection lost while reading: {exc}") from exc
            if not chunk:
                raise ConnectionError110("Remote closed the connection unexpectedly.")
            buf += chunk
        return buf[: -len(self._PROMPT)].decode('ascii', errors='replace').strip()

    def _send_raw(self, cmd: str) -> str:
        self._require_connection()
        try:
            self._sock.sendall((cmd + self._TERMINATOR).encode('ascii'))
        except OSError as exc:
            raise ConnectionError110(f"Send failed: {exc}") from exc
        return self._read_until_prompt()

    def _query(self, cmd: str) -> str:
        raw = self._send_raw(f'{cmd}?')
        if raw.startswith('%% Error:'):
            raise ParameterError110(raw)
        return raw.split('=', 1)[1].strip() if '=' in raw else raw

    def _set(self, cmd: str, value: str) -> None:
        raw = self._send_raw(f'{cmd}={value}')
        if raw.startswith('%% Error:'):
            raise ParameterError110(raw)

    def _query_bool(self, cmd: str) -> bool:
        return self._query(cmd).lower() == 'true'

    def _set_bool(self, cmd: str, value: bool) -> None:
        self._set(cmd, 'true' if value else 'false')

    def _query_int(self, cmd: str) -> int:
        return int(self._query(cmd))

    def _set_int(self, cmd: str, value: int) -> None:
        self._set(cmd, str(value))

    # ---- DMS commands ----

    def get_commandlist(self) -> list[str]:
        """Return all commands available on the DMS."""
        raw = self._query('commandlist')
        return [c.strip() for c in raw.split(',') if c.strip()]

    def get_messages_waiting(self) -> int:
        return self._query_int('messages waiting')

    def get_number_of_modules(self) -> int:
        """Number of DigiLock modules physically connected to the computer."""
        return self._query_int('number of modules')

    def get_number_connected_modules(self) -> int:
        """Number of DigiLock modules with an active DMS connection."""
        return self._query_int('number connected modules')

    def get_module_names(self) -> list[str]:
        """Names of all detected DigiLock modules."""
        raw = self._query('modules:names')
        return [n.strip() for n in raw.split(',') if n.strip()]

    def get_module_port_numbers(self) -> list[int]:
        """DUI TCP port numbers for all detected modules (e.g. [60001])."""
        raw = self._query('modules:port numbers')
        return [int(p.strip()) for p in raw.split(',') if p.strip()]

    def get_module_serial_numbers(self) -> list[str]:
        """Serial numbers of all detected DigiLock modules."""
        raw = self._query('modules:serial numbers')
        return [s.strip() for s in raw.split(',') if s.strip()]

    def get_module_connection_statuses(self) -> list[str]:
        """Connection status strings for all detected modules."""
        raw = self._query('modules:connection status')
        return [s.strip() for s in raw.split(',') if s.strip()]

    def get_selected_module(self) -> int:
        """Index of the currently active DigiLock module (0-based)."""
        return self._query_int('selected module')

    def set_selected_module(self, index: int) -> None:
        if index < 0:
            raise ValidationError110("Module index must be non-negative.")
        self._set_int('selected module', index)

    def get_module_connected(self) -> bool:
        """True if the currently selected module has an established connection."""
        return self._query_bool('module:connect')

    def set_module_connected(self, connected: bool) -> None:
        """Establish or drop the DMS connection to the selected module."""
        self._set_bool('module:connect', connected)

    def get_module_show(self) -> bool:
        """True if the DUI window of the active module is visible."""
        return self._query_bool('module:show')

    def set_module_show(self, visible: bool) -> None:
        self._set_bool('module:show', visible)

    def get_ip_address(self) -> str:
        """IP address of the DMS host computer."""
        return self._query('program:ip address')

    def get_port_number(self) -> int:
        """TCP port number of the DMS."""
        return self._query_int('program:port number')

    def update_module_list(self) -> None:
        """Trigger a rescan for connected DigiLock modules."""
        self._set_bool('program:update module list', True)
