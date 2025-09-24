#!/usr/bin/env python3
"""
synthetic_logs.py
Append syslog-style entries to ./synthetic_logs.log (one line per second).
"""

import time
import random
import socket
import os
from datetime import datetime

LOG_FILE = "synthetic_logs.log"
HOSTNAME = socket.gethostname()    # e.g. 'Kunals-MacBook-Air'
PROCESS = "syslogd"

MESSAGES = [
    "Alert - password change",
    "Failed login attempt",
    "Successfull login",
    "Successfull login",
    "User login successful",
    "File uploaded",
    "File download error",
    "Connection timeout",
    "System rebooted"
]

def make_timestamp(dt=None):
    dt = dt or datetime.now()
    # produce "Sep 22 04:35:00" with a space-padded day (syslog-style)
    return f"{dt.strftime('%b')} {dt.day:2d} {dt.strftime('%H:%M:%S')}"

def generate_entry():
    ts = make_timestamp()
    pid = random.randint(100, 999)
    msg = random.choice(MESSAGES)
    return f"{ts} {HOSTNAME} {PROCESS}[{pid}]: {msg}\n"

if __name__ == "__main__":
    try:
        while True:
            entry = generate_entry()
            # Append to file and flush to ensure Logstash sees it quickly
            with open(LOG_FILE, "a") as f:
                f.write(entry)
                f.flush()
                try:
                    os.fsync(f.fileno())
                except OSError:
                    # fsync might fail on some filesystems/containers; ignore safely
                    pass
            # also print to stdout (optional)
            print(entry, end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped by user")