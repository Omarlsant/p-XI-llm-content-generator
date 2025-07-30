# test_agent.py
import os
from dotenv import load_dotenv

print("--- STARTING AGENT DIAGNOSTIC SCRIPT ---")

# 1. Load Environment Variables from the root .env file
print("Loading environment variables...")
load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")
if not tavily_key:
    print("!!! ERROR: TAVILY_API_KEY not found in your .env file. Exiting.")
    exit()
print("TAVILY_API_KEY found.")

# 2. Test the problematic import directly
try:
    print("Attempting to import 'TavilySearchResults' from 'langchain_community.tools'...")
    from langchain_community.tools.tavily_search import TavilySearchResults
    print("✅ SUCCESS: 'TavilySearchResults' imported from langchain_community.tools")
    TavilyToolClass = TavilySearchResults
except ImportError:
    print("❌ FAILED to import 'TavilySearchResults' from langchain_community.tools.")
    try:
        print("Attempting fallback import 'TavilySearch' from 'langchain_tavily'...")
        from langchain_tavily import TavilySearch as TavilySearchResults # Use an alias for compatibility
        print("✅ SUCCESS: 'TavilySearch' imported from langchain_tavily and aliased.")
        TavilyToolClass = TavilySearchResults
    except ImportError as e:
        print(f"❌ FATAL ERROR: Could not import Tavily tool from any known location.")
        print(f"   The specific error is: {e}")
        print("   Please ensure 'langchain-community' and 'langchain-tavily' are installed correctly in your venv.")
        exit()

# 3. Create and test the tool
try:
    print("Initializing the Tavily tool...")
    search_tool = TavilyToolClass(max_results=1)
    print("Tool initialized successfully.")
    
    print("Running a test search for 'What is LangChain?'...")
    results = search_tool.invoke("What is LangChain?")
    print("✅ SUCCESS: Tool invocation successful!")
    print("--- SEARCH RESULTS ---")
    print(results)
    print("----------------------")

except Exception as e:
    print(f"❌ FATAL ERROR: Failed to create or invoke the Tavily tool.")
    import traceback
    traceback.print_exc()
    exit()

print("\n--- AGENT DIAGNOSTIC COMPLETE ---")
print("Conclusion: Your local environment is correctly set up to use the Tavily search tool.")
print(f"The correct class to use in your main code is: {TavilyToolClass.__name__}")