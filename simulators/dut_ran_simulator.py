import time
import argparse
import logging
from simulators.base_simulator import BaseSimulator
from middleware import timers, socket_communication

class DUTRANSimulator(BaseSimulator):
    def __init__(self, simulator_id, host, port, mib_parameters):
        super().__init__(simulator_id, host, port)
        self.mib_parameters = mib_parameters
        self.mib = self.create_mib()

    def create_mib(self):
        return f"MIB(systemFrameNumber={self.mib_parameters['systemFrameNumber']}, subCarrierSpacingCommon={self.mib_parameters['subCarrierSpacingCommon']}, ssb_SubcarrierOffset={self.mib_parameters['ssb_SubcarrierOffset']}, dmrs_TypeA_Position={self.mib_parameters['dmrs_TypeA_Position']}, pdcch_ConfigSIB1={self.mib_parameters['pdcch_ConfigSIB1']}, cellBarred={self.mib_parameters['cellBarred']}, intraFreqReselection={self.mib_parameters['intraFreqReselection']}, spare={self.mib_parameters['spare']})"

    def run(self):
        self.setup_logging(f'logs/dut_ran_simulator_{self.simulator_id}.log')
        logging.info(f"DUT RAN {self.simulator_id} starting.")
        print(f"DUT RAN {self.simulator_id} starting.")
        conn, addr = self.start_server()
        with conn:
            logging.info(f"DUT RAN {self.simulator_id} connected by {addr}")
            print(f"DUT RAN {self.simulator_id} connected by {addr}")
            start_time = time.time()
            while time.time() - start_time < 10:
                timers.sleep(0.04)  # Broadcast every 40 ms
                socket_communication.send_data(conn, self.mib)
                logging.info(f"DUT RAN {self.simulator_id} broadcasted MIB: {self.mib}")
                print(f"DUT RAN {self.simulator_id} broadcasted MIB: {self.mib}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DUT RAN Simulator')
    parser.add_argument('--simulator_id', type=int, required=True, help='Simulator ID')
    parser.add_argument('--host', type=str, required=True, help='Host address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--systemFrameNumber', type=str, required=True, help='System Frame Number')
    parser.add_argument('--subCarrierSpacingCommon', type=str, required=True, help='Sub Carrier Spacing Common')
    parser.add_argument('--ssb_SubcarrierOffset', type=int, required=True, help='SSB Subcarrier Offset')
    parser.add_argument('--dmrs_TypeA_Position', type=str, required=True, help='DMRS Type A Position')
    parser.add_argument('--pdcch_ConfigSIB1', type=int, required=True, help='PDCCH Config SIB1')
    parser.add_argument('--cellBarred', type=str, required=True, help='Cell Barred')
    parser.add_argument('--intraFreqReselection', type=str, required=True, help='Intra Freq Reselection')
    parser.add_argument('--spare', type=int, required=True, help='Spare')
    args = parser.parse_args()

    mib_parameters = {
        'systemFrameNumber': args.systemFrameNumber,
        'subCarrierSpacingCommon': args.subCarrierSpacingCommon,
        'ssb_SubcarrierOffset': args.ssb_SubcarrierOffset,
        'dmrs_TypeA_Position': args.dmrs_TypeA_Position,
        'pdcch_ConfigSIB1': args.pdcch_ConfigSIB1,
        'cellBarred': args.cellBarred,
        'intraFreqReselection': args.intraFreqReselection,
        'spare': args.spare
    }

    simulator = DUTRANSimulator(args.simulator_id, args.host, args.port, mib_parameters)
    simulator.start()
    simulator.join()