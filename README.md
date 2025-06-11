# 🤖 Gemini-Powered AI Coding Agent
This is a command-line AI agent powered by Google's Gemini API. It can autonomously explore, read, execute, and modify code in a secure working directory based on natural language prompts.

Inspired by the excellent [Boot.dev course on building an AI agent in Python](https://www.boot.dev/courses/build-ai-agent-python), this project serves as a fully working example of LLM tool use via function calling.

---

## 🧠 Features

- 🗂️ List files in a sandboxed directory
- 📖 Read file content (up to 10,000 characters)
- 🐍 Run Python scripts and capture output
- ✍️ Create or modify files
- 🔁 Loop up to 20 iterations until the task is complete

All operations are confined to a secure workspace (e.g., ./calculator).

---

## 🧪 Demo

```bash
python3 main.py "List the files, create hello.py that prints Hello World, and run it." --verbose
```

----

## 📁 Project Structure

```bash
.
├── main.py                    # Main agent loop with Gemini API calls
├── functions/
│   ├── get_files_info.py      # Tool: list files
│   ├── get_file_content.py    # Tool: read file
│   ├── run_python_file.py     # Tool: run script
│   └── write_file.py          # Tool: write file
├── calculator/                # Safe sandbox for file operations
├── .env                       # API key stored here
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

1. Clone this repo

```bash
git clone https://github.com/t-morgan/ai-agent.git
cd ai-agent
```

2. Create .env file

```ini
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 How It Works

1. Takes a user prompt from the command line
2. Sends it to Gemini along with available tool schemas
3. Executes tool calls when requested by the model
4. Feeds results back into the conversation
5. Repeats until Gemini responds with a final answer

The loop runs up to 20 times or until the model stops requesting tools.

---

## 🛠 Supported Tools

| Tool Name          | Description                                                                          |
|--------------------|--------------------------------------------------------------------------------------|
| `get_files_info`   | Lists files and their sizes in a specified directory within the working directory.   |
| `get_file_content` | Reads and returns up to 10,000 characters from a file.                               |
| `run_python_file`  | Executes a `.py` script using `subprocess` and returns STDOUT/STDERR.                |
| `write_file`       | Writes or overwrites a file with the provided content.                               |

All tools enforce path restrictions to ensure they only operate within the working directory (e.g., `./calculator`).

---

## 📦 Example Usage

```bash
# Create and execute a Python script
python3 main.py "Create hello.py that prints 'Hello, AI!' and run it." --verbose
```

```bash
# List files and show content
python3 main.py "What files exist and what's in main.py?"
```

---

## 🔒 Security Measures

* ✅ All file operations are sandboxed to ./calculator
* ✅ File reads are capped at 10,000 characters
* ✅ Scripts are run with subprocess + timeout
* ✅ Absolute paths are resolved and validated

---

## 📚 Credits
This project is based on and expands ideas from the Boot.dev course: Build an AI Agent in Python. Highly recommended for understanding LLM function calling from scratch.

---
## 📜 License
MIT License