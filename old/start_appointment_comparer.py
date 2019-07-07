from appointment_comparer.webapp.app import start_server, stop_server
import signal
import sys


# Handler for SIGINT event
def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        stop_server()
        sys.exit(0)

# Register event
signal.signal(signal.SIGINT, signal_handler)

# start flask server
start_server()



