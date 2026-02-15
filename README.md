![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.2.0-orange)
![Build Status](https://github.com/yenksid/nexus_cli/actions/workflows/ci.yml/badge.svg)
![Format](https://img.shields.io/badge/format-Markdown-blue)

# Nexus CLI 🌌
**Version: 0.2.0**

A powerful, unified Command Line Interface (CLI) suite designed for AI-driven development, project scaffolding, and context generation. 

Nexus CLI provides a seamless pipeline to generate folder structures from ASCII trees, automatically detect project configurations, and compile your entire codebase into a single markdown context report tailored for Large Language Models (LLMs).

## ✨ Features

- **`nexus scaffold`**: Instantly generate complex folder and file structures from standard ASCII tree diagrams. Includes smart boilerplate injection for `.py`, `.md`, `.env`, and `.gitignore` files.
- **`nexus init`**: Intelligently scans projects, detects extensions, and generates a modular `nexus.json` configuration file.
- **`nexus scan`**: Compiles your project into a Markdown report with pro-level optimizations:
    - **🗜️ Minification**: Strips redundant whitespace and newlines to maximize token efficiency.
    - **📊 Token Estimation**: Real-time token counting using `tiktoken` (`cl100k_base`).
    - **📋 Auto-Clipboard**: Optional instant copying of reports for immediate use in LLMs.
    - **🕒 Smart Snapshots**: Automatic timestamped filenames and self-exclusion logic to prevent context pollution.
- **🔌 Modular Handlers**: Easily extend Nexus by adding custom parsers in a `.nexus/custom_handlers.py` file.

## 📦 Installation

Ensure you have Python 3.9+ installed.

### Option 1: Direct Install from GitHub (Recommended)
Install Nexus CLI directly into your active virtual environment:
```bash
pip install git+https://github.com/yenksid/nexus_cli.git
```

### Option 2: Local Development
```bash
git clone https://github.com/yenksid/nexus_cli.git
cd nexus_cli
pip install -e .
```
*(Note: Using -e installs the package in "editable" mode, meaning changes to the code are reflected immediately without re-installing).*

## 🚀 The Nexus Pipeline (Usage)
Once installed, the `nexus` command is available globally within your active environment.

### 1. Scaffold a New Project (Optional)
Generate a project structure from an ASCII tree:

```bash
nexus scaffold -f my_tree.txt -o ./MyNewProject
```

### 2. Initialize Configuration
Navigate to your project and run init. It will scan for extensions and create your nexus.json config:

```bash
cd MyNewProject
nexus init --yes
```

### 3. Generate AI Context
Create a snapshot of your codebase for your LLM. Use the QoL flags to optimize your tokens:

```bash
# Basic scan with dynamic timestamp
nexus scan

# Full QoL: Minify output and copy result to clipboard automatically
nexus scan -m -c
# Example Output: ✅ Context Snapshot saved to: context_20260214_200226.md (~6,541 tokens).

# Specify a custom output file
nexus scan -o NEXUS_CONTEXT.md
```

## 🔌 Extending Nexus (Modular Plugins)
You can teach Nexus how to handle new file types without modifying the core source code. Create a file at `.nexus/custom_handlers.py` in your project root:

```python
from nexus_cli.handlers import register_handler

@register_handler("my_type")
def handle_custom(filepath):
    return f"### CUSTOM: {filepath}\nProcessed content here."
```
Then, map the extension in your `nexus.json`:

```json
"translators": {
    "xyz": "my_type"
}
```

## 🧪 Running Tests
The project includes an end-to-end Automated Test Suite verifying the entire pipeline for both new and legacy projects:

```bash
python tests/run_tests.py
```
## 🗺️ Project Roadmap
We are actively building the future of context orchestration. You can track our progress through our GitHub Issues.

- [ ] **Phase 1: Infrastructure** (#4)  
  Implement a fully automated changelog and release pipeline using Conventional Commits.

- [ ] **Phase 2: Semantic Intelligence** (#1)  
  Integrate LLMs to generate automated semantic summaries of project architectures.

- [ ] **Phase 3: Context Filtering** (#2)  
  Add task-based API integration to intelligently select only relevant files for a specific scan.

- [ ] **Phase 4: Advanced Retrieval (RAG)** (#3)  
  Bridge Nexus CLI with OpenRAG to enable semantic querying and vector-based context retrieval.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.