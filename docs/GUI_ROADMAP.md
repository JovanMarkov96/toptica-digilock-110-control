# GUI Roadmap

This document defines the standalone GUI direction for interactive control and
testing of the Toptica DigiLock 110 via the RCI TCP/IP interface.

## Goals

- Connect to DMS (port 60000) and DUI (port 6000x) from the GUI
- Full read/write access to the key subsystems: scan, PID, autolock, LI/PDH
- Live scope and spectrum readback
- Command trace for debugging communication

## Phase 1 GUI Scope

- Connection panel: host/port entry, connect/disconnect button
- DMS panel: module list, port numbers, selected module selector
- Scan panel:
  - frequency, amplitude spinboxes + apply buttons
  - output and waveform selectors
  - enable/disable toggle
- PID 1 and PID 2 panels:
  - proportional, integral, differential, gain spinboxes
  - input/output channel selectors
  - setpoint spinbox
  - lock enable/hold toggles
  - lock state and regulating status indicators (read-only)
- Error/status panel: connection status, last error message

## Phase 2 GUI Scope

- Autolock panel:
  - enable/disable toggle
  - lock mode and strategy selectors
  - cursor index control
  - relock enable + parameters
  - window supervision controls
- Lock-In (LI) and PDH panels:
  - modulation enable, amplitude, frequency controls
  - phase shift spinbox + auto-adjust toggle
  - input and output channel selectors
- Offset panel:
  - output channel selector
  - value spinbox
- Main input / AUX input filter panels

## Phase 3 GUI Scope

- Live scope display (polling `scope:graph`, `scope:ch1:mean`, `scope:ch2:mean`)
- Live spectrum analyzer display
- Autolock display graph (polling `autolock:display:graph`)
- Command history log panel
- Session state save/load (JSON snapshot of all current parameters)

## Suggested Technical Stack

- UI toolkit: PyQt5 or PySide6
- Device backend: `toptica_digilock110.DigiLockDUI` / `DigiLockDMS`
- Non-blocking reads via a QThread polling loop
- Structured logging for parameter read/write traceability

## Safety Defaults

- Do not enable any lock (PID or autolock) immediately after connection
- Surface `ParameterError110` and `ConnectionError110` prominently
- Validate all numeric input (non-negative amplitude, positive frequency) before sending
- Allow manual scan-stop before enabling PID lock
