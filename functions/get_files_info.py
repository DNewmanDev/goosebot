import os
import types
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        print("get files is running")
        working_dir_abs = os.path.abspath(
            working_directory
        )  # grab absolute path of working dir

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}", unauthorized access'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        print("building response")
        response = []
        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)

            response.append(
                f" - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}"
            )
        print(f'returning: {"\n".join(response)}')
        return "\n".join(response)
    except Exception as e:
        return f"ERROR: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
