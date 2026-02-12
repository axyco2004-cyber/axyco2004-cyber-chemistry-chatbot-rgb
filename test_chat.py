"""
Test script to check if the chat endpoint is working
"""
import requests
import json

# Test the chat endpoint
url = "http://localhost:5000/chat"

# Test 1: Simple question
print("Test 1: Simple question")
response1 = requests.post(url, json={
    "message": "What is water?",
    "history": []
})
print(f"Status: {response1.status_code}")
print(f"Response: {response1.json()}\n")

# Test 2: Follow-up question with history
print("Test 2: Follow-up with history")
history = [
    {"role": "user", "content": "What is water?"},
    {"role": "assistant", "content": response1.json().get("response", "")}
]
response2 = requests.post(url, json={
    "message": "What is its boiling point?",
    "history": history
})
print(f"Status: {response2.status_code}")
print(f"Response: {response2.json()}\n")

# Test 3: Different question
print("Test 3: Different question")
response3 = requests.post(url, json={
    "message": "What is hydrogen?",
    "history": []
})
print(f"Status: {response3.status_code}")
print(f"Response: {response3.json()}\n")
