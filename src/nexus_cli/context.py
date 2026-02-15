#!/usr/bin/env python3
"""
context.py - Context Scanner Module for Nexus CLI
Scans the project directory and compiles files into an LLM-ready markdown report.
"""

import os
import re  # <--- NEW: Regular Expressions for Minification
import json
import fnmatch
import importlib.util
from datetime import datetime

# --- QoL Libraries ---
import tiktoken
import pyperclip
from rich.console import Console # <--- NEW

# Import the core registry from our handlers module
from nexus_cli.handlers import REGISTRY

def load_config():
    """Loads nexus.json or returns a default configuration."""
    if os.path.exists("nexus.json"):
        print("[Nexus] Loading configuration from nexus.json")
        with open("nexus.json", "r", encoding="utf-8") as f:
            return json.load(f)
            
    print("[Nexus] WARNING: nexus.json not found. Using defaults.")
    return {
        "project_name": os.path.basename(os.getcwd()),
        "watch_dirs": ["."],
        "ignore_patterns": [
            ".git", "venv", "__pycache__", "nexus_tool", 
            "test_output", "context_*.md", "nexus_report_*.md"
        ],
        "translators": {
            "csv": "csv", "py": "code", "js": "code", "md": "text", 
            "txt": "text", "png": "image", "jpg": "image", "pdf": "pdf",
            "tex": "text", "bib": "text", "bat": "code", "yml": "code"
        }
    }

def is_ignored(path_string, ignore_patterns):
    """Evaluates if a path should be ignored using both substrings and wildcards."""
    for pattern in ignore_patterns:
        if pattern in path_string or fnmatch.fnmatch(os.path.basename(path_string), pattern):
            return True
    return False

def load_custom_handlers():
    """Loads a custom_handlers.py file from the user's project if it exists."""
    custom_path = os.path.join(os.getcwd(), ".nexus", "custom_handlers.py")
    if os.path.exists(custom_path):
        print(f"[Nexus] 🔌 Loading custom extensions from {custom_path}")
        try:
            spec = importlib.util.spec_from_file_location("custom_handlers", custom_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"[Nexus] ❌ Failed to load custom handlers: {e}")

# Initialize a Rich console
console = Console()

def run_scan(args):
    """Entry point for the 'nexus scan' subcommand."""
    config = load_config()
    load_custom_handlers()  
    
    # Use a status spinner for a premium CLI feel
    with console.status("[bold cyan][Nexus] Scanning project files...", spinner="dots") as status:
        report = f"# NEXUS CONTEXT REPORT: {config.get('project_name')}\n**Generated:** {datetime.now()}\n\n"
        
        files_processed = 0
        watch_dirs = config.get("watch_dirs", ["."])

        for directory in watch_dirs:
            if not os.path.exists(directory):
                continue
                
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), config["ignore_patterns"])]
                    
                for file in files:
                    path = os.path.join(root, file)
                    if is_ignored(path, config["ignore_patterns"]):
                        continue

                    # Update status message for the current file
                    status.update(f"[bold cyan][Nexus] Processing: [white]{file}")

                    ext = file.split(".")[-1].lower()
                    translator = config["translators"].get(ext)

                    if translator and translator in REGISTRY:
                        try:
                            content = REGISTRY[translator](path)
                            if content:
                                report += content + "\n---\n"
                                files_processed += 1
                        except Exception as e:
                            console.print(f"[bold red]! Error reading {file}: {e}")
    
    # --- Token Minification ---
    if getattr(args, 'minify', False):
        report = re.sub(r'[ \t]+$', '', report, flags=re.MULTILINE)
        report = re.sub(r'\n{3,}', '\n\n', report)
        console.print("[cyan][Nexus] 🗜️  Report minified (removed extra spaces and newlines).")

    # --- Save Logic ---
    if getattr(args, 'output', None):
        out_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"context_{timestamp}.md"
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
        
    # --- Token Estimation ---
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        token_count = len(enc.encode(report))
        token_msg = f" (~{token_count:,} tokens)"
    except Exception:
        token_msg = ""
        
    console.print(f"[bold green]✅ Context Snapshot saved to: [white]{out_path}{token_msg}")

    # --- Auto-Clipboard ---
    if getattr(args, 'copy', False):
        try:
            pyperclip.copy(report)
            console.print("[bold blue]📋 Output successfully copied to clipboard!")
        except Exception as e:
            console.print(f"[bold yellow]⚠️ Failed to copy to clipboard: {e}")