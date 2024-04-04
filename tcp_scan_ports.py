import threading
from queue import Queue
import socket
import time

NUM_THREADS = 50  # Number of threads for parallel scanning
TIMEOUT = 0.5  # Timeout value for connection attempts

def scan_ports(target, ports):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

def worker():
    while True:
        target, ports = queue.get()
        open_ports = scan_ports(target, ports)
        if open_ports:
            print(f"Open ports on {target}: {open_ports}")
        queue.task_done()

def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.2f} seconds")
        return result
    return wrapper

@calculate_execution_time
def main():
    global queue
    target = input("Enter the host you want to scan: ")
    ports = range(1, 65535)
    queue = Queue()

#    chunk_size = len(ports) // NUM_THREADS
    for port_range in [ports[i:i+10] for i in range(0, len(ports), 10)]:
        queue.put((target, port_range))

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    queue.join()
    print("Scan completed.")

if __name__ == "__main__":
    main()
