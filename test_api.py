import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables")
    exit(1)

print(f"API Key found: {api_key[:10]}...")

# Configure the API
genai.configure(api_key=api_key)

# List available models
print("\nListing available models:")
try:
    for m in genai.list_models():
        print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {str(e)}")

# Test with different model names
model_names = ['gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']

for model_name in model_names:
    print(f"\nTrying model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, are you working?")
        print(f"Success with {model_name}: {response.text}")
    except Exception as e:
        print(f"Error with {model_name}: {str(e)}")

print("\nTest completed.") 