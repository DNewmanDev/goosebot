import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions_list import available_functions, call_function


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
    for _ in range(20):
        function_called = False
        response = client.models.generate_content(  # assign a variable to hold the generate content response
            model="gemini-2.5-flash",
            contents=messages,  # chat history list
            config=types.GenerateContentConfig(  # necessary config arg for adding tools to call and sys inst
                tools=[
                    available_functions
                ],  # available_functions comes from functions_list.py, special Tools type,
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
        # call the generate_content and assign to response
        if response.usage_metadata is None:
            raise RuntimeError(
                "No metadata found in response, likely a failed API request"
            )

        function_result_list = []
        for candidate in response.candidates:
            messages.append(candidate.content)
        for part in response.candidates[0].content.parts:
            if part.function_call is None:
                continue

            function_called = True

            function_result = call_function(part.function_call, verbose=args.verbose)
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )
            if not function_result.parts:
                raise Exception("Function call returned empty parts list")
            elif not function_result.parts[0].function_response:
                raise Exception("No Function Response object detected")
            elif not function_result.parts[0].function_response.response:
                raise Exception("No response attached to result")

            if args.verbose == True:
                print(f"-> {function_result.parts[0].function_response.response}")

            function_result_list.append(function_result.parts[0])

            messages.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            function_response=function_result.parts[0].function_response
                        )
                    ],
                )
            )
        if not function_called:
            print(response.candidates[0].content.parts[0].text)
            return


if __name__ == "__main__":
    main()
