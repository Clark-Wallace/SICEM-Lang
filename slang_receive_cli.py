import argparse
import json
from pathlib import Path
from slang_receiver import SlangReceiver, ReceptionStatus
from slang_uploader import IntelligenceProfile

def main():
    parser = argparse.ArgumentParser(description='SICEM-Lang Receiver')
    parser.add_argument('transmission', type=str, help='Path to the transmission file')
    parser.add_argument('--profile', type=str, required=True, help='Path to intelligence profile file')
    parser.add_argument('--output', type=str, help='Path to save reception log')
    
    args = parser.parse_args()
    
    # Load intelligence profile
    with open(args.profile, 'r') as f:
        profile_data = json.load(f)
        profile = IntelligenceProfile(**profile_data)
    
    # Initialize receiver
    receiver = SlangReceiver(profile)
    
    try:
        # Receive and process the transmission
        status = receiver.receive_transmission(args.transmission)
        
        if status.success:
            print("\nTransmission successfully received!")
            print(f"Source: {status.details['source']}")
            print(f"Functions processed: {status.details['functions_processed']}")
            print(f"CI Level: {status.details['ci_level']}")
            
            # Save reception log if requested
            if args.output:
                receiver.save_reception_log(args.output)
                print(f"\nReception log saved to: {args.output}")
                
            # Print capability checks
            print("\nCapability Analysis:")
            for file in receiver.get_received_files():
                for func in file['processed_content']:
                    print(f"\nFunction: {func['original']['name']}")
                    for capability, has_capability in func['capability_check'].items():
                        print(f"  {capability}: {'✓' if has_capability else '✗'}")
        else:
            print(f"\nError: {status.message}")
            if status.details:
                print("Details:", json.dumps(status.details, indent=2))
            return 1
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 