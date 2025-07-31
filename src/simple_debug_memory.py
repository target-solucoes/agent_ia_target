"""
Simple debug script for memory functionality
"""
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.append("src")
sys.path.append(".")

from duckdb_agent import create_agent
from dotenv import load_dotenv

load_dotenv()

def test_memory():
    print("Simple Memory Test")
    print("=" * 40)
    
    # Create agent with session ID
    session_id = "test_session_001" 
    print(f"Creating agent with session: {session_id}")
    
    try:
        agent, df = create_agent(session_user_id=session_id)
        print("Agent created successfully!")
    except Exception as e:
        print(f"Error creating agent: {e}")
        return False
    
    # Test 1: Say name
    print("\nTEST 1: Setting name")
    try:
        query1 = "meu nome eh Pedro"
        print(f"User: {query1}")
        response1 = agent.run(query1)
        print(f"Agent response received: {len(response1.content)} characters")
        # Clean response for display
        clean_response = response1.content.encode('ascii', errors='ignore').decode('ascii')
        print(f"Response preview: {clean_response[:100]}...")
    except Exception as e:
        print(f"Error in test 1: {e}")
        return False
    
    # Test 2: Ask for name
    print("\nTEST 2: Asking for name")
    try:
        query2 = "qual eh meu nome?"
        print(f"User: {query2}")
        response2 = agent.run(query2)
        print(f"Agent response received: {len(response2.content)} characters")
        # Clean response for display
        clean_response2 = response2.content.encode('ascii', errors='ignore').decode('ascii')
        print(f"Response preview: {clean_response2[:100]}...")
        
        # Check if Pedro is mentioned
        pedro_mentioned = "pedro" in response2.content.lower()
        print(f"Pedro mentioned: {pedro_mentioned}")
        
        return pedro_mentioned
        
    except Exception as e:
        print(f"Error in test 2: {e}")
        return False

if __name__ == "__main__":
    success = test_memory()
    print(f"\nMemory test result: {'PASSED' if success else 'FAILED'}")