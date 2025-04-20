import argparse
import json
from pathlib import Path
from slang_uploader import SlangUploader, IntelligenceProfile

def main():
    parser = argparse.ArgumentParser(description='SICEM-Lang Uploader')
    parser.add_argument('file', type=str, help='Path to the .slang file')
    parser.add_argument('--source', type=str, required=True, help='Source intelligence name')
    parser.add_argument('--target', type=str, required=True, help='Target intelligence name')
    parser.add_argument('--output', type=str, help='Output path for the adapted .slang file')
    parser.add_argument('--config', type=str, help='Path to intelligence configuration file')
    
    args = parser.parse_args()
    
    # Initialize uploader
    uploader = SlangUploader()
    
    # Load or create intelligence profiles
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
            for profile in config['intelligences']:
                uploader.register_intelligence(IntelligenceProfile(**profile))
    else:
        # Default profiles for testing
        uploader.register_intelligence(IntelligenceProfile(
            name="gpt4",
            ci_level=0.9,
            capabilities=["natural_language", "code_generation", "context_understanding"],
            preferences={"style": "technical", "detail_level": "high"}
        ))
        uploader.register_intelligence(IntelligenceProfile(
            name="basic_ai",
            ci_level=0.4,
            capabilities=["basic_commands", "simple_patterns"],
            preferences={"style": "simple", "detail_level": "low"}
        ))
    
    try:
        # Upload and transmit the .slang file
        transmission = uploader.upload_slang(args.file, args.source, args.target)
        
        # Generate adapted .slang content
        adapted_content = uploader.generate_target_slang(transmission)
        
        # Save the adapted content
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(adapted_content)
            print(f"Adapted .slang file saved to: {output_path}")
        else:
            print("\nAdapted .slang content:")
            print(adapted_content)
            
        # Save transmission log
        log_path = Path(args.file).with_suffix('.transmission.json')
        uploader.save_transmission(transmission, str(log_path))
        print(f"\nTransmission log saved to: {log_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 