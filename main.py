import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions_list import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI API KEY not found, check .Env file")


def main():
    parser = argparse.ArgumentParser(
        description="ChatbotForGeese"
    )  # creates parser object
    parser.add_argument(
        "user_prompt", type=str, help="User prompt"
    )  # creates command line argument from user input
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Toggle verbose output"
    )  # adds command line toggle for verbose output
    args = (
        parser.parse_args()
    )  # creates argparse.Namespace to store extracted data from the parser object containing positional argument user prompt and verbose flag
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]  # list container to hold the messages
    client = genai.Client(api_key=api_key)  # init client
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )
    # call the generate_content and assign to response
    if response.usage_metadata is None:
        raise RuntimeError("No metadata found in response, likely a failed API request")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    call_check = response.candidates[0].content.parts[0]
    if hasattr(call_check, "function_call"):
        function_responses = []
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call"):
                fc = part.function_call
                print(f"Calling function: {fc.name}({fc.args})")

                if fc.name == "get_file_content":
                    from functions.get_file_content import get_file_content

                    result = get_file_content("calculator", fc.args["file_path"])
                    print(result)
                elif fc.name == "get_files_info":
                    from functions.get_files_info import get_files_info

                    result = get_files_info("calculator", fc.args["directory"])
                    print(result)
                elif fc.name == "write_file":
                    from functions.write_file import write_file

                    result = write_file(
                        "calculator", fc.args["file_path"], fc.args["content"]
                    )
                    print(result)

                elif fc.name == "run_python_file":
                    from functions.run_python_file import run_python_file

                    args_list = fc.args.get("args", None)
                    result = run_python_file(
                        "calculator", fc.args["file_path"], args_list
                    )
                    print(result)
                else:
                    result = f"Error: Unknown function {fc.name}"


if __name__ == "__main__":
    main()
