"""neomon — tiny synthetic vitals feed for the masterclass.

Prints fake neonatal vitals to the terminal once per second.

Run:  python monitor.py
Stop: Ctrl+C
"""

import random
import time

# ---------------------------------------------------------------
# configuration
# ---------------------------------------------------------------
CONFIG = {
    "patient_id": "SIM-0001",
    "interval_s": 1.0,
    "hr_range": (110, 170),      # bpm, synthetic
    "rr_range": (35, 65),        # breaths/min, synthetic
    "hr_alarm_bpm": 170,
    "spo2_range": (88, 100),     # %, synthetic
}


def generate_reading():
    """Produce one synthetic reading."""
    hr = random.randint(*CONFIG["hr_range"])
    rr = random.randint(*CONFIG["rr_range"])
    spo2 = random.randint(*CONFIG["spo2_range"])
    return {"hr": hr, "rr": rr, "spo2": spo2}


def check_alarm(reading, prev_reading):
    if prev_reading is None:
        return False

    threshold = CONFIG["hr_alarm_bpm"]
    if reading["hr"] > threshold and prev_reading["hr"] > threshold:
        return True
    return False


def format_reading(reading, tick, prev_reading):
    """Render one reading as a single output line."""
    alarm = "!!" if check_alarm(reading,prev_reading) else " "
    line = "%s  #%04d  HR %3d  RR %2d SpO2 %3d%%" % (
        alarm,
        tick,
        reading["hr"],
        reading["rr"],
        reading["spo2"],
    )
    return line


def main():
    print("neomon 0.1  |  patient %s  |  synthetic feed (HR/RR/SpO2)" % CONFIG["patient_id"])
    print("alarm > %d bpm" % CONFIG["hr_alarm_bpm"])
    print("-" * 44)
    tick = 0
    prev_reading = None
    while True:
        tick += 1
        reading = generate_reading()
        print(format_reading(reading, tick, prev_reading))
        prev_reading = reading
        time.sleep(CONFIG["interval_s"])


if __name__ == "__main__":
    main()
