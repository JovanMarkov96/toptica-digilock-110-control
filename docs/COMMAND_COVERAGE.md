# Command Coverage Map

This document tracks DigiLock 110 RCI command coverage and implementation status.

Status values:
- **Implemented** — available in current Python API
- **Needs-verification** — path derived from the RCI manual; must be confirmed on hardware
- **Planned** — identified for future API iterations

Command paths follow the DigiLock 110 RCI Manual (Toptica, M-038, Version 05, February 2023).
Access types: **Q** = query only, **Q,S** = query and set, **S** = set only.

---

## DMS Commands (port 60000)

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `commandlist` | Q | array | Implemented | `get_commandlist` |
| `messages waiting` | Q | numeric | Implemented | `get_messages_waiting` |
| `number of modules` | Q | numeric | Implemented | `get_number_of_modules` |
| `number connected modules` | Q | numeric | Implemented | `get_number_connected_modules` |
| `modules:names` | Q | array | Implemented | `get_module_names` |
| `modules:port numbers` | Q | array | Implemented | `get_module_port_numbers` |
| `modules:serial numbers` | Q | array | Implemented | `get_module_serial_numbers` |
| `modules:connection status` | Q | array | Implemented | `get_module_connection_statuses` |
| `selected module` | Q,S | numeric | Implemented | `get_selected_module`, `set_selected_module` |
| `module:connect` | Q,S | boolean | Implemented | `get_module_connected`, `set_module_connected` |
| `module:show` | Q,S | boolean | Implemented | `get_module_show`, `set_module_show` |
| `program:ip address` | Q,S | string | Implemented | `get_ip_address` |
| `program:port number` | Q,S | numeric | Implemented | `get_port_number` |
| `program:update module list` | Q,S | boolean | Implemented | `update_module_list` |
| `access control` | S | enum | Planned | — |
| `echo` | S | boolean | Planned | — |
| `program:exit` | Q,S | boolean | Planned | — |

---

## DUI Commands (port 6000x)

### Scan Module

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `scan:enable` | Q,S | boolean | Implemented | `get_scan_enabled`, `set_scan_enabled` |
| `scan:frequency` | Q,S | numeric | Implemented | `get_scan_frequency`, `set_scan_frequency` |
| `scan:amplitude` | Q,S | numeric | Implemented | `get_scan_amplitude`, `set_scan_amplitude` |
| `scan:output` | Q,S | enum | Implemented | `get_scan_output`, `set_scan_output` |
| `scan:signal type` | Q,S | enum | Implemented | `get_scan_waveform`, `set_scan_waveform` |

