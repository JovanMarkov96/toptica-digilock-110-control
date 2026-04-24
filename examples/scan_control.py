from toptica_digilock110 import DigiLockDUI, ScanWaveform


def main() -> None:
    # Replace with your instrument's IP address and DUI port
    with DigiLockDUI('192.168.0.1', 60001) as dui:
        print("Current scan state:")
        print(f"  Enabled:    {dui.get_scan_enabled()}")
        print(f"  Frequency:  {dui.get_scan_frequency():.3f} Hz")
        print(f"  Amplitude:  {dui.get_scan_amplitude():.3f} V")
        print(f"  Output:     {dui.get_scan_output()}")
        print(f"  Waveform:   {dui.get_scan_waveform()}")

        # Configure a 10 Hz triangle scan with 1 V amplitude
        dui.set_scan_waveform(ScanWaveform.TRIANGLE)
        dui.set_scan_frequency(10.0)
        dui.set_scan_amplitude(1.0)
        dui.set_scan_enabled(True)

        print("\nScan started. Press Enter to stop.")
        input()

        dui.set_scan_enabled(False)
        print("Scan stopped.")


if __name__ == "__main__":
    main()
