from slang_assistant import SlangAssistant
from dotenv import load_dotenv
import os
import json

def test_api_connection():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("(E)rror: No API key found in .env file 😅")
        return
        
    print("(T)esting API connection...")
    
    try:
        # Initialize assistant
        assistant = SlangAssistant(user_ci_level=0.7)
        
        # Test with a simple .slang file
        test_slang = {
            "system": "TestSystem",
            "version": "1.0",
            "description": "A test system for API verification",
            "context": {
                "user_ci_score": 0.7,
                "capabilities": ["test", "verify"],
                "preferences": {"style": "friendly"}
            },
            "functions": [
                {
                    "name": "test_connection",
                    "agent": "TestAgent",
                    "intent": "Test the API connection",
                    "context": {"complexity": "low"},
                    "input": "test",
                    "output": "response"
                }
            ]
        }
        
        # Save test file
        with open("test.slang", "w") as f:
            json.dump(test_slang, f, indent=2)
            
        # Load and test
        response = assistant.save_draft("test.slang")
        print(response)
        
        # Test a simple query
        test_response = assistant.process_user_input("(T)est connection")
        print("\n(T)est response:")
        print(test_response)
        
        print("\n(A)PI connection successful! 🎉")
        
    except Exception as e:
        print(f"(E)rror during API test: {str(e)} 😅")
        
    finally:
        # Clean up
        if os.path.exists("test.slang"):
            os.remove("test.slang")

if __name__ == "__main__":
    test_api_connection() 