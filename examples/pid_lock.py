"""Demonstrates PID controller setup, locking, and status readback."""

import time
from toptica_digilock110 import DigiLockDUI


def main() -> None:
    # Replace with your instrument's IP address and DUI port
    with DigiLockDUI('192.168.0.1', 60001) as dui:
        # --- Configure PID 1 ---
        dui.set_pid1_proportional(1000.0)
        dui.set_pid1_integral(100.0)
        dui.set_pid1_differential(0.0)
        dui.set_pid1_gain(1.0)
        dui.set_pid1_sign(True)   # positive sign
        dui.set_pid1_slope(True)  # lock to positive slope
        dui.set_pid1_setpoint(0.0)

        print("PID 1 configured:")
        print(f"  Proportional: {dui.get_pid1_proportional()}")
        print(f"  Integral:     {dui.get_pid1_integral()}")
        print(f"  Differential: {dui.get_pid1_differential()}")
        print(f"  Gain:         {dui.get_pid1_gain()}")
        print(f"  Setpoint:     {dui.get_pid1_setpoint()}")

        # --- Enable lock ---
        dui.set_pid1_lock_enabled(True)
        print("\nPID 1 lock enabled. Waiting 2 s...")
        time.sleep(2.0)

        print(f"  Lock state:   {dui.get_pid1_lock_state()}")
        print(f"  Regulating:   {dui.get_pid1_regulating()}")

        print("\nScope readback:")
        print(f"  CH1 mean:     {dui.get_scope_ch1_mean():.5f} V")
        print(f"  CH1 RMS:      {dui.get_scope_ch1_rms():.5f} V")

        print("\nPress Enter to release lock.")
        input()

        dui.set_pid1_lock_enabled(False)
        print("PID 1 unlocked.")


if __name__ == "__main__":
    main()
