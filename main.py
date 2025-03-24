from mcp.server.fastmcp import FastMCP
from pathlib import Path
from typing import List

# Create an MCP server
mcp = FastMCP("Android source code")

def is_android_project(project_dir: str) -> bool:
    """Validate if a directory is an Android project root by checking for key gradle files."""
    path = Path(project_dir)
    
    # Check if directory exists
    if not path.is_dir():
        return False
    
    # Check for essential gradle files that identify Android projects
    has_settings_gradle = any(path.glob('settings.gradle*'))
    has_build_gradle = any(path.glob('build.gradle*'))
    
    # An Android project must have both settings.gradle and build.gradle at root level
    return has_settings_gradle and has_build_gradle

@mcp.tool()
async def validate_android_project(project_dir: str) -> str:
    """Validate if a directory is an Android project root.
    Returns success message if valid, otherwise error details.
    """
    path = Path(project_dir)
    
    if not path.is_dir():
        return f"Error: Directory does not exist: {project_dir}"
    
    if is_android_project(project_dir):
        return f"Valid Android project detected at: {project_dir}"
    else:
        return f"Not a valid Android project. Missing essential gradle configuration files."

@mcp.tool()
async def get_all_project_files(project_dir: str) -> str:
    """Get list of available files in android project. Returns
    kotlin files, kts files, toml files and AndriodManifest.xml file.
    Output shows project root and files grouped by relative directory.
    """
    path = Path(project_dir)
    
    if not path.is_dir():
        raise ValueError(f"Directory does not exist: {project_dir}")
    
    if not is_android_project(project_dir):
        raise ValueError(f"Not a valid Android project: {project_dir}")
    
    dir_files = {}
    
    for file_path in path.rglob('*'):
        # Exclude files in .gradle and .git directories
        if any(part in {".gradle", ".git", "build"} for part in file_path.parts):
            continue
        if file_path.suffix in {'.kt', '.kts', '.toml'} or file_path.name == 'AndroidManifest.xml':
            # Get relative path to project root
            rel_dir = str(file_path.parent.relative_to(path))
            if rel_dir not in dir_files:
                dir_files[rel_dir] = []
            dir_files[rel_dir].append(file_path.name)
    
    # Sort directories and their files
    output = [f"Project root: {path}"]
    for directory in sorted(dir_files.keys()):
        output.append(f"\ndir: {directory}")
        output.append(f"files: {', '.join(sorted(dir_files[directory]))}")
    
    return '\n'.join(output)

@mcp.tool()
async def read_project_file(project_dir: str, file_path: str) -> str:
    """Read contents of a file from an android project. Returns raw file content.
    Only allows files with extensions: .kt, .kts, .toml, .md or AndroidManifest.xml
    """
    root = Path(project_dir)
    
    if not root.is_dir():
        raise ValueError(f"Directory does not exist: {project_dir}")
    
    if not is_android_project(project_dir):
        raise ValueError(f"Not a valid Android project: {project_dir}")
    
    full_path = root / file_path
    
    # Security checks
    if any(part in {".gradle", ".git", "build"} for part in full_path.parts):
        raise ValueError("Access to restricted directories denied")
    
    if not (full_path.suffix in {'.kt', '.kts', '.toml', '.md'} or full_path.name == 'AndroidManifest.xml'):
        raise ValueError("File type not allowed")
    
    if not full_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return full_path.read_text()

@mcp.tool()
async def read_multiple_project_files(project_dir: str, file_paths: List[str]) -> str:
    """Read contents of multiple files from an android project. Returns concatenated content with file headers.
    Only allows files with extensions: .kt, .kts, .toml, .md or AndroidManifest.xml
    """
    root = Path(project_dir)
    
    if not root.is_dir():
        raise ValueError(f"Directory does not exist: {project_dir}")
    
    if not is_android_project(project_dir):
        raise ValueError(f"Not a valid Android project: {project_dir}")
    
    output = []
    
    for file_path in file_paths:
        full_path = root / file_path
        
        # Security checks
        if any(part in {".gradle", ".git", "build"} for part in full_path.parts):
            raise ValueError(f"Access to restricted directories denied for file: {file_path}")
        
        if not (full_path.suffix in {'.kt', '.kts', '.toml', '.md'} or full_path.name == 'AndroidManifest.xml'):
            raise ValueError(f"File type not allowed: {file_path}")
        
        if not full_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = full_path.read_text()
        output.append(f"// {file_path}\n{content}")
    
    return '\n\n'.join(output)

if __name__ == "__main__":
    mcp.run(transport='stdio')