### PID 1

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `pid1:proportional` | Q,S | numeric | Implemented | `get_pid1_proportional`, `set_pid1_proportional` |
| `pid1:integral` | Q,S | numeric | Implemented | `get_pid1_integral`, `set_pid1_integral` |
| `pid1:differential` | Q,S | numeric | Implemented | `get_pid1_differential`, `set_pid1_differential` |
| `pid1:gain` | Q,S | numeric | Implemented | `get_pid1_gain`, `set_pid1_gain` |
| `pid1:lock:enable` | Q,S | boolean | Implemented | `get_pid1_lock_enabled`, `set_pid1_lock_enabled` |
| `pid1:lock:hold` | Q,S | boolean | Implemented | `get_pid1_lock_hold`, `set_pid1_lock_hold` |
| `pid1:lock:state` | Q | boolean | Implemented | `get_pid1_lock_state` |
| `pid1:hold:state` | Q | boolean | Implemented | `get_pid1_hold_state` |
| `pid1:regulating state` | Q | boolean | Implemented | `get_pid1_regulating` |
| `pid1:input` | Q,S | enum | Implemented | `get_pid1_input`, `set_pid1_input` |
| `pid1:output` | Q,S | enum | Implemented | `get_pid1_output`, `set_pid1_output` |
| `pid1:setpoint` | Q,S | numeric | Implemented | `get_pid1_setpoint`, `set_pid1_setpoint` |
| `pid1:sign` | Q,S | boolean | Implemented | `get_pid1_sign`, `set_pid1_sign` |
| `pid1:slope` | Q,S | boolean | Implemented | `get_pid1_slope`, `set_pid1_slope` |
| `pid1:relock:enable` | Q,S | boolean | Implemented | `get_pid1_relock_enabled`, `set_pid1_relock_enabled` |
| `pid1:relock:frequency` | Q,S | numeric | Implemented | `get_pid1_relock_frequency`, `set_pid1_relock_frequency` |
| `pid1:relock:amplitude` | Q,S | numeric | Implemented | `get_pid1_relock_amplitude`, `set_pid1_relock_amplitude` |
| `pid1:relock:output` | Q,S | enum | Implemented | `get_pid1_relock_output`, `set_pid1_relock_output` |
| `pid1:limit enable` | Q,S | boolean | Implemented | `get_pid1_limit_enabled`, `set_pid1_limit_enabled` |
| `pid1:limit:max` | Q,S | numeric | Implemented | `get_pid1_limit_max`, `set_pid1_limit_max` |
| `pid1:limit:min` | Q,S | numeric | Implemented | `get_pid1_limit_min`, `set_pid1_limit_min` |
| `pid1:integral:cutoff:enable` | Q,S | boolean | Implemented | `get_pid1_integral_cutoff_enabled`, `set_pid1_integral_cutoff_enabled` |
| `pid1:integral:cutoff:frequency` | Q,S | numeric | Implemented | `get_pid1_integral_cutoff_frequency`, `set_pid1_integral_cutoff_frequency` |
| `pid1:window:enable` | Q,S | boolean | Implemented | `get_pid1_window_enabled`, `set_pid1_window_enabled` |
| `pid1:window:maxin` | Q,S | numeric | Implemented | `get_pid1_window_maxin`, `set_pid1_window_maxin` |
| `pid1:window:maxout` | Q,S | numeric | Implemented | `get_pid1_window_maxout`, `set_pid1_window_maxout` |
| `pid1:window:minin` | Q,S | numeric | Implemented | `get_pid1_window_minin`, `set_pid1_window_minin` |
| `pid1:window:minout` | Q,S | numeric | Implemented | `get_pid1_window_minout`, `set_pid1_window_minout` |
| `pid1:window:reset:enable` | Q,S | boolean | Implemented | `get_pid1_window_reset_enabled`, `set_pid1_window_reset_enabled` |
| `pid1:window:reset:delay` | Q,S | numeric | Implemented | `get_pid1_window_reset_delay`, `set_pid1_window_reset_delay` |
| `pid1:window:channel` | Q,S | enum | Needs-verification | — |
| `pid1:window:reset:rate` | Q,S | numeric | Planned | — |
| `pid1:turnoff reset:autolock` | Q,S | boolean | Planned | — |
| `pid1:turnoff reset:manual` | Q,S | boolean | Planned | — |

### PID 2

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `pid2:proportional` | Q,S | numeric | Implemented | `get_pid2_proportional`, `set_pid2_proportional` |
| `pid2:integral` | Q,S | numeric | Implemented | `get_pid2_integral`, `set_pid2_integral` |
| `pid2:differential` | Q,S | numeric | Implemented | `get_pid2_differential`, `set_pid2_differential` |
| `pid2:gain` | Q,S | numeric | Implemented | `get_pid2_gain`, `set_pid2_gain` |
| `pid2:lock:enable` | Q,S | boolean | Implemented | `get_pid2_lock_enabled`, `set_pid2_lock_enabled` |
| `pid2:lock:hold` | Q,S | boolean | Implemented | `get_pid2_lock_hold`, `set_pid2_lock_hold` |
| `pid2:lock:state` | Q | boolean | Implemented | `get_pid2_lock_state` |
| `pid2:hold:state` | Q | boolean | Implemented | `get_pid2_hold_state` |
| `pid2:regulating state` | Q | boolean | Implemented | `get_pid2_regulating` |
| `pid2:input` | Q,S | enum | Implemented | `get_pid2_input`, `set_pid2_input` |
| `pid2:output` | Q,S | enum | Implemented | `get_pid2_output`, `set_pid2_output` |
| `pid2:setpoint` | Q,S | numeric | Implemented | `get_pid2_setpoint`, `set_pid2_setpoint` |
| `pid2:sign` | Q,S | boolean | Implemented | `get_pid2_sign`, `set_pid2_sign` |
| `pid2:slope` | Q,S | boolean | Implemented | `get_pid2_slope`, `set_pid2_slope` |
| `pid2:relock:enable` | Q,S | boolean | Implemented | `get_pid2_relock_enabled`, `set_pid2_relock_enabled` |
| `pid2:relock:frequency` | Q,S | numeric | Implemented | `get_pid2_relock_frequency`, `set_pid2_relock_frequency` |
| `pid2:relock:amplitude` | Q,S | numeric | Implemented | `get_pid2_relock_amplitude`, `set_pid2_relock_amplitude` |
| `pid2:relock:output` | Q,S | enum | Implemented | `get_pid2_relock_output`, `set_pid2_relock_output` |
| `pid2:limit:enable` | Q,S | boolean | Implemented | `get_pid2_limit_enabled`, `set_pid2_limit_enabled` |
| `pid2:limit:max` | Q,S | numeric | Implemented | `get_pid2_limit_max`, `set_pid2_limit_max` |
| `pid2:limit:min` | Q,S | numeric | Implemented | `get_pid2_limit_min`, `set_pid2_limit_min` |
| `pid2:low pass:bypass` | Q,S | boolean | Implemented | `get_pid2_lowpass_bypass`, `set_pid2_lowpass_bypass` |
| `pid2:low pass:frequency` | Q,S | numeric | Implemented | `get_pid2_lowpass_frequency`, `set_pid2_lowpass_frequency` |
| `pid2:low pass:order` | Q,S | numeric | Implemented | `get_pid2_lowpass_order`, `set_pid2_lowpass_order` |
| `pid2:window:enable` | Q,S | boolean | Implemented | `get_pid2_window_enabled`, `set_pid2_window_enabled` |
| `pid2:window:maxin` | Q,S | numeric | Implemented | `get_pid2_window_maxin`, `set_pid2_window_maxin` |
| `pid2:window:maxout` | Q,S | numeric | Implemented | `get_pid2_window_maxout`, `set_pid2_window_maxout` |
| `pid2:window:minin` | Q,S | numeric | Implemented | `get_pid2_window_minin`, `set_pid2_window_minin` |
| `pid2:window:minout` | Q,S | numeric | Implemented | `get_pid2_window_minout`, `set_pid2_window_minout` |
| `pid2:window:reset:enable` | Q,S | boolean | Implemented | `get_pid2_window_reset_enabled`, `set_pid2_window_reset_enabled` |
| `pid2:window:reset:delay` | Q,S | numeric | Implemented | `get_pid2_window_reset_delay`, `set_pid2_window_reset_delay` |

