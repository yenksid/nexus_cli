import os
import pandas as pd
from PIL import Image
from pypdf import PdfReader

# This is our central registry
REGISTRY = {}

def register_handler(name):
    """Decorator to easily register a new file handler."""
    def decorator(func):
        REGISTRY[name] = func
        return func
    return decorator

@register_handler("csv")
def handle_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        return f"### DATA: {os.path.basename(filepath)}\n- Shape: {df.shape}\n- Columns: {list(df.columns)}\n"
    except Exception as e: return f"### CSV ERROR: {e}\n"

@register_handler("code")
def handle_code(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f"### CODE: {os.path.basename(filepath)}\n```\n{f.read()[:3000]}\n...\n```\n"
    except: return ""

@register_handler("text")
def handle_text(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f"### TEXT: {os.path.basename(filepath)}\n{f.read()[:2000]}\n"
    except: return ""

@register_handler("image")
def handle_image(filepath):
    try:
        with Image.open(filepath) as img:
            return f"### IMAGE: {os.path.basename(filepath)}\n- Format: {img.format} | Size: {img.size} | Mode: {img.mode}\n"
    except Exception as e: return f"### IMG ERROR: {e}\n"

@register_handler("pdf")
def handle_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = reader.pages[0].extract_text()[:1000] if len(reader.pages) > 0 else "Empty"
        return f"### PDF: {os.path.basename(filepath)}\n- Pages: {len(reader.pages)}\n- Preview:\n> {text}...\n"
    except Exception as e: return f"### PDF ERROR: {e}\n"