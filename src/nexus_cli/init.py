#!/usr/bin/env python3
"""
init.py - Initialization Module for Nexus CLI
Auto-generates the nexus.json configuration file.
"""
import os
import json
from pathlib import Path

# --- CONSTANTS & COLORS ---
class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# --- NEW IGNORE PATTERNS ADDED HERE ---
DEFAULT_IGNORE = [
    ".git", "venv", "__pycache__", "node_modules", 
    "site-packages", ".egg-info", "nexus_tool", "test_output",
    "context_*.md", "nexus_report_*.md" 
]

EXT_GUESSER = {
    "py": "code", "js": "code", "ts": "code", "html": "code", "css": "code",
    "json": "code", "yaml": "code", "yml": "code", "bat": "code", "sh": "code",
    "md": "text", "txt": "text", "tex": "text", "bib": "text", "csv": "csv",
    "png": "image", "jpg": "image", "jpeg": "image", "gif": "image", "pdf": "pdf"
}

def run_init(args):
    print(f"{C.CYAN}🚀 Initializing Nexus Project...{C.RESET}")
    
    if Path("nexus.json").exists() and not getattr(args, 'force', False):
        print(f"{C.YELLOW}⚠️  nexus.json already exists in this directory!{C.RESET}")
        print("Use 'nexus init --force' to overwrite it.")
        return
        
    default_name = Path.cwd().name
    if getattr(args, 'yes', False):
        project_name = default_name
    else:
        project_name = input(f"📦 Project name ({default_name}): ").strip() or default_name

    print("\n🔍 Scanning current directory for file types...")
    found_exts = set()
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not any(ig in d for ig in DEFAULT_IGNORE)]
        for file in files:
            if "." in file and not file.startswith("."):
                ext = file.rsplit(".", 1)[-1].lower()
                found_exts.add(ext)
                
    found_exts = sorted(list(found_exts))
    
    if not found_exts:
        print(f"{C.YELLOW}No files found. Using default extension tracking.{C.RESET}")
        selected_exts = ["py", "md", "txt", "csv", "png", "pdf"]
    else:
        print(f"\n{C.GREEN}📋 Detected extensions:{C.RESET} {', '.join(found_exts)}")
        if getattr(args, 'yes', False):
            selected_exts = found_exts
        else:
            print(f"Press {C.YELLOW}[Enter]{C.RESET} to track ALL, or type specific ones (e.g. py,md):")
            user_input = input(f"{C.CYAN}Extensions > {C.RESET}").strip()
            if not user_input:
                selected_exts = found_exts
            else:
                selected_exts = [e.strip().strip(".") for e in user_input.split(",") if e.strip()]
    
    translators = {}
    for ext in selected_exts:
        translators[ext] = EXT_GUESSER.get(ext, "text")
        
    config = {
        "project_name": project_name,
        "watch_dirs": ["."],
        "ignore_patterns": DEFAULT_IGNORE,
        "translators": translators
    }
    
    with open("nexus.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    print(f"\n{C.GREEN}✅ Successfully generated nexus.json for '{project_name}'!{C.RESET}")
    print("You can now run 'nexus scan' to generate your AI context report.")