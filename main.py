from mcp.server.fastmcp import FastMCP
from pathlib import Path

project_roots: dict[str, str] = {
    "palau": "/Users/sdi/work/palau-android"
}

# Create an MCP server
mcp = FastMCP("Android source code")

@mcp.tool()
async def get_all_projects() -> list[str]:
    """Get list of available project names"""
    return list(project_roots.keys())

@mcp.tool()
async def get_all_project_files(project_name: str) -> str:
    """Get list of available files in android project. Returns
    kotlin files, kts files, toml files and AndriodManifest.xml file.
    Output shows project root and files grouped by relative directory.
    """
    if project_name not in project_roots:
        raise ValueError(f"Project {project_name} not found. Available projects: {', '.join(project_roots.keys())}")
    
    root = Path(project_roots[project_name])
    dir_files = {}
    
    for path in root.rglob('*'):
        # Exclude files in .gradle and .git directories
        if any(part in {".gradle", ".git", "build"} for part in path.parts):
            continue
        if path.suffix in {'.kt', '.kts', '.toml'} or path.name == 'AndroidManifest.xml':
            # Get relative path to project root
            rel_dir = str(path.parent.relative_to(root))
            if rel_dir not in dir_files:
                dir_files[rel_dir] = []
            dir_files[rel_dir].append(path.name)
    
    # Sort directories and their files
    output = [f"Project root: {root}"]
    for directory in sorted(dir_files.keys()):
        output.append(f"\ndir: {directory}")
        output.append(f"files: {', '.join(sorted(dir_files[directory]))}")
    
    return '\n'.join(output)

@mcp.tool()
async def read_project_file(project_name: str, file_path: str) -> str:
    """Read contents of a file from an android project. Returns raw file content.
    Only allows files with extensions: .kt, .kts, .toml or AndroidManifest.xml
    """
    if project_name not in project_roots:
        raise ValueError(f"Project {project_name} not found. Available projects: {', '.join(project_roots.keys())}")
    
    root = Path(project_roots[project_name])
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
async def read_multiple_project_files(project_name: str, file_paths: list[str]) -> str:
    """Read contents of multiple files from an android project. Returns concatenated content with file headers.
    Only allows files with extensions: .kt, .kts, .toml, .md or AndroidManifest.xml
    """
    if project_name not in project_roots:
        raise ValueError(f"Project {project_name} not found. Available projects: {', '.join(project_roots.keys())}")
    
    root = Path(project_roots[project_name])
    output = []
    
    for file_path in file_paths:
        full_path = root / file_path
        
        # Security checks
        if any(part in {".gradle", ".git", "build"} for part in full_path.parts):
            raise ValueError(f"Access to restricted directories denied for file: {file_path}")
        
        if not (full_path.suffix in {'.kt', '.kts', '.toml'} or full_path.name == 'AndroidManifest.xml'):
            raise ValueError(f"File type not allowed: {file_path}")
        
        if not full_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = full_path.read_text()
        output.append(f"// {file_path}\n{content}")
    
    return '\n\n'.join(output)



if __name__ == "__main__":
    mcp.run(transport='stdio')
