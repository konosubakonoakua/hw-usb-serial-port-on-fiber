#!/usr/bin/env python3

import serial
import random
import string
import time
import argparse

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def serial_loopback_test(port, baudrate, data_length, test_cycles, delay):
    """
    Serial loopback test with configurable parameters
    """
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Starting loopback test (baudrate: {baudrate}, data length: {data_length})")

            for i in range(test_cycles):
                # Generate random ASCII string
                test_str = ''.join(random.choices(
                    string.ascii_letters + string.digits,
                    k=data_length
                ))

                # Send data
                ser.write(test_str.encode())
                print(f"<<< Sent     [{i+1}/{test_cycles}]: {test_str}")

                # Receive loopback data
                received = ser.read(data_length).decode()

                # Verify data
                if received == test_str:
                    print(f"{GREEN}>>> Received [{i+1}/{test_cycles}]: {received} (MATCHED){RESET}")
                else:
                    print(f"{RED}>>> Received [{i+1}/{test_cycles}]: {received} (MISMATCH!){RESET}")

                time.sleep(delay)

            print("Test completed")

    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Serial port loopback tester")
    parser.add_argument("--port", default="/dev/ttyUSB0", help="Serial port device")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--length", type=int, default=30, help="Data length per packet")
    parser.add_argument("--cycles", type=int, default=100, help="Number of test cycles")
    parser.add_argument("--delay", type=float, default=0, help="Delay between sends (seconds)")

    args = parser.parse_args()

    serial_loopback_test(
        port=args.port,
        baudrate=args.baud,
        data_length=args.length,
        test_cycles=args.cycles,
        delay=args.delay
    )

if __name__ == "__main__":
    main()
