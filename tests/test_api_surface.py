from toptica_digilock110 import (
    DigiLockDUI,
    DigiLockDMS,
    DigiLock110Error,
    ConnectionError110,
    ParameterError110,
    ValidationError110,
    ScanWaveform,
    AutolockMode,
    AutolockStrategy,
)


def test_error_hierarchy() -> None:
    assert issubclass(ConnectionError110, DigiLock110Error)
    assert issubclass(ParameterError110, DigiLock110Error)
    assert issubclass(ValidationError110, DigiLock110Error)


def test_scan_waveform_values() -> None:
    assert ScanWaveform.TRIANGLE.value == "triangle"
    assert ScanWaveform.SINE.value == "sine"
    assert ScanWaveform.SAWTOOTH.value == "sawtooth"


def test_autolock_mode_values() -> None:
    assert AutolockMode.MANUAL.value == "manual"
    assert AutolockMode.AUTOMATIC.value == "automatic"


def test_autolock_strategy_values() -> None:
    assert AutolockStrategy.SLOPE.value == "slope"
    assert AutolockStrategy.EXTREMUM.value == "extremum"


def test_requires_connection_dui_raises_before_connect() -> None:
    dui = DigiLockDUI(host='0.0.0.0', port=60001)
    try:
        dui.get_scan_enabled()
        assert False, "expected ConnectionError110"
    except ConnectionError110:
        pass


def test_requires_connection_dms_raises_before_connect() -> None:
    dms = DigiLockDMS(host='0.0.0.0', port=60000)
    try:
        dms.get_number_of_modules()
        assert False, "expected ConnectionError110"
    except ConnectionError110:
        pass


def test_dui_connect_to_unreachable_host_raises() -> None:
    dui = DigiLockDUI(host='192.0.2.1', port=60001, timeout=0.1)
    try:
        dui.connect()
        assert False, "expected ConnectionError110"
    except ConnectionError110:
        pass


def test_dms_connect_to_unreachable_host_raises() -> None:
    dms = DigiLockDMS(host='192.0.2.1', port=60000, timeout=0.1)
    try:
        dms.connect()
        assert False, "expected ConnectionError110"
    except ConnectionError110:
        pass


def test_dui_set_scan_frequency_rejects_zero() -> None:
    dui = DigiLockDUI.__new__(DigiLockDUI)
    dui._sock = object()
    try:
        dui.set_scan_frequency(0.0)
        assert False, "expected ValidationError110"
    except (ValidationError110, AttributeError):
        pass


def test_dui_set_scan_amplitude_rejects_negative() -> None:
    dui = DigiLockDUI.__new__(DigiLockDUI)
    dui._sock = object()
    try:
        dui.set_scan_amplitude(-1.0)
        assert False, "expected ValidationError110"
    except (ValidationError110, AttributeError):
        pass


def test_dui_set_autolock_cursor_index_rejects_out_of_range() -> None:
    dui = DigiLockDUI.__new__(DigiLockDUI)
    dui._sock = object()
    try:
        dui.set_autolock_cursor_index(0)
        assert False, "expected ValidationError110"
    except (ValidationError110, AttributeError):
        pass
    try:
        dui.set_autolock_cursor_index(1001)
        assert False, "expected ValidationError110"
    except (ValidationError110, AttributeError):
        pass


def test_dms_set_selected_module_rejects_negative() -> None:
    dms = DigiLockDMS.__new__(DigiLockDMS)
    dms._sock = object()
    try:
        dms.set_selected_module(-1)
        assert False, "expected ValidationError110"
    except (ValidationError110, AttributeError):
        pass


def test_dui_default_host_and_port() -> None:
    dui = DigiLockDUI()
    assert dui._host == DigiLockDUI.DEFAULT_HOST
    assert dui._port == DigiLockDUI.DEFAULT_PORT


def test_dms_default_host_and_port() -> None:
    dms = DigiLockDMS()
    assert dms._host == DigiLockDMS.DEFAULT_HOST
    assert dms._port == DigiLockDMS.DEFAULT_PORT


def test_dui_set_scan_waveform_accepts_enum() -> None:
    dui = DigiLockDUI.__new__(DigiLockDUI)
    dui._sock = None
    sent = []

    def fake_set(cmd, value):
        sent.append((cmd, value))

    dui._set = fake_set
    dui.set_scan_waveform(ScanWaveform.TRIANGLE)
    assert sent == [('scan:signal type', 'triangle')]


def test_dui_set_scan_waveform_accepts_string() -> None:
    dui = DigiLockDUI.__new__(DigiLockDUI)
    dui._sock = None
    sent = []

    def fake_set(cmd, value):
        sent.append((cmd, value))

    dui._set = fake_set
    dui.set_scan_waveform('sine')
    assert sent == [('scan:signal type', 'sine')]
