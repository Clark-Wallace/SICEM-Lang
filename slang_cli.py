import argparse
from pathlib import Path
from slang_parser import SlangParser
from slang_interpreter import SlangInterpreter

def get_simplified_help():
    return """
    How to use this program:
    1. Choose a .slang file (--file)
    2. Pick what you want to do (--function)
    3. Type what you want to say (--input)
    4. (Optional) Set how smart you want the program to be (--ci)
    """

def main():
    parser = argparse.ArgumentParser(
        description='A simple program to understand .slang files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_simplified_help()
    )
    
    parser.add_argument('--file', required=True, help='The .slang file to use')
    parser.add_argument('--function', required=True, help='What you want to do (process_text or analyze_context)')
    parser.add_argument('--input', required=True, help='What you want to say')
    parser.add_argument('--ci', type=float, default=0.5, help='How smart the program should be (0.0-1.0)')
    parser.add_argument('--verbose', action='store_true', help='Show more details')
    parser.add_argument('--help-simple', action='store_true', help='Show simple help')
    
    args = parser.parse_args()
    
    if args.help_simple:
        print(get_simplified_help())
        return
    
    try:
        # Read and parse the .slang file
        with open(args.file, 'r') as f:
            content = f.read()
        
        parser = SlangParser()
        parsed_content = parser.parse(content)
        
        # Initialize interpreter with CI level
        interpreter = SlangInterpreter(ci_level=args.ci)
        
        # Execute the specified function
        result = interpreter.execute_function(parsed_content['functions'][args.function], args.input)
        
        if args.verbose:
            print(f"\nWhat I did:")
            print(f"- Used function: {args.function}")
            print(f"- Your input: {args.input}")
            print(f"- Smartness level: {args.ci}")
            print(f"\nResult:")
            print(result)
            print("\nHelp:")
            print(interpreter.get_help())
        else:
            print(result)
            
    except Exception as e:
        if args.ci < 0.3:
            print("Sorry, something went wrong. Please try again with simpler words.")
        else:
            print(f"Error: {str(e)}")
            print("\nTry using --help-simple for easier instructions.")

if __name__ == "__main__":
    main() 