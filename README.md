# toptica-digilock-110-control

Python control library for the **Toptica DigiLock 110** laser feedback controller
via its TCP/IP Remote Control Interface (RCI).

## Hardware overview

The DigiLock 110 runs as Windows software (DigiLock Module Server + DigiLock User
Interface) and communicates with the physical DC 110 rack over USB.  Remote control
is via plain-text TCP/IP connections:

| Endpoint | Default port | Purpose |
|----------|-------------|---------|
| DMS (DigiLock Module Server) | 60000 | Module management |
| DUI (DigiLock User Interface) | 60001, 60002, … | Laser control per module |

## Installation

```bash
pip install toptica-digilock-110-control
```

Or from source:

```bash
git clone https://github.com/JovanMarkov96/toptica-digilock-110-control.git
cd toptica-digilock-110-control
pip install -e .
```

## Quick start

```python
from toptica_digilock110 import DigiLockDUI

with DigiLockDUI('192.168.0.1', 60001) as dui:
    # Start a 10 Hz triangle scan
    dui.set_scan_frequency(10.0)
    dui.set_scan_amplitude(1.0)
    dui.set_scan_waveform('triangle')
    dui.set_scan_enabled(True)

    # Read scope
    print(dui.get_scope_ch1_mean(), dui.get_scope_ch1_rms())

    # Enable PID 1 lock
    dui.set_pid1_proportional(1000.0)
    dui.set_pid1_lock_enabled(True)
```

Discover module ports via the DMS:

```python
from toptica_digilock110 import DigiLockDMS

with DigiLockDMS('192.168.0.1') as dms:
    print(dms.get_module_names())
    print(dms.get_module_port_numbers())
```

## Protocol notes

- Commands terminate with `\r\n` (CR+LF, ASCII 13 + 10).
- Query: `cmd?\r\n` → `cmd=value\r\n> `
- Set: `cmd=value\r\n` → `> `
- Errors: `%% Error: <description>` — raised as `ParameterError110`.
- Run `commandlist?` on a connected DUI to list all available commands for
  the installed firmware version.
- Enum parameter values (channel names, waveform strings, etc.) must be
  verified with `.range?` queries on hardware; see `docs/COMMAND_COVERAGE.md`.

## Reference

- Toptica DigiLock 110 RCI Manual, M-038, Version 05, February 2023
- `docs/COMMAND_COVERAGE.md` — full parameter table and implementation status
- `docs/GUI_ROADMAP.md` — planned interactive GUI
