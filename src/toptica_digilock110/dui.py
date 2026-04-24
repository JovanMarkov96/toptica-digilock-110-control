import socket

from .errors import ConnectionError110, ParameterError110, ValidationError110


class DigiLockDUI:
    """TCP/IP client for the DigiLock 110 User Interface Remote Control Interface (DUI RCI).

    Each DigiLock 110 module exposes a DUI on TCP port 6000x, where x is the
    module index (default port 60001 for the first module).  Commands follow
    the text protocol described in the DigiLock 110 RCI Manual (Toptica, 2023):
    - Query:  ``cmd?\\r\\n``   → device replies ``cmd=value\\r\\n> ``
    - Set:    ``cmd=value\\r\\n`` → device replies ``> ``
    - Errors: ``%% Error: <description>``

    Usage::

        with DigiLockDUI('192.168.0.1', 60001) as dui:
            print(dui.get_commandlist())
            dui.set_scan_frequency(10.0)
            dui.set_scan_enabled(True)
    """

    DEFAULT_HOST = '192.168.0.1'
    DEFAULT_PORT = 60001
    _PROMPT = b'> '
    _TERMINATOR = '\r\n'

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                 timeout: float = 5.0) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock: socket.socket | None = None

    # ---- Context manager ----

    def __enter__(self) -> 'DigiLockDUI':
        self.connect()
        return self

    def __exit__(self, *_) -> None:
        self.close()

    # ---- Connection ----

    def connect(self) -> None:
        """Open TCP connection to the DUI RCI and consume the welcome prompt."""
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
                f"Cannot connect to {self._host}:{self._port}: {exc}"
            ) from exc

    def close(self) -> None:
        """Close the TCP connection."""
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

    def _query_float(self, cmd: str) -> float:
        return float(self._query(cmd))

    def _set_float(self, cmd: str, value: float) -> None:
        self._set(cmd, repr(value))

    def _query_int(self, cmd: str) -> int:
        return int(self._query(cmd))

    def _set_int(self, cmd: str, value: int) -> None:
        self._set(cmd, str(value))

    # ---- Utility ----

    def get_commandlist(self) -> list[str]:
        """Return all commands available on this DUI."""
        raw = self._query('commandlist')
        return [c.strip() for c in raw.split(',') if c.strip()]

    def get_messages_waiting(self) -> int:
        """Number of messages waiting in the RCI command queue."""
        return self._query_int('messages waiting')

    def get_range(self, cmd: str) -> str:
        """Query the allowed range of a parameter: ``cmd.range?``."""
        raw = self._send_raw(f'{cmd}.range?')
        if raw.startswith('%% Error:'):
            raise ParameterError110(raw)
        return raw.split('=', 1)[1].strip() if '=' in raw else raw

    def get_help(self, cmd: str) -> str:
        """Query the help string of a parameter: ``cmd.help?``."""
        raw = self._send_raw(f'{cmd}.help?')
        if raw.startswith('%% Error:'):
            raise ParameterError110(raw)
        return raw.split('=', 1)[1].strip() if '=' in raw else raw

    # ---- Scan module ----

    def get_scan_enabled(self) -> bool:
        return self._query_bool('scan:enable')

    def set_scan_enabled(self, enabled: bool) -> None:
        self._set_bool('scan:enable', enabled)

    def get_scan_frequency(self) -> float:
        return self._query_float('scan:frequency')

    def set_scan_frequency(self, hz: float) -> None:
        if hz <= 0:
            raise ValidationError110("Scan frequency must be positive.")
        self._set_float('scan:frequency', hz)

    def get_scan_amplitude(self) -> float:
        return self._query_float('scan:amplitude')

    def set_scan_amplitude(self, volts: float) -> None:
        if volts < 0:
            raise ValidationError110("Scan amplitude must be non-negative.")
        self._set_float('scan:amplitude', volts)

    def get_scan_output(self) -> str:
        return self._query('scan:output')

    def set_scan_output(self, channel: str) -> None:
        self._set('scan:output', channel)

    def get_scan_waveform(self) -> str:
        return self._query('scan:signal type')

    def set_scan_waveform(self, waveform) -> None:
        """Set scan waveform. Accepts a ScanWaveform enum or a plain string."""
        value = waveform.value if hasattr(waveform, 'value') else str(waveform)
        self._set('scan:signal type', value)

    # ---- PID 1 ----

    def get_pid1_proportional(self) -> float:
        return self._query_float('pid1:proportional')

    def set_pid1_proportional(self, gain: float) -> None:
        self._set_float('pid1:proportional', gain)

    def get_pid1_integral(self) -> float:
        return self._query_float('pid1:integral')

    def set_pid1_integral(self, gain: float) -> None:
        self._set_float('pid1:integral', gain)

    def get_pid1_differential(self) -> float:
        return self._query_float('pid1:differential')

    def set_pid1_differential(self, gain: float) -> None:
        self._set_float('pid1:differential', gain)

    def get_pid1_gain(self) -> float:
        return self._query_float('pid1:gain')

    def set_pid1_gain(self, gain: float) -> None:
        self._set_float('pid1:gain', gain)

    def get_pid1_lock_enabled(self) -> bool:
        return self._query_bool('pid1:lock:enable')

    def set_pid1_lock_enabled(self, enabled: bool) -> None:
        self._set_bool('pid1:lock:enable', enabled)

    def get_pid1_lock_hold(self) -> bool:
        return self._query_bool('pid1:lock:hold')

    def set_pid1_lock_hold(self, hold: bool) -> None:
        self._set_bool('pid1:lock:hold', hold)

    def get_pid1_lock_state(self) -> bool:
        """Read-only: current lock status of PID 1."""
        return self._query_bool('pid1:lock:state')

    def get_pid1_hold_state(self) -> bool:
        """Read-only: hold status of PID 1."""
        return self._query_bool('pid1:hold:state')

    def get_pid1_regulating(self) -> bool:
        """Read-only: True when PID 1 is actively regulating."""
        return self._query_bool('pid1:regulating state')

    def get_pid1_input(self) -> str:
        return self._query('pid1:input')

    def set_pid1_input(self, channel: str) -> None:
        self._set('pid1:input', channel)

    def get_pid1_output(self) -> str:
        return self._query('pid1:output')

    def set_pid1_output(self, channel: str) -> None:
        self._set('pid1:output', channel)

    def get_pid1_setpoint(self) -> float:
        return self._query_float('pid1:setpoint')

    def set_pid1_setpoint(self, value: float) -> None:
        self._set_float('pid1:setpoint', value)

    def get_pid1_sign(self) -> bool:
        return self._query_bool('pid1:sign')

    def set_pid1_sign(self, positive: bool) -> None:
        self._set_bool('pid1:sign', positive)

    def get_pid1_slope(self) -> bool:
        return self._query_bool('pid1:slope')

    def set_pid1_slope(self, positive_slope: bool) -> None:
        self._set_bool('pid1:slope', positive_slope)

    def get_pid1_relock_enabled(self) -> bool:
        return self._query_bool('pid1:relock:enable')

    def set_pid1_relock_enabled(self, enabled: bool) -> None:
        self._set_bool('pid1:relock:enable', enabled)

    def get_pid1_relock_frequency(self) -> float:
        return self._query_float('pid1:relock:frequency')

    def set_pid1_relock_frequency(self, hz: float) -> None:
        self._set_float('pid1:relock:frequency', hz)

    def get_pid1_relock_amplitude(self) -> float:
        return self._query_float('pid1:relock:amplitude')

    def set_pid1_relock_amplitude(self, volts: float) -> None:
        self._set_float('pid1:relock:amplitude', volts)

    def get_pid1_relock_output(self) -> str:
        return self._query('pid1:relock:output')

    def set_pid1_relock_output(self, channel: str) -> None:
        self._set('pid1:relock:output', channel)

    def get_pid1_limit_enabled(self) -> bool:
        return self._query_bool('pid1:limit enable')

    def set_pid1_limit_enabled(self, enabled: bool) -> None:
        self._set_bool('pid1:limit enable', enabled)

    def get_pid1_limit_max(self) -> float:
        return self._query_float('pid1:limit:max')

    def set_pid1_limit_max(self, value: float) -> None:
        self._set_float('pid1:limit:max', value)

    def get_pid1_limit_min(self) -> float:
        return self._query_float('pid1:limit:min')

    def set_pid1_limit_min(self, value: float) -> None:
        self._set_float('pid1:limit:min', value)

    def get_pid1_integral_cutoff_enabled(self) -> bool:
        return self._query_bool('pid1:integral:cutoff:enable')

    def set_pid1_integral_cutoff_enabled(self, enabled: bool) -> None:
        self._set_bool('pid1:integral:cutoff:enable', enabled)

    def get_pid1_integral_cutoff_frequency(self) -> float:
        return self._query_float('pid1:integral:cutoff:frequency')

    def set_pid1_integral_cutoff_frequency(self, hz: float) -> None:
        self._set_float('pid1:integral:cutoff:frequency', hz)

    def get_pid1_window_enabled(self) -> bool:
        return self._query_bool('pid1:window:enable')

    def set_pid1_window_enabled(self, enabled: bool) -> None:
        self._set_bool('pid1:window:enable', enabled)

    def get_pid1_window_maxin(self) -> float:
        return self._query_float('pid1:window:maxin')

    def set_pid1_window_maxin(self, value: float) -> None:
        self._set_float('pid1:window:maxin', value)

    def get_pid1_window_maxout(self) -> float:
        return self._query_float('pid1:window:maxout')

    def set_pid1_window_maxout(self, value: float) -> None:
        self._set_float('pid1:window:maxout', value)

    def get_pid1_window_minin(self) -> float:
        return self._query_float('pid1:window:minin')

    def set_pid1_window_minin(self, value: float) -> None:
        self._set_float('pid1:window:minin', value)

    def get_pid1_window_minout(self) -> float:
        return self._query_float('pid1:window:minout')

    def set_pid1_window_minout(self, value: float) -> None:
        self._set_float('pid1:window:minout', value)

    def get_pid1_window_reset_enabled(self) -> bool:
        return self._query_bool('pid1:window:reset:enable')

    def set_pid1_window_reset_enabled(self, enabled: bool) -> None:
        self._set_bool('pid1:window:reset:enable', enabled)

    def get_pid1_window_reset_delay(self) -> float:
        return self._query_float('pid1:window:reset:delay')

    def set_pid1_window_reset_delay(self, seconds: float) -> None:
        self._set_float('pid1:window:reset:delay', seconds)

    # ---- PID 2 ----

    def get_pid2_proportional(self) -> float:
        return self._query_float('pid2:proportional')

    def set_pid2_proportional(self, gain: float) -> None:
        self._set_float('pid2:proportional', gain)

    def get_pid2_integral(self) -> float:
        return self._query_float('pid2:integral')

    def set_pid2_integral(self, gain: float) -> None:
        self._set_float('pid2:integral', gain)

    def get_pid2_differential(self) -> float:
        return self._query_float('pid2:differential')

    def set_pid2_differential(self, gain: float) -> None:
        self._set_float('pid2:differential', gain)

    def get_pid2_gain(self) -> float:
        return self._query_float('pid2:gain')

    def set_pid2_gain(self, gain: float) -> None:
        self._set_float('pid2:gain', gain)

    def get_pid2_lock_enabled(self) -> bool:
        return self._query_bool('pid2:lock:enable')

    def set_pid2_lock_enabled(self, enabled: bool) -> None:
        self._set_bool('pid2:lock:enable', enabled)

    def get_pid2_lock_hold(self) -> bool:
        return self._query_bool('pid2:lock:hold')

    def set_pid2_lock_hold(self, hold: bool) -> None:
        self._set_bool('pid2:lock:hold', hold)

    def get_pid2_lock_state(self) -> bool:
        """Read-only: current lock status of PID 2."""
        return self._query_bool('pid2:lock:state')

    def get_pid2_hold_state(self) -> bool:
        """Read-only: hold status of PID 2."""
        return self._query_bool('pid2:hold:state')

    def get_pid2_regulating(self) -> bool:
        """Read-only: True when PID 2 is actively regulating."""
        return self._query_bool('pid2:regulating state')

    def get_pid2_input(self) -> str:
        return self._query('pid2:input')

    def set_pid2_input(self, channel: str) -> None:
        self._set('pid2:input', channel)

    def get_pid2_output(self) -> str:
        return self._query('pid2:output')

    def set_pid2_output(self, channel: str) -> None:
        self._set('pid2:output', channel)

    def get_pid2_setpoint(self) -> float:
        return self._query_float('pid2:setpoint')

    def set_pid2_setpoint(self, value: float) -> None:
        self._set_float('pid2:setpoint', value)

    def get_pid2_sign(self) -> bool:
        return self._query_bool('pid2:sign')

    def set_pid2_sign(self, positive: bool) -> None:
        self._set_bool('pid2:sign', positive)

    def get_pid2_slope(self) -> bool:
        return self._query_bool('pid2:slope')

    def set_pid2_slope(self, positive_slope: bool) -> None:
        self._set_bool('pid2:slope', positive_slope)

    def get_pid2_relock_enabled(self) -> bool:
        return self._query_bool('pid2:relock:enable')

    def set_pid2_relock_enabled(self, enabled: bool) -> None:
        self._set_bool('pid2:relock:enable', enabled)

    def get_pid2_relock_frequency(self) -> float:
        return self._query_float('pid2:relock:frequency')

    def set_pid2_relock_frequency(self, hz: float) -> None:
        self._set_float('pid2:relock:frequency', hz)

    def get_pid2_relock_amplitude(self) -> float:
        return self._query_float('pid2:relock:amplitude')

    def set_pid2_relock_amplitude(self, volts: float) -> None:
        self._set_float('pid2:relock:amplitude', volts)

    def get_pid2_relock_output(self) -> str:
        return self._query('pid2:relock:output')

    def set_pid2_relock_output(self, channel: str) -> None:
        self._set('pid2:relock:output', channel)

    def get_pid2_limit_enabled(self) -> bool:
        return self._query_bool('pid2:limit:enable')

    def set_pid2_limit_enabled(self, enabled: bool) -> None:
        self._set_bool('pid2:limit:enable', enabled)

    def get_pid2_limit_max(self) -> float:
        return self._query_float('pid2:limit:max')

    def set_pid2_limit_max(self, value: float) -> None:
        self._set_float('pid2:limit:max', value)

    def get_pid2_limit_min(self) -> float:
        return self._query_float('pid2:limit:min')

    def set_pid2_limit_min(self, value: float) -> None:
        self._set_float('pid2:limit:min', value)

    def get_pid2_lowpass_bypass(self) -> bool:
        return self._query_bool('pid2:low pass:bypass')

    def set_pid2_lowpass_bypass(self, bypass: bool) -> None:
        self._set_bool('pid2:low pass:bypass', bypass)

    def get_pid2_lowpass_frequency(self) -> float:
        return self._query_float('pid2:low pass:frequency')

    def set_pid2_lowpass_frequency(self, hz: float) -> None:
        self._set_float('pid2:low pass:frequency', hz)

    def get_pid2_lowpass_order(self) -> int:
        return self._query_int('pid2:low pass:order')

    def set_pid2_lowpass_order(self, order: int) -> None:
        self._set_int('pid2:low pass:order', order)

    def get_pid2_window_enabled(self) -> bool:
        return self._query_bool('pid2:window:enable')

    def set_pid2_window_enabled(self, enabled: bool) -> None:
        self._set_bool('pid2:window:enable', enabled)

    def get_pid2_window_maxin(self) -> float:
        return self._query_float('pid2:window:maxin')

    def set_pid2_window_maxin(self, value: float) -> None:
        self._set_float('pid2:window:maxin', value)

    def get_pid2_window_maxout(self) -> float:
        return self._query_float('pid2:window:maxout')

    def set_pid2_window_maxout(self, value: float) -> None:
        self._set_float('pid2:window:maxout', value)

    def get_pid2_window_minin(self) -> float:
        return self._query_float('pid2:window:minin')

    def set_pid2_window_minin(self, value: float) -> None:
        self._set_float('pid2:window:minin', value)

    def get_pid2_window_minout(self) -> float:
        return self._query_float('pid2:window:minout')

    def set_pid2_window_minout(self, value: float) -> None:
        self._set_float('pid2:window:minout', value)

    def get_pid2_window_reset_enabled(self) -> bool:
        return self._query_bool('pid2:window:reset:enable')

    def set_pid2_window_reset_enabled(self, enabled: bool) -> None:
        self._set_bool('pid2:window:reset:enable', enabled)

    def get_pid2_window_reset_delay(self) -> float:
        return self._query_float('pid2:window:reset:delay')

    def set_pid2_window_reset_delay(self, seconds: float) -> None:
        self._set_float('pid2:window:reset:delay', seconds)

    # ---- Autolock ----

    def get_autolock_enabled(self) -> bool:
        return self._query_bool('autolock:enable')

    def set_autolock_enabled(self, enabled: bool) -> None:
        self._set_bool('autolock:enable', enabled)

    def get_autolock_lock_enabled(self) -> bool:
        return self._query_bool('autolock:lock:enable')

    def set_autolock_lock_enabled(self, enabled: bool) -> None:
        self._set_bool('autolock:lock:enable', enabled)

    def get_autolock_lock_hold(self) -> bool:
        return self._query_bool('autolock:lock:hold')

    def set_autolock_lock_hold(self, hold: bool) -> None:
        self._set_bool('autolock:lock:hold', hold)

    def get_autolock_lock_mode(self) -> str:
        return self._query('autolock:lock:mode')

    def set_autolock_lock_mode(self, mode) -> None:
        """Set autolock operating mode. Accepts AutolockMode enum or plain string."""
        self._set('autolock:lock:mode', mode.value if hasattr(mode, 'value') else str(mode))

    def get_autolock_lock_strategy(self) -> str:
        return self._query('autolock:lock:strategy')

    def set_autolock_lock_strategy(self, strategy) -> None:
        self._set('autolock:lock:strategy',
                  strategy.value if hasattr(strategy, 'value') else str(strategy))

    def get_autolock_setpoint(self) -> float:
        return self._query_float('autolock:setpoint')

    def set_autolock_setpoint(self, value: float) -> None:
        self._set_float('autolock:setpoint', value)

    def get_autolock_input(self) -> str:
        return self._query('autolock:input')

    def set_autolock_input(self, channel: str) -> None:
        self._set('autolock:input', channel)

    def get_autolock_cursor_index(self) -> int:
        """Cursor index (1–1000) for lock-point selection in autolock display."""
        return self._query_int('autolock:display:cursor index')

    def set_autolock_cursor_index(self, index: int) -> None:
        if not (1 <= index <= 1000):
            raise ValidationError110("Autolock cursor index must be between 1 and 1000.")
        self._set_int('autolock:display:cursor index', index)

    def get_autolock_relock_enabled(self) -> bool:
        return self._query_bool('autolock:relock:enable')

    def set_autolock_relock_enabled(self, enabled: bool) -> None:
        self._set_bool('autolock:relock:enable', enabled)

    def get_autolock_relock_frequency(self) -> float:
        return self._query_float('autolock:relock:frequency')

    def set_autolock_relock_frequency(self, hz: float) -> None:
        self._set_float('autolock:relock:frequency', hz)

    def get_autolock_relock_amplitude(self) -> float:
        return self._query_float('autolock:relock:amplitude')

    def set_autolock_relock_amplitude(self, volts: float) -> None:
        self._set_float('autolock:relock:amplitude', volts)

    def get_autolock_relock_output(self) -> str:
        return self._query('autolock:relock:output')

    def set_autolock_relock_output(self, channel: str) -> None:
        self._set('autolock:relock:output', channel)

    def get_autolock_window_enabled(self) -> bool:
        return self._query_bool('autolock:window:enable')

    def set_autolock_window_enabled(self, enabled: bool) -> None:
        self._set_bool('autolock:window:enable', enabled)

    def get_autolock_window_maxin(self) -> float:
        return self._query_float('autolock:window:maxin')

    def set_autolock_window_maxin(self, value: float) -> None:
        self._set_float('autolock:window:maxin', value)

    def get_autolock_window_maxout(self) -> float:
        return self._query_float('autolock:window:maxout')

    def set_autolock_window_maxout(self, value: float) -> None:
        self._set_float('autolock:window:maxout', value)

    def get_autolock_window_minin(self) -> float:
        return self._query_float('autolock:window:minin')

    def set_autolock_window_minin(self, value: float) -> None:
        self._set_float('autolock:window:minin', value)

    def get_autolock_window_minout(self) -> float:
        return self._query_float('autolock:window:minout')

    def set_autolock_window_minout(self, value: float) -> None:
        self._set_float('autolock:window:minout', value)

    def get_autolock_window_reset_delay(self) -> float:
        return self._query_float('autolock:window:reset:delay')

    def set_autolock_window_reset_delay(self, seconds: float) -> None:
        self._set_float('autolock:window:reset:delay', seconds)

    def get_autolock_display_ch1_mean(self) -> float:
        """Read-only: mean value of autolock display CH 1 data."""
        return self._query_float('autolock:display:ch1:mean')

    def get_autolock_display_ch1_rms(self) -> float:
        """Read-only: RMS value of autolock display CH 1 data."""
        return self._query_float('autolock:display:ch1:rms')

    def get_autolock_display_ch2_mean(self) -> float:
        """Read-only: mean value of autolock display CH 2 data."""
        return self._query_float('autolock:display:ch2:mean')

    def get_autolock_display_ch2_rms(self) -> float:
        """Read-only: RMS value of autolock display CH 2 data."""
        return self._query_float('autolock:display:ch2:rms')

    def get_autolock_display_data(self) -> str:
        """Read-only: raw 2D autolock data array string."""
        return self._query('autolock:display:graph')

    # ---- Lock-In (LI) module ----

    def get_li_modulation_enabled(self) -> bool:
        return self._query_bool('li:modulation:enable')

    def set_li_modulation_enabled(self, enabled: bool) -> None:
        self._set_bool('li:modulation:enable', enabled)

    def get_li_modulation_amplitude(self) -> float:
        return self._query_float('li:modulation:amplitude')

    def set_li_modulation_amplitude(self, volts: float) -> None:
        self._set_float('li:modulation:amplitude', volts)

    def get_li_modulation_frequency_actual(self) -> float:
        """Read-only: actual modulation frequency."""
        return self._query_float('li:modulation:frequency act')

    def get_li_modulation_frequency_set(self) -> float:
        return self._query_float('li:modulation:frequency set')

    def set_li_modulation_frequency(self, hz: float) -> None:
        self._set_float('li:modulation:frequency set', hz)

    def get_li_phase_shift(self) -> float:
        return self._query_float('li:phase shift')

    def set_li_phase_shift(self, degrees: float) -> None:
        self._set_float('li:phase shift', degrees)

    def get_li_phase_adjust(self) -> bool:
        return self._query_bool('li:phase adjust')

    def set_li_phase_adjust(self, auto: bool) -> None:
        self._set_bool('li:phase adjust', auto)

    def get_li_input(self) -> str:
        return self._query('li:input')

    def set_li_input(self, channel: str) -> None:
        self._set('li:input', channel)

    def get_li_offset(self) -> float:
        return self._query_float('li:offset')

    def set_li_offset(self, value: float) -> None:
        self._set_float('li:offset', value)

    def get_li_modulation_output(self) -> str:
        return self._query('li:modulation:output')

    def set_li_modulation_output(self, channel: str) -> None:
        self._set('li:modulation:output', channel)

    # ---- PDH module ----

    def get_pdh_modulation_enabled(self) -> bool:
        return self._query_bool('pdh:modulation:enable')

    def set_pdh_modulation_enabled(self, enabled: bool) -> None:
        self._set_bool('pdh:modulation:enable', enabled)

    def get_pdh_modulation_amplitude(self) -> float:
        return self._query_float('pdh:modulation:amplitude')

    def set_pdh_modulation_amplitude(self, volts: float) -> None:
        self._set_float('pdh:modulation:amplitude', volts)

    def get_pdh_input(self) -> str:
        return self._query('pdh:input')

    def set_pdh_input(self, channel: str) -> None:
        self._set('pdh:input', channel)

    def get_pdh_phase_shift(self) -> float:
        return self._query_float('pdh:phase shift')

    def set_pdh_phase_shift(self, degrees: float) -> None:
        self._set_float('pdh:phase shift', degrees)

    def get_pdh_phase_adjust(self) -> bool:
        return self._query_bool('pdh:phase adjust')

    def set_pdh_phase_adjust(self, auto: bool) -> None:
        self._set_bool('pdh:phase adjust', auto)

    def get_pdh_offset(self) -> float:
        return self._query_float('pdh:offset')

    def set_pdh_offset(self, value: float) -> None:
        self._set_float('pdh:offset', value)

    def get_pdh_modulation_output(self) -> str:
        return self._query('pdh:modulation:output')

    def set_pdh_modulation_output(self, channel: str) -> None:
        self._set('pdh:modulation:output', channel)

    # ---- DC Offset ----

    def get_offset_value(self) -> float:
        return self._query_float('offset:value')

    def set_offset_value(self, volts: float) -> None:
        self._set_float('offset:value', volts)

    def get_offset_output(self) -> str:
        return self._query('offset:output')

    def set_offset_output(self, channel: str) -> None:
        self._set('offset:output', channel)

    # ---- Main input ----

    def get_main_in_gain(self) -> str:
        return self._query('main in:gain')

    def set_main_in_gain(self, gain: str) -> None:
        self._set('main in:gain', gain)

    def get_main_in_invert(self) -> bool:
        return self._query_bool('main in:invert')

    def set_main_in_invert(self, invert: bool) -> None:
        self._set_bool('main in:invert', invert)

    def get_main_in_input_offset(self) -> float:
        return self._query_float('main in:input offset')

    def set_main_in_input_offset(self, value: float) -> None:
        self._set_float('main in:input offset', value)

    def get_main_in_highpass_bypass(self) -> bool:
        return self._query_bool('main in:high pass:bypass')

    def set_main_in_highpass_bypass(self, bypass: bool) -> None:
        self._set_bool('main in:high pass:bypass', bypass)

    def get_main_in_highpass_frequency(self) -> float:
        return self._query_float('main in:high pass:frequency')

    def set_main_in_highpass_frequency(self, hz: float) -> None:
        self._set_float('main in:high pass:frequency', hz)

    def get_main_in_highpass_order(self) -> int:
        return self._query_int('main in:high pass:order')

    def set_main_in_highpass_order(self, order: int) -> None:
        self._set_int('main in:high pass:order', order)

    def get_main_in_lowpass_bypass(self) -> bool:
        return self._query_bool('main in:low pass:bypass')

    def set_main_in_lowpass_bypass(self, bypass: bool) -> None:
        self._set_bool('main in:low pass:bypass', bypass)

    def get_main_in_lowpass_frequency(self) -> float:
        return self._query_float('main in:low pass:frequency')

    def set_main_in_lowpass_frequency(self, hz: float) -> None:
        self._set_float('main in:low pass:frequency', hz)

    def get_main_in_lowpass_order(self) -> int:
        return self._query_int('main in:low pass:order')

    def set_main_in_lowpass_order(self, order: int) -> None:
        self._set_int('main in:low pass:order', order)

    # ---- AUX input ----

    def get_aux_in_invert(self) -> bool:
        return self._query_bool('aux in:invert')

    def set_aux_in_invert(self, invert: bool) -> None:
        self._set_bool('aux in:invert', invert)

    def get_aux_in_lowpass_bypass(self) -> bool:
        return self._query_bool('aux in:low pass:bypass')

    def set_aux_in_lowpass_bypass(self, bypass: bool) -> None:
        self._set_bool('aux in:low pass:bypass', bypass)

    def get_aux_in_lowpass_frequency(self) -> float:
        return self._query_float('aux in:low pass:frequency')

    def set_aux_in_lowpass_frequency(self, hz: float) -> None:
        self._set_float('aux in:low pass:frequency', hz)

    def get_aux_in_lowpass_order(self) -> int:
        return self._query_int('aux in:low pass:order')

    def set_aux_in_lowpass_order(self, order: int) -> None:
        self._set_int('aux in:low pass:order', order)

    # ---- Analog controller ----

    def get_analog_lock_enabled(self) -> bool:
        return self._query_bool('analog:lock:enable')

    def set_analog_lock_enabled(self, enabled: bool) -> None:
        self._set_bool('analog:lock:enable', enabled)

    def get_analog_proportional(self) -> float:
        return self._query_float('analog:proportional')

    def set_analog_proportional(self, gain: float) -> None:
        self._set_float('analog:proportional', gain)

    def get_analog_sign(self) -> bool:
        return self._query_bool('analog:sign')

    def set_analog_sign(self, positive: bool) -> None:
        self._set_bool('analog:sign', positive)

    def get_analog_slope(self) -> bool:
        return self._query_bool('analog:slope')

    def set_analog_slope(self, positive_slope: bool) -> None:
        self._set_bool('analog:slope', positive_slope)

    # ---- DIO output ----

    def get_dio_function(self) -> str:
        return self._query('dio out:function')

    def set_dio_function(self, function: str) -> None:
        self._set('dio out:function', function)

    def get_dio_manual_state(self) -> bool:
        return self._query_bool('dio out:manual state')

    def set_dio_manual_state(self, state: bool) -> None:
        self._set_bool('dio out:manual state', state)

    # ---- Scope ----

    def get_scope_ch1_channel(self) -> str:
        return self._query('scope:ch1:channel')

    def set_scope_ch1_channel(self, channel: str) -> None:
        self._set('scope:ch1:channel', channel)

    def get_scope_ch1_mean(self) -> float:
        """Read-only: mean value of scope CH 1."""
        return self._query_float('scope:ch1:mean')

    def get_scope_ch1_rms(self) -> float:
        """Read-only: RMS value of scope CH 1."""
        return self._query_float('scope:ch1:rms')

    def get_scope_ch1_overload(self) -> bool:
        """Read-only: True if scope CH 1 is overloaded."""
        return self._query_bool('scope:ch1:overload')

    def get_scope_ch2_channel(self) -> str:
        return self._query('scope:ch2:channel')

    def set_scope_ch2_channel(self, channel: str) -> None:
        self._set('scope:ch2:channel', channel)

    def get_scope_ch2_mean(self) -> float:
        """Read-only: mean value of scope CH 2."""
        return self._query_float('scope:ch2:mean')

    def get_scope_ch2_rms(self) -> float:
        """Read-only: RMS value of scope CH 2."""
        return self._query_float('scope:ch2:rms')

    def get_scope_ch2_overload(self) -> bool:
        """Read-only: True if scope CH 2 is overloaded."""
        return self._query_bool('scope:ch2:overload')

    def get_scope_data(self) -> str:
        """Read-only: raw 2D scope data array string."""
        return self._query('scope:graph')

    def get_scope_timescale(self) -> str:
        return self._query('scope:timescale')

    def set_scope_timescale(self, span: str) -> None:
        self._set('scope:timescale', span)

    # ---- Spectrum analyzer ----

    def get_spectrum_ch1_channel(self) -> str:
        return self._query('spectrum:ch1:channel')

    def set_spectrum_ch1_channel(self, channel: str) -> None:
        self._set('spectrum:ch1:channel', channel)

    def get_spectrum_ch1_mean(self) -> float:
        """Read-only: mean value of spectrum analyzer CH 1."""
        return self._query_float('spectrum:ch1:mean')

    def get_spectrum_ch1_rms(self) -> float:
        """Read-only: RMS value of spectrum analyzer CH 1."""
        return self._query_float('spectrum:ch1:rms')

    def get_spectrum_ch1_overload(self) -> bool:
        return self._query_bool('spectrum:ch1:overload')

    def get_spectrum_ch2_channel(self) -> str:
        return self._query('spectrum:ch2:channel')

    def set_spectrum_ch2_channel(self, channel: str) -> None:
        self._set('spectrum:ch2:channel', channel)

    def get_spectrum_ch2_mean(self) -> float:
        """Read-only: mean value of spectrum analyzer CH 2."""
        return self._query_float('spectrum:ch2:mean')

    def get_spectrum_ch2_rms(self) -> float:
        """Read-only: RMS value of spectrum analyzer CH 2."""
        return self._query_float('spectrum:ch2:rms')

    def get_spectrum_ch2_overload(self) -> bool:
        return self._query_bool('spectrum:ch2:overload')

    def get_spectrum_data(self) -> str:
        """Read-only: raw 2D spectrum data array string."""
        return self._query('spectrum:graph')

    def get_spectrum_frequency_scale(self) -> str:
        return self._query('spectrum:frequency scale')

    def set_spectrum_frequency_scale(self, span: str) -> None:
        self._set('spectrum:frequency scale', span)

    # ---- Display ----

    def get_display_sampling(self) -> bool:
        return self._query_bool('display:sampling')

    def set_display_sampling(self, enabled: bool) -> None:
        self._set_bool('display:sampling', enabled)

    def get_display_update_rate(self) -> float:
        return self._query_float('display:update rate')

    def set_display_update_rate(self, rate: float) -> None:
        self._set_float('display:update rate', rate)
