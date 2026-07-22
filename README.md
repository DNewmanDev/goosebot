# GOOSEBOT #
This Python program is an autonomous AI coding agent built on Google's Gemini API, featuring iterative function-calling loops, tool-augmented reasoning, and self-verifying code repair.

## 🚀 Key Features
- **Autonomous Code Repair**: Diagnoses and fixes broken Python code snippets without step-by-step human guidance
- **Agentic Loop Architecture**: Iterative reasoning loop (up to 20 turns) that plans, acts, and re-evaluates until the task succeeds
- **Tool-Augmented LLM**: Gemini function-calling integration exposing file system and code execution tools to the model
- **Self-Verification**: Agent executes the code it modifies to confirm the fix actually works, rather than assuming success
- **CLI Interface**: Command-line tool with verbose mode for inspecting the agent's reasoning, token usage, and tool calls

## 🎯 Skills Demonstrated
- **LLM API Integration**: Structured use of the Gemini API, including function/tool calling and system instructions
- **Agentic System Design**: Multi-turn agent loop with state tracking across conversation history
- **Prompt Engineering**: System prompt design to constrain and guide autonomous agent behavior
- **Tool/Function Calling**: Defining callable tools the model can invoke to interact with the file system and execute code
- **Testing**: Unit test coverage for individual agent tools (file reading, file listing, file writing, code execution)
- **Error Handling**: Defensive checks around API responses, malformed function results, and missing metadata

## 🏗️ Technical Architecture

### Agent Loop Design
- **Conversation State**: Full message history maintained and passed to the model on every turn
- **Bounded Iteration**: Loop runs up to 20 turns, terminating early once the model responds without requesting a tool call
- **Function Call Detection**: Each turn inspects model output for function calls versus final text responses

### Tool System
- **Defined Tool Set**: File and code-execution tools exposed to the model as callable functions
- **Function Dispatch**: Central function-calling handler routes model tool requests to the correct implementation
- **Verbose Diagnostics**: Optional flag surfaces prompt/response token counts and raw tool outputs for debugging

### Prompting
- **System Instruction**: Dedicated system prompt module constrains agent behavior and scope
- **Zero-Temperature Inference**: Deterministic model configuration for consistent, repeatable agent behavior

## 💻 Technologies Used
- **Python 3**: Core language for agent logic and tooling
- **Google Gemini API (google-genai)**: LLM backend with function-calling support
- **python-dotenv**: Environment-based API key management
- **argparse**: Command-line interface and verbose-mode flag handling

## 🔧 Technical Highlights

### Agent Loop
```python
for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )
    # Inspect response for function calls; dispatch tool execution
    # or return final text once the agent has finished reasoning
```
### Function Dispatch
```python
function_result = call_function(part.function_call, verbose=args.verbose)
# Routes the model's requested tool call to its implementation
# and returns a structured function_response back into the conversation
```
##🚀 Getting Started

### Prerequisites
- Python 3
- A Gemini API key (set as GEMINI_API_KEY in a .env file)

### Installation & Running
```bash
# Clone the repository
git clone https://github.com/DNewmanDev/goosebot.git
cd goosebot

# Install dependencies
uv sync

# Run the agent
python3 main.py "your prompt describing the broken code" --verbose
```
## 🏗️ Project Structure

```
goosebot/
├── main.py               # Agent loop, CLI entry point
├── functions_list.py     # Tool definitions and function dispatch
├── prompts.py             # System prompt for agent behavior
├── config.py               # Configuration constants
├── calculator/            # Sample project used as an agent test target
├── test_get_file_content.py
├── test_get_files_info.py
├── test_run_python_file.py
├── test_write_file.py
├── pyproject.toml
└── uv.lock
```
