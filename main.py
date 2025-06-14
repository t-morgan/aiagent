import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

model_name = "gemini-2.0-flash-001"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read, relative to the working directory. Required.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read, relative to the working directory. File path must end in .py. Required.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file, constrained to the working directory. Overwrites the file if it already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write, relative to the working directory. Required.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file being written. Required.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_registry = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


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
    max_iterations = 20
    for i in range(max_iterations):
        if isVerbose:
            print(f"\nIteration {i + 1}:\n")

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

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(
                    function_call_part, verbose=isVerbose
                )
                messages.append(function_call_result)
            continue
        else:
            print(f"\nFinal response:\n{response.text}")
            break
    else:
        print(f"\nReached maximum iterations ({max_iterations}). Exiting.")

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args
    working_directory = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")
    
    func = function_registry.get(function_name)
    if func:
        function_result = func(working_directory, **args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


if __name__ == "__main__":
    main()