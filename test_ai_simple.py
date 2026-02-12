"""
Simple test for the AI assistant
"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import the AI assistant
from ai_assistant import ai_assistant

# Test 1: Check if available
print("=== Test 1: Check Availability ===")
print(f"AI Available: {ai_assistant.is_available()}")
print()

# Test 2: Simple generation without history
print("=== Test 2: Simple Generation ===")
try:
    response = ai_assistant.generate_response("What is water?", conversation_history=None)
    print(f"Response: {response[:200]}...")
except Exception as e:
    print(f"Error: {e}")
print()

# Test 3: Generation with history
print("=== Test 3: With History ===")
try:
    history = [
        {"role": "user", "content": "What is water?"},
        {"role": "assistant", "content": "Water (H2O) is a chemical compound..."}
    ]
    response = ai_assistant.generate_response("What is its boiling point?", conversation_history=history)
    print(f"Response: {response[:200]}...")
except Exception as e:
    print(f"Error: {e}")
