from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.write_file import write_file

available_functions = types.Tool(  # special type from genai
    function_declarations=[  # create a list to hold valid schemas for function calls
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)
function_map = {  # dictionary to hold key:value pairs of string function names and the function calls
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info,
    "write_file": write_file,
}


def call_function(function_call, verbose=False):
    if function_call is None or not function_call.name:
        raise ValueError("call_function received empty function_call")
    if verbose:
        print(
            f"Calling function: {function_call.name}({function_call.args})"
        )  # print the name with the args
    else:
        print(f" - Calling function: {function_call.name}")
    function_name = function_call.name or ""  # safety catch for bad input
    if not function_name in function_map:
        return types.Content(  # return content type with error
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"  # set working directory to calculator

    function_result = function_map[function_name](
        **args
    )  # unpacks args and passes to the function call
    return types.Content(  # result content object with parts including the function name and response held in a dictionary of string string pairs
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
