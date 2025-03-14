import time
from simulators.base_simulator import BaseSimulator

class RANSimulator(BaseSimulator):
    def __init__(self, simulator_id, host, port):
        super().__init__(simulator_id, host, port)
        self.mib = "MIB(systemFrameNumber=000000, subCarrierSpacingCommon=scs15or60, ssb_SubcarrierOffset=0, dmrs_TypeA_Position=pos2, pdcch_ConfigSIB1=0, cellBarred=notBarred, intraFreqReselection=allowed, spare=0)"

    def run(self):
        self.setup_logging(f'logs/ran_simulator_{self.simulator_id}.log')
        logging.info(f"RAN {self.simulator_id} starting.")
        print(f"RAN {self.simulator_id} starting.")
        conn, addr = self.start_server()
        with conn:
            logging.info(f"RAN {self.simulator_id} connected by {addr}")
            print(f"RAN {self.simulator_id} connected by {addr}")
            start_time = time.time()
            while time.time() - start_time < 10:
                timers.sleep(0.04)  # Broadcast every 40 ms
                socket_communication.send_data(conn, self.mib)
                logging.info(f"RAN {self.simulator_id} broadcasted MIB: {self.mib}")
                print(f"RAN {self.simulator_id} broadcasted MIB: {self.mib}")