### Autolock

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `autolock:enable` | Q,S | boolean | Implemented | `get_autolock_enabled`, `set_autolock_enabled` |
| `autolock:lock:enable` | Q,S | boolean | Implemented | `get_autolock_lock_enabled`, `set_autolock_lock_enabled` |
| `autolock:lock:hold` | Q,S | boolean | Implemented | `get_autolock_lock_hold`, `set_autolock_lock_hold` |
| `autolock:lock:mode` | Q,S | enum | Implemented | `get_autolock_lock_mode`, `set_autolock_lock_mode` |
| `autolock:lock:strategy` | Q,S | enum | Implemented | `get_autolock_lock_strategy`, `set_autolock_lock_strategy` |
| `autolock:setpoint` | Q,S | numeric | Implemented | `get_autolock_setpoint`, `set_autolock_setpoint` |
| `autolock:input` | Q,S | enum | Implemented | `get_autolock_input`, `set_autolock_input` |
| `autolock:display:cursor index` | Q,S | numeric | Implemented | `get_autolock_cursor_index`, `set_autolock_cursor_index` |
| `autolock:relock:enable` | Q,S | boolean | Implemented | `get_autolock_relock_enabled`, `set_autolock_relock_enabled` |
| `autolock:relock:frequency` | Q,S | numeric | Implemented | `get_autolock_relock_frequency`, `set_autolock_relock_frequency` |
| `autolock:relock:amplitude` | Q,S | numeric | Implemented | `get_autolock_relock_amplitude`, `set_autolock_relock_amplitude` |
| `autolock:relock:output` | Q,S | enum | Implemented | `get_autolock_relock_output`, `set_autolock_relock_output` |
| `autolock:window:enable` | Q,S | boolean | Implemented | `get_autolock_window_enabled`, `set_autolock_window_enabled` |
| `autolock:window:maxin` | Q,S | numeric | Implemented | `get_autolock_window_maxin`, `set_autolock_window_maxin` |
| `autolock:window:maxout` | Q,S | numeric | Implemented | `get_autolock_window_maxout`, `set_autolock_window_maxout` |
| `autolock:window:minin` | Q,S | numeric | Implemented | `get_autolock_window_minin`, `set_autolock_window_minin` |
| `autolock:window:minout` | Q,S | numeric | Implemented | `get_autolock_window_minout`, `set_autolock_window_minout` |
| `autolock:window:reset:delay` | Q,S | numeric | Implemented | `get_autolock_window_reset_delay`, `set_autolock_window_reset_delay` |
| `autolock:display:ch1:mean` | Q | numeric | Implemented | `get_autolock_display_ch1_mean` |
| `autolock:display:ch1:rms` | Q | numeric | Implemented | `get_autolock_display_ch1_rms` |
| `autolock:display:ch2:mean` | Q | numeric | Implemented | `get_autolock_display_ch2_mean` |
| `autolock:display:ch2:rms` | Q | numeric | Implemented | `get_autolock_display_ch2_rms` |
| `autolock:display:graph` | Q | 2D array | Implemented | `get_autolock_display_data` |
| `autolock:controller:pid1` | Q,S | boolean | Needs-verification | — |
| `autolock:controller:pid2` | Q,S | boolean | Needs-verification | — |
| `autolock:controller:analog` | Q,S | boolean | Needs-verification | — |
| `autolock:smart:engage` | Q,S | boolean | Needs-verification | — |
| `autolock:smart:setpoint` | Q,S | boolean | Needs-verification | — |

