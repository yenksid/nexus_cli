#!/usr/bin/env python3
"""
scaffolding.py - CLI Version
Generates a folder and file structure from an ASCII tree.
"""

from __future__ import annotations
import re
import sys
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

# --- CONSTANTS & COLORS ---
class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

CONNECTOR_RE = re.compile(r"^(├──|└──|\+--|\|--|`--)\s*")
CONNECTOR_FUZZY_RE = re.compile(r"(├──|└──|\+--|\|--|`--)\s*")

# --- AUTOMATIC BOILERPLATES ---
BOILERPLATES = {
    ".py": 'def main():\n    pass\n\nif __name__ == "__main__":\n    main()\n',
    ".gitignore": "venv/\n__pycache__/\n.env\n*.pyc\n.DS_Store\n",
    ".env": "ENV=development\nDEBUG=True\nSECRET_KEY=your_secret_here\n",
    ".md": "# New Project\n\nProject description goes here.\n"
}

@dataclass
class Entry:
    depth: int
    raw_name: str
    is_dir_hint: bool 

# --- UTILITIES ---

def get_confirmation(prompt: str, auto_yes: bool = False) -> bool:
    if auto_yes: return True
    while True:
        response = input(f"{C.YELLOW}{prompt} (y/n): {C.RESET}").strip().lower()
        if response in ["y", "yes", "s"]: return True
        if response in ["n", "no"]: return False
        print(f"{C.RED}❌ Please type 'y' or 'n'.{C.RESET}")

def sanitize_component(component: str) -> str:
    component = component.strip().strip('"').strip("'")
    illegal = '<>:"/\\|?*'
    component = "".join("_" if ch in illegal or ord(ch) < 32 else ch for ch in component)
    component = component.rstrip(" .")
    if not component: component = "_"
    if component.upper() in WINDOWS_RESERVED: component += "_"
    return component

# --- PARSING LOGIC ---

def strip_inline_notes(s: str) -> str:
    if "<--" in s: s = s.split("<--", 1)[0]
    if "#" in s: s = s.split("#", 1)[0]
    s = re.split(r"\s{2,}", s, maxsplit=1)[0]
    s = re.split(r"\s+//", s, maxsplit=1)[0]
    return s.strip()

def count_tree_depth(line: str) -> Tuple[int, str]:
    line = line.expandtabs(4)
    depth = 0
    i = 0
    while i < len(line):
        if line[i:i+4] in ("│   ", "    ", "|   "):
            depth += 1
            i += 4
        elif line[i:i+2] == "  ":
            depth += 1
            i += 2
        else:
            break
    return depth, line[i:]

def extract_name_from_line(line: str) -> Optional[Entry]:
    depth, rest = count_tree_depth(line)
    rest = rest.lstrip()
    
    m = CONNECTOR_RE.match(rest)
    if not m:
        m2 = CONNECTOR_FUZZY_RE.search(rest)
        if not m2: return None
        name_part = rest[m2.end():]
    else:
        name_part = rest[m.end():]

    name_part = strip_inline_notes(name_part)
    if not name_part: return None
    
    return Entry(depth=depth, raw_name=name_part, is_dir_hint=name_part.endswith("/"))

def parse_tree(lines: List[str]) -> Tuple[str, List[Entry]]:
    non_empty = [l for l in lines if l.strip()]
    if not non_empty: raise ValueError("No valid content found.")
    
    root_name = strip_inline_notes(non_empty[0]).rstrip("/").strip()
    if not root_name: root_name = "project_root"
    
    entries = []
    for raw in non_empty[1:]:
        e = extract_name_from_line(raw)
        if e: entries.append(e)
            
    return root_name, entries

def build_plan(root_dir: Path, entries: List[Entry]) -> List[Tuple[Path, bool]]:
    plan = []
    stack: List[Path] = [] 

    for i, e in enumerate(entries):
        while len(stack) > e.depth:
            stack.pop()
        
        next_depth = entries[i+1].depth if i+1 < len(entries) else -1
        is_dir = e.is_dir_hint or (next_depth > e.depth)
        
        clean_name = sanitize_component(e.raw_name.rstrip("/"))
        current_path = root_dir.joinpath(*stack) / clean_name
        
        plan.append((current_path, is_dir))
        if is_dir: stack.append(Path(clean_name))

    return plan

