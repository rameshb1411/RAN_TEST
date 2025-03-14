from simulators.dut_ran_simulator import DUTRANSimulator
from simulators.ue_simulator import UESimulator

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

    for sim in ran_simulators + ue_simulators:
        sim.join()
    
    # Collect results
    print("\nSimulation Results:")
    for sim in ran_simulators:
        print(f"DUT RAN {sim.simulator_id} broadcasted MIB: {sim.mib}")
    for sim in ue_simulators:
        print(f"UE {sim.simulator_id} received MIB")

def main():
    parser = argparse.ArgumentParser(description='Simulate DUT RAN and UE communication.')
    parser.add_argument('--call_flow', type=str, required=True, help='The call flow to execute. Example: mib')
    args = parser.parse_args()

    if args.call_flow == 'mib':
        execute_mib_call_flow()
    else:
        print(f"Unknown call flow: {args.call_flow}")

    print("Test execution completed.")

if __name__ == "__main__":
    main()