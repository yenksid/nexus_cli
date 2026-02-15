# .nexus/custom_handlers.py
import json
import os
from nexus_cli.handlers import register_handler

@register_handler("notebook")
def handle_ipynb(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        cells = [c['source'] for c in nb['cells'] if c['cell_type'] == 'code']
    return f"### JUPYTER NOTEBOOK: {os.path.basename(filepath)}\n```python\n{''.join(cells[:5])}...\n```\n"