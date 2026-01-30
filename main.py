import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt

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
            system_instruction=system_prompt, temperature=0
        ),
    )
    # call the generate_content and assign to response
    if response.usage_metadata is None:
        raise RuntimeError("No metadata found in response, likely a failed API request")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
