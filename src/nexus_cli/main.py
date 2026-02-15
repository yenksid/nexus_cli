#!/usr/bin/env python3
import argparse
from pathlib import Path

# Import our subcommands
from nexus_cli.context import run_scan
from nexus_cli.scaffolding import run_scaffold
from nexus_cli.init import run_init

def main():
    parser = argparse.ArgumentParser(
        prog="nexus", 
        description="Nexus CLI Suite for AI Development & Project Management"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")

    # --- Subcommand: INIT ---
    parser_init = subparsers.add_parser("init", help="Initialize Nexus project and generate nexus.json")
    parser_init.add_argument("-f", "--force", action="store_true", help="Overwrite existing nexus.json")
    parser_init.add_argument("-y", "--yes", action="store_true", help="Auto-accept all found extensions")

    # --- Subcommand: SCAN ---
    parser_scan = subparsers.add_parser("scan", help="Generate context report for LLMs")
    parser_scan.add_argument("-o", "--output", help="Output filename (default: dynamic timestamp)")
    parser_scan.add_argument("-c", "--copy", action="store_true", help="Copy the generated context to clipboard")
    parser_scan.add_argument("-m", "--minify", action="store_true", help="Minify output to save tokens (strips extra newlines/spaces)")

    # --- Subcommand: SCAFFOLD ---
    parser_scaf = subparsers.add_parser("scaffold", help="Generate directory structure from ASCII tree")
    parser_scaf.add_argument("-f", "--file", type=Path, help="Path to ASCII tree text file")
    parser_scaf.add_argument("-o", "--out", type=Path, default=Path.cwd(), help="Output destination directory")
    parser_scaf.add_argument("-y", "--yes", action="store_true", help="Automatically accept all confirmations")
    parser_scaf.add_argument("--json", action="store_true", help="Automatically export plan as JSON")
    parser_scaf.add_argument("--dry-run", action="store_true", help="Display the plan and exit without creating anything")
    parser_scaf.add_argument("--no-boilerplate", action="store_true", help="Create files completely empty")

    # Parse and Dispatch
    args = parser.parse_args()
    
    if args.command == "init":
        run_init(args)
    elif args.command == "scan":
        run_scan(args)
    elif args.command == "scaffold":
        run_scaffold(args)

if __name__ == "__main__":
    main()