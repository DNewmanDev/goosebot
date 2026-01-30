import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        returned_process = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        output = []
        if not returned_process.returncode == 0:
            output.append(f"Process exited with code {returned_process.returncode} ")
        if not returned_process.stderr and not returned_process.stdout:
            output.append(f"No output produced")
        if returned_process.stdout:
            output.append(f"STDOUT: {returned_process.stdout}")
        if returned_process.stderr:
            output.append(f"STDERR: {returned_process.stderr}")

        return "\n".join(output)

    except Exception as e:
        print("Error: {e}")
