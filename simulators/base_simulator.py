import threading
import logging
import os
from middleware import timers, socket_communication, os_functions, memory_management

class BaseSimulator(threading.Thread):
    def __init__(self, simulator_id, host, port):
        threading.Thread.__init__(self)
        self.simulator_id = simulator_id
        self.host = host
        self.port = port
        self.socket = None

    def setup_logging(self, log_file):
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except FileExistsError:
                pass
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    def start_server(self):
        self.socket = socket_communication.create_server(self.host, self.port)
        conn, addr = socket_communication.accept_connection(self.socket)
        return conn, addr

    def connect_to_server(self):
        self.socket = socket_communication.create_client(self.host, self.port)

    def run(self):
        raise NotImplementedError("Subclasses must implement this method")