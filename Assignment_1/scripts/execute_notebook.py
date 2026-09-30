"""Run the notebook in a fresh kernel using this project's Python."""
import os
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]
expected = ROOT / '.venv' / 'Scripts' / 'python.exe'
if Path(sys.executable).resolve() != expected.resolve():
    raise RuntimeError('Run this helper using .venv/Scripts/python.exe.')
os.environ['IPYTHONDIR'] = str(ROOT / '.venv' / 'ipython')
os.environ['JUPYTER_RUNTIME_DIR'] = str(ROOT / '.venv' / 'jupyter_runtime')
path = ROOT / 'AB_Testing_Assignment.ipynb'
notebook = nbformat.read(path, as_version=4)
manager = KernelManager(kernel_name='python3')
# Override the launch command explicitly; no global/user kernel registration.
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(notebook, km=manager, timeout=120,
                        resources={'metadata': {'path': str(ROOT)}}, allow_errors=False)
try:
    client.execute()
finally:
    nbformat.write(notebook, path)
nbformat.validate(notebook)
print('Notebook executed in a fresh project kernel and outputs saved.')
