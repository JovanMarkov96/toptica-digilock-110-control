class DigiLock110Error(Exception):
    """Base class for all DigiLock 110 library errors."""


class ConnectionError110(DigiLock110Error):
    """Raised when the TCP connection to DMS or DUI cannot be established or is lost."""


class ParameterError110(DigiLock110Error):
    """Raised when the device returns an error response ('%% Error: ...') to a command."""


class ValidationError110(DigiLock110Error):
    """Raised when caller input is outside the accepted range or format."""
