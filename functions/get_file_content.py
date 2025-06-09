import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))
    if not target.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target, 'r', encoding='utf-8') as file:
            content = file.read()
        if len(content) > 10000:
            content = content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'