### Lock-In (LI) Module

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `li:modulation:enable` | Q,S | boolean | Implemented | `get_li_modulation_enabled`, `set_li_modulation_enabled` |
| `li:modulation:amplitude` | Q,S | numeric | Implemented | `get_li_modulation_amplitude`, `set_li_modulation_amplitude` |
| `li:modulation:frequency act` | Q | numeric | Implemented | `get_li_modulation_frequency_actual` |
| `li:modulation:frequency set` | Q,S | numeric | Implemented | `get_li_modulation_frequency_set`, `set_li_modulation_frequency` |
| `li:modulation:output` | Q,S | enum | Implemented | `get_li_modulation_output`, `set_li_modulation_output` |
| `li:phase shift` | Q,S | numeric | Implemented | `get_li_phase_shift`, `set_li_phase_shift` |
| `li:phase adjust` | Q,S | boolean | Implemented | `get_li_phase_adjust`, `set_li_phase_adjust` |
| `li:input` | Q,S | enum | Implemented | `get_li_input`, `set_li_input` |
| `li:offset` | Q,S | numeric | Implemented | `get_li_offset`, `set_li_offset` |
| `li:first filter notch` | Q,S | enum | Needs-verification | — |

### PDH Module

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `pdh:modulation:enable` | Q,S | boolean | Implemented | `get_pdh_modulation_enabled`, `set_pdh_modulation_enabled` |
| `pdh:modulation:amplitude` | Q,S | numeric | Implemented | `get_pdh_modulation_amplitude`, `set_pdh_modulation_amplitude` |
| `pdh:modulation:output` | Q,S | enum | Implemented | `get_pdh_modulation_output`, `set_pdh_modulation_output` |
| `pdh:phase shift` | Q,S | numeric | Implemented | `get_pdh_phase_shift`, `set_pdh_phase_shift` |
| `pdh:phase adjust` | Q,S | boolean | Implemented | `get_pdh_phase_adjust`, `set_pdh_phase_adjust` |
| `pdh:input` | Q,S | enum | Implemented | `get_pdh_input`, `set_pdh_input` |
| `pdh:offset` | Q,S | numeric | Implemented | `get_pdh_offset`, `set_pdh_offset` |
| `pdh:modulation:frequency set` | Q,S | enum | Needs-verification | — |

### DC Offset

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `offset:value` | Q,S | numeric | Implemented | `get_offset_value`, `set_offset_value` |
| `offset:output` | Q,S | enum | Implemented | `get_offset_output`, `set_offset_output` |

### Main Input

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `main in:gain` | Q,S | enum | Implemented | `get_main_in_gain`, `set_main_in_gain` |
| `main in:invert` | Q,S | boolean | Implemented | `get_main_in_invert`, `set_main_in_invert` |
| `main in:input offset` | Q,S | numeric | Implemented | `get_main_in_input_offset`, `set_main_in_input_offset` |
| `main in:high pass:bypass` | Q,S | boolean | Implemented | `get_main_in_highpass_bypass`, `set_main_in_highpass_bypass` |
| `main in:high pass:frequency` | Q,S | numeric | Implemented | `get_main_in_highpass_frequency`, `set_main_in_highpass_frequency` |
| `main in:high pass:order` | Q,S | numeric | Implemented | `get_main_in_highpass_order`, `set_main_in_highpass_order` |
| `main in:low pass:bypass` | Q,S | boolean | Implemented | `get_main_in_lowpass_bypass`, `set_main_in_lowpass_bypass` |
| `main in:low pass:frequency` | Q,S | numeric | Implemented | `get_main_in_lowpass_frequency`, `set_main_in_lowpass_frequency` |
| `main in:low pass:order` | Q,S | numeric | Implemented | `get_main_in_lowpass_order`, `set_main_in_lowpass_order` |

