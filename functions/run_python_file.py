import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target):
        return f'Error: File "{file_path}" not found.'
    
    if not target.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ['python', target],
            capture_output=True,
            text=True,
            timeout=30 
        )
        output = ''
        if result.stdout:
            output += f'STDOUT:\n{result.stdout.strip()}\n'
        if result.stderr:
            output += f'STDERR:\n{result.stderr.strip()}\n'
        if result.returncode != 0:
            output += f'Process exited with status {result.returncode}.\n'
        if not result.stdout and not result.stderr:
            output += 'No output produced.'
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"