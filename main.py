from call_flows.mib_call_flow import execute_mib_call_flow
import argparse

def main():
    parser = argparse.ArgumentParser(description='Simulate DUT RAN and UE communication.')
    parser.add_argument('--call_flow', type=str, required=True, help='The call flow to execute. Example: mib')
    args = parser.parse_args()

    if args.call_flow == 'mib':
        execute_mib_call_flow()
    else:
        print(f"Unknown call flow: {args.call_flow}")

if __name__ == "__main__":
    main()