### AUX Input

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `aux in:invert` | Q,S | boolean | Implemented | `get_aux_in_invert`, `set_aux_in_invert` |
| `aux in:low pass:bypass` | Q,S | boolean | Implemented | `get_aux_in_lowpass_bypass`, `set_aux_in_lowpass_bypass` |
| `aux in:low pass:frequency` | Q,S | numeric | Implemented | `get_aux_in_lowpass_frequency`, `set_aux_in_lowpass_frequency` |
| `aux in:low pass:order` | Q,S | numeric | Implemented | `get_aux_in_lowpass_order`, `set_aux_in_lowpass_order` |

### Analog Controller

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `analog:lock:enable` | Q,S | boolean | Implemented | `get_analog_lock_enabled`, `set_analog_lock_enabled` |
| `analog:proportional` | Q,S | numeric | Implemented | `get_analog_proportional`, `set_analog_proportional` |
| `analog:sign` | Q,S | boolean | Implemented | `get_analog_sign`, `set_analog_sign` |
| `analog:slope` | Q,S | boolean | Implemented | `get_analog_slope`, `set_analog_slope` |

### DIO Output

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `dio out:function` | Q,S | enum | Implemented | `get_dio_function`, `set_dio_function` |
| `dio out:manual state` | Q,S | boolean | Implemented | `get_dio_manual_state`, `set_dio_manual_state` |

### Scope

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `scope:ch1:channel` | Q,S | enum | Implemented | `get_scope_ch1_channel`, `set_scope_ch1_channel` |
| `scope:ch1:mean` | Q | numeric | Implemented | `get_scope_ch1_mean` |
| `scope:ch1:rms` | Q | numeric | Implemented | `get_scope_ch1_rms` |
| `scope:ch1:overload` | Q | boolean | Implemented | `get_scope_ch1_overload` |
| `scope:ch2:channel` | Q,S | enum | Implemented | `get_scope_ch2_channel`, `set_scope_ch2_channel` |
| `scope:ch2:mean` | Q | numeric | Implemented | `get_scope_ch2_mean` |
| `scope:ch2:rms` | Q | numeric | Implemented | `get_scope_ch2_rms` |
| `scope:ch2:overload` | Q | boolean | Implemented | `get_scope_ch2_overload` |
| `scope:graph` | Q | 2D array | Implemented | `get_scope_data` |
| `scope:timescale` | Q,S | enum | Implemented | `get_scope_timescale`, `set_scope_timescale` |

### Spectrum Analyzer

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `spectrum:ch1:channel` | Q,S | enum | Implemented | `get_spectrum_ch1_channel`, `set_spectrum_ch1_channel` |
| `spectrum:ch1:mean` | Q | numeric | Implemented | `get_spectrum_ch1_mean` |
| `spectrum:ch1:rms` | Q | numeric | Implemented | `get_spectrum_ch1_rms` |
| `spectrum:ch1:overload` | Q | boolean | Implemented | `get_spectrum_ch1_overload` |
| `spectrum:ch2:channel` | Q,S | enum | Implemented | `get_spectrum_ch2_channel`, `set_spectrum_ch2_channel` |
| `spectrum:ch2:mean` | Q | numeric | Implemented | `get_spectrum_ch2_mean` |
| `spectrum:ch2:rms` | Q | numeric | Implemented | `get_spectrum_ch2_rms` |
| `spectrum:ch2:overload` | Q | boolean | Implemented | `get_spectrum_ch2_overload` |
| `spectrum:graph` | Q | 2D array | Implemented | `get_spectrum_data` |
| `spectrum:frequency scale` | Q,S | enum | Implemented | `get_spectrum_frequency_scale`, `set_spectrum_frequency_scale` |

### Display / System

| Command | Access | Type | Status | API method(s) |
|---------|--------|------|--------|---------------|
| `messages waiting` | Q | numeric | Implemented | `get_messages_waiting` |
| `commandlist` | Q | array | Implemented | `get_commandlist` |
| `display:sampling` | Q,S | boolean | Implemented | `get_display_sampling`, `set_display_sampling` |
| `display:update rate` | Q,S | numeric | Implemented | `get_display_update_rate`, `set_display_update_rate` |

---

## Verification Notes

- All enum parameter values (channel names, waveform types, etc.) must be confirmed
  with `.range?` queries on connected hardware, as the RCI manual does not list them.
- `scan:signal type` waveform strings: run `scan:signal type.range?` on hardware.
- `pid1:input` / `pid2:input` channel names: run `pid1:input.range?` on hardware.
- `pid1:output` / `pid2:output` channel names: run `pid1:output.range?` on hardware.
- Run `commandlist?` on a connected DUI to verify all available commands for the
  specific firmware version installed.
- The `response:` (transfer function) and `simulation:` subsystems are not yet
  implemented; they are lower priority for basic laser control use cases.
