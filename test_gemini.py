"""
Test script to verify Gemini API connection
"""
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test if Gemini API is properly configured and working."""
    
    # Check if API key exists
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with your API key")
        return False
    
    print("✓ GEMINI_API_KEY found")
    print(f"  Key starts with: {api_key[:10]}...")
    
    # Try to configure and connect
    try:
        client = genai.Client(api_key=api_key)
        print("✓ Gemini API configured")
        
        # List available models
        print("\nListing available models...")
        try:
            models = client.models.list()
            print("Available models:")
            for model in models:
                if hasattr(model, 'name'):
                    print(f"  - {model.name}")
        except Exception as e:
            print(f"Could not list models: {e}")
        
        # Test a simple query with gemini-2.5-flash
        print("\nTesting API with a simple query (gemini-2.5-flash)...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Say "Hello! Connection successful!" if you can read this.'
        )
        
        print("✓ Successfully received response from Gemini!")
        print(f"\nResponse: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error connecting to Gemini: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Gemini API Connection")
    print("=" * 50)
    
    success = test_gemini_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Gemini connection test PASSED")
    else:
        print("❌ Gemini connection test FAILED")
    print("=" * 50)
