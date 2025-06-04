import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 main.py \"prompt text\"")
        sys.exit(1)
    prompt = " ".join(args)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=prompt,
    )
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()