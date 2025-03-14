import time
import threading
import logging
import os
import argparse
import socket

# Middleware
class Timers:
    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)

    @staticmethod
    def set_interval(interval, action, *args, **kwargs):
        def wrapper():
            while True:
                time.sleep(interval)
                action(*args, **kwargs)
        thread = threading.Thread(target=wrapper)
        thread.start()
        return thread

class SocketCommunication:
    @staticmethod
    def create_server(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        return s

    @staticmethod
    def accept_connection(server_socket):
        conn, addr = server_socket.accept()
        return conn, addr

    @staticmethod
    def create_client(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    @staticmethod
    def send_data(socket, data):
        socket.sendall(data.encode())

    @staticmethod
    def receive_data(socket, buffer_size=1024):
        try:
            data = socket.recv(buffer_size)
            return data.decode()
        except ConnectionResetError:
            logging.info("Connection was forcibly closed by the remote host.")
            return None

    @staticmethod
    def close_socket(socket):
        if socket:
            socket.close()

class OSFunctions:
    @staticmethod
    def get_os_info():
        return platform.system(), platform.release()

    @staticmethod
    def get_memory_usage():
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3)

    @staticmethod
    def create_directory(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def remove_directory(path):
        os.rmdir(path)

class MemoryManagement:
    @staticmethod
    def collect_garbage():
        gc.collect()

    @staticmethod
    def get_objects():
        return gc.get_objects()

# Base Simulator
class BaseSimulator(threading.Thread):
    def __init__(self, simulator_id, host, port):
        threading.Thread.__init__(self)
        self.simulator_id = simulator_id
        self.host = host
        self.port = port
        self.socket = None
        self.running = True

    def setup_logging(self, log_file):
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except FileExistsError:
                pass
        
        # Set up logging to file and console
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler(log_file),
                                logging.StreamHandler()
                            ])

    def start_server(self):
        self.socket = SocketCommunication.create_server(self.host, self.port)
        conn, addr = SocketCommunication.accept_connection(self.socket)
        return conn, addr

    def connect_to_server(self):
        self.socket = SocketCommunication.create_client(self.host, self.port)

    def run(self):
        raise NotImplementedError("Subclasses must implement this method")

    def stop(self):
        self.running = False
        SocketCommunication.close_socket(self.socket)

# DUT RAN Simulator
class DUTRANSimulator(BaseSimulator):
    def __init__(self, simulator_id, host, port, mib_parameters):
        super().__init__(simulator_id, host, port)
        self.mib_parameters = mib_parameters
        self.mib = self.create_mib()

    def create_mib(self):
        return f"MIB(systemFrameNumber={self.mib_parameters['systemFrameNumber']}, subCarrierSpacingCommon={self.mib_parameters['subCarrierSpacingCommon']}, ssb_SubcarrierOffset={self.mib_parameters['ssb_SubcarrierOffset']}, dmrs_TypeA_Position={self.mib_parameters['dmrs_TypeA_Position']}, pdcch_ConfigSIB1={self.mib_parameters['pdcch_ConfigSIB1']}, cellBarred={self.mib_parameters['cellBarred']}, intraFreqReselection={self.mib_parameters['intraFreqReselection']}, spare={self.mib_parameters['spare']})"

    def run(self):
        self.setup_logging(f'results/logs/dut_ran_simulator_{self.simulator_id}.log')
        logging.info(f"DUT RAN {self.simulator_id} starting.")
        conn, addr = self.start_server()
        with conn:
            logging.info(f"DUT RAN {self.simulator_id} connected by {addr}")
            start_time = time.time()
            while self.running and time.time() - start_time < 10:
                Timers.sleep(0.04)  # Broadcast every 40 ms
                SocketCommunication.send_data(conn, self.mib)
                logging.info(f"DUT RAN {self.simulator_id} broadcasted MIB: {self.mib}")
        self.stop()

# UE Simulator
class UESimulator(BaseSimulator):
    def run(self):
        self.setup_logging(f'results/logs/ue_simulator_{self.simulator_id}.log')
        logging.info(f"UE {self.simulator_id} starting.")
        self.connect_to_server()
        start_time = time.time()
        while self.running and time.time() - start_time < 10:
            mib_str = SocketCommunication.receive_data(self.socket)
            if mib_str:
                logging.info(f"UE {self.simulator_id} received MIB: {mib_str}")
        self.stop()

def execute_mib_call_flow():
    host = '127.0.0.1'
    port_base = 65432
    mib_parameters = {
        'systemFrameNumber': '000000',
        'subCarrierSpacingCommon': 'scs15or60',
        'ssb_SubcarrierOffset': 0,
        'dmrs_TypeA_Position': 'pos2',
        'pdcch_ConfigSIB1': 0,
        'cellBarred': 'notBarred',
        'intraFreqReselection': 'allowed',
        'spare': 0
    }
    ran_simulators = [DUTRANSimulator(sim_id, host, port_base + sim_id, mib_parameters) for sim_id in range(1, 3)]
    ue_simulators = [UESimulator(ue_id, host, port_base + (ue_id % 2) + 1) for ue_id in range(1, 6)]

    for sim in ran_simulators + ue_simulators:
        sim.start()

    Timers.sleep(10)

    for sim in ran_simulators + ue_simulators:
        sim.stop()
        sim.join()

    # Collect results
    result = "\nSimulation Results:\n"
    for sim in ran_simulators:
        result += f"DUT RAN {sim.simulator_id} broadcasted MIB: {sim.mib}\n"
    for sim in ue_simulators:
        result += f"UE {sim.simulator_id} received MIB\n"

    result += "Test execution completed."
    print(result)
    logging.info(result)
    logging.debug("Test execution completed.")
    logging.shutdown()
    return result

def main():
    parser = argparse.ArgumentParser(description='Simulate DUT RAN and UE communication.')
    parser.add_argument('--call_flow', type=str, required=True, help='The call flow to execute. Example: mib')
    args = parser.parse_args()

    logging.debug(f"Starting main with call flow: {args.call_flow}")
    if args.call_flow == 'mib':
        result = execute_mib_call_flow()
    else:
        result = f"Unknown call flow: {args.call_flow}"

    print(result)
    logging.debug(f"Finished main with result: {result}")

if __name__ == "__main__":
    # Create results directory
    if not os.path.exists('results'):
        os.makedirs('results')
    if not os.path.exists('results/logs'):
        os.makedirs('results/logs')

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("Starting run_tests.py script")
    main()
    logging.debug("Finished run_tests.py script")