import subprocess
from pathlib import Path

from agents import function_tool

WORKSPACE = Path("/tmp/workspace")

def workspace_path(path: str) -> Path:
    return WORKSPACE/path.lstrip("/")

@function_tool
def write(path: str, content: str) -> str:
    """write content to a file."""
    file_path = workspace_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return f"wrote {file_path}"

@function_tool
def edit(path:str, old, new: str) -> str:
    """Replace text in a file.""" 
    file_path = workspace_path(path)
    content = file_path.read_text()

    if old not in content:
        return f"Text not found in {file_path}"

    file_path.write_text(content.replace(old, new))
    return f"Edited {file_path}" 


@function_tool
def exec_command (command: str) -> str:
    """Run a shell command."""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        command,
        shell=True,
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        timeout=30,
    )

    output = result.stdout+ result.stderr
    return output.strip() or f"Command exited with code {result.returncode}"