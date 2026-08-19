import signal
import time
import sys

def handler(signum, frame):
    print("Graceful shutdown received. Exiting...")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, handler)

print("App started. Waiting for SIGTERM...")
while True:
    time.sleep(1)
