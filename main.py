import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

model_name = "gemini-2.0-flash-001"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def main():
    load_dotenv()

    isVerbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("Usage: python3 main.py \"prompt text\" [--verbose]")
        print("Example: python3 main.py \"What is the capital of France?\" --verbose")
        sys.exit(1)
    prompt = " ".join(args)
    
    if isVerbose:
        print(f"User prompt: {prompt}\n")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    generate_content(client, messages, isVerbose)

def generate_content(client, messages, isVerbose):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if isVerbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls is not None:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()