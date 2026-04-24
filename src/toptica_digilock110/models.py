from enum import Enum


class ScanWaveform(Enum):
    """Waveform shape for the scan output signal.

    The exact string values accepted by the device must be confirmed with
    ``scan:signal type.range?`` on connected hardware. Common values are
    shown here as a convenience; pass a plain string if these differ.
    """
    TRIANGLE = "triangle"
    SINE = "sine"
    SAWTOOTH = "sawtooth"


class AutolockMode(Enum):
    """Operating mode of the autolock module (``autolock:lock:mode``).

    Verify exact values with ``autolock:lock:mode.range?`` on hardware.
    """
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class AutolockStrategy(Enum):
    """Strategy used by the autolock module in full automatic mode.

    Verify exact values with ``autolock:lock:strategy.range?`` on hardware.
    """
    SLOPE = "slope"
    EXTREMUM = "extremum"
