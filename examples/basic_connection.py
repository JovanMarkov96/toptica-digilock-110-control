from toptica_digilock110 import DigiLockDMS, DigiLockDUI


def main() -> None:
    # Replace with your DMS host and DUI port
    host = '192.168.0.1'
    dms_port = 60000
    dui_port = 60001

    print("--- DigiLock Module Server ---")
    with DigiLockDMS(host, dms_port) as dms:
        n = dms.get_number_of_modules()
        print(f"Modules detected:   {n}")
        if n > 0:
            print(f"Module names:       {dms.get_module_names()}")
            print(f"DUI ports:          {dms.get_module_port_numbers()}")
            print(f"Serial numbers:     {dms.get_module_serial_numbers()}")

    print()
    print("--- DigiLock User Interface (module 1) ---")
    with DigiLockDUI(host, dui_port) as dui:
        print(f"Scan enabled:       {dui.get_scan_enabled()}")
        print(f"Scan frequency:     {dui.get_scan_frequency():.3f} Hz")
        print(f"Scan amplitude:     {dui.get_scan_amplitude():.3f} V")
        print(f"Scan output:        {dui.get_scan_output()}")
        print()
        print(f"PID1 proportional:  {dui.get_pid1_proportional()}")
        print(f"PID1 integral:      {dui.get_pid1_integral()}")
        print(f"PID1 locked:        {dui.get_pid1_lock_state()}")
        print(f"PID1 regulating:    {dui.get_pid1_regulating()}")
        print()
        print(f"Autolock enabled:   {dui.get_autolock_enabled()}")
        print(f"Autolock locked:    {dui.get_autolock_lock_enabled()}")
        print()
        print(f"Offset output:      {dui.get_offset_output()}")
        print(f"Offset value:       {dui.get_offset_value():.4f} V")


if __name__ == "__main__":
    main()
