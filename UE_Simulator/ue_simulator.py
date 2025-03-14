import threading
import time

class UESimulator(threading.Thread):
    def __init__(self, ue_id):
        threading.Thread.__init__(self)
        self.ue_id = ue_id

    def run(self):
        print(f"UE {self.ue_id} is starting.")
        # Simulate UE behavior
        time.sleep(2)
        print(f"UE {self.ue_id} is attaching.")
        # Attach procedure
        time.sleep(2)
        print(f"UE {self.ue_id} is attached.")

def main():
    ue_count = 5
    ue_simulators = [UESimulator(ue_id) for ue_id in range(1, ue_count + 1)]

    for ue_simulator in ue_simulators:
        ue_simulator.start()

    for ue_simulator in ue_simulators:
        ue_simulator.join()

if __name__ == "__main__":
    main()