def preview_plan(root_dir: Path, plan: List[Tuple[Path, bool]]):
    print(f"\n{C.CYAN}--- PLAN PREVIEW ---{C.RESET}")
    print(f"{C.GREEN}📁 {root_dir}{C.RESET} (Base Directory)")
    
    for path, is_dir in plan[:40]:
        try: rel_path = path.relative_to(root_dir.parent)
        except ValueError: rel_path = path.name
        
        icon = "📁" if is_dir else "📄"
        print(f"  {icon} {rel_path}")
        
    if len(plan) > 40:
        print(f"  ... and {len(plan) - 40} more items.")
    print(f"{C.CYAN}--------------------{C.RESET}\n")

def save_json_plan(root_dir: Path, plan: List[Tuple[Path, bool]]):
    data = {
        "root": str(root_dir),
        "items": [{"path": str(p), "type": "dir" if d else "file"} for p, d in plan]
    }
    log_path = root_dir.parent / f"{root_dir.name}_plan.json"
    
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"{C.GREEN}📄 Plan saved to: {log_path}{C.RESET}")
    except OSError as e:
        print(f"{C.RED}❌ Failed to save JSON: {e}{C.RESET}")

def apply_plan(plan: List[Tuple[Path, bool]], overwrite: bool, use_boilerplate: bool):
    d_count, f_count = 0, 0
    for path, is_dir in plan:
        if is_dir:
            path.mkdir(parents=True, exist_ok=True)
            d_count += 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or overwrite:
                content = ""
                if use_boilerplate:
                    if path.name == ".gitignore": content = BOILERPLATES[".gitignore"]
                    elif path.name == ".env": content = BOILERPLATES[".env"]
                    else: content = BOILERPLATES.get(path.suffix, "")
                
                path.write_text(content, encoding="utf-8")
                f_count += 1
    return d_count, f_count


# --- ENTRY POINT FOR ROUTER ---

def run_scaffold(args):
    """
    This is the new entry point called by main.py.
    It receives 'args' directly from the router.
    """
    lines = []

    # 1. READ INPUT
    if args.file:
        if not args.file.exists():
            print(f"{C.RED}❌ File does not exist: {args.file}{C.RESET}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"{C.CYAN}📥 Reading tree from: {args.file}{C.RESET}")
    else:
        if sys.stdin.isatty():
            print(f"{C.CYAN}Paste your ASCII tree.{C.RESET} Press Enter on {C.YELLOW}two consecutive empty lines{C.RESET} to finish:")
        empty_count = 0
        while True:
            try:
                line = input()
                if not line.strip():
                    empty_count += 1
                    if empty_count >= 2: break
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError: break

    # 2. PARSE AND EXECUTE
    try:
        root_name, entries = parse_tree(lines)
        base_dir = args.out.expanduser().resolve()
        
        try:
            base_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"{C.RED}❌ System Error: Cannot access or create the base directory '{base_dir}'.{C.RESET}")
            print(f"{C.YELLOW}Make sure the drive exists and you have write permissions.{C.RESET}")
            sys.exit(1)

        root_dir = base_dir / sanitize_component(root_name)
        plan = build_plan(root_dir, entries)
        
        preview_plan(root_dir, plan)
        print(f"{C.CYAN}{len(plan)} items{C.RESET} will be created in total.")
        
        if args.dry_run:
            print(f"\n{C.YELLOW}🏁 Dry-run completed. No changes were made to the disk.{C.RESET}")
            sys.exit(0)

        if args.json or get_confirmation("Save a copy of the plan as JSON?", args.yes):
            save_json_plan(root_dir, plan)
            
        ow = get_confirmation("Overwrite existing files?", args.yes)
        
        if get_confirmation("Proceed with creation on disk?", args.yes):
            dc, fc = apply_plan(plan, ow, not args.no_boilerplate)
            print(f"\n{C.GREEN}✅ Success! Folders created: {dc}, Files created/updated: {fc}{C.RESET}")
        else:
            print(f"{C.YELLOW}🛑 Operation cancelled by user.{C.RESET}")
            
    except Exception as e:
        print(f"{C.RED}❌ Error: {e}{C.RESET}")
        sys.exit(1)