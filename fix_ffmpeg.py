import os
import sys

# Try to import imageio_ffmpeg to get the executable path
try:
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Found ffmpeg at: {ffmpeg_exe}")
except ImportError:
    print("imageio_ffmpeg not found. Please install it first.")
    sys.exit(1)

# Escape backslashes for python string
ffmpeg_exe_escaped = ffmpeg_exe.replace('\\', '\\\\')

# Files to patch
files_to_patch = [
    "src/utils/videoio.py",
    "src/gradio_demo.py"
]

for file_path in files_to_patch:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
        
    print(f"Patching {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    # Add import if missing
    if "import imageio_ffmpeg" not in new_content:
        # Insert after imports
        lines = new_content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                continue
            if line.strip() == "":
                continue
            # Found first non-import line (or just insert at top)
            lines.insert(0, "import imageio_ffmpeg")
            break
        new_content = "\n".join(lines)

    # Replace os.system(cmd) with modified cmd
    # We need to be careful. The code constructs 'cmd' string.
    # We want to replace "ffmpeg " with the full path.
    
    # In videoio.py:
    # cmd = r'ffmpeg -y ...'
    # We replace r'ffmpeg with r'"{ffmpeg_exe}"
    
    # In gradio_demo.py:
    # cmd = r"ffmpeg -y ..."
    
    # We can just replace the string literal content.
    
    # Replace 'ffmpeg ' with '"{ffmpeg_exe}" '
    # But we need to handle the raw string quotes.
    
    # Let's try a simpler approach: replace "ffmpeg " with the executable path.
    # But since it's inside a string, we need to be careful about quotes.
    
    # If we use imageio_ffmpeg.get_ffmpeg_exe() at runtime in the patched file, it's better.
    
    # Strategy:
    # 1. Add `import imageio_ffmpeg`
    # 2. Add `ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()` near imports or inside function?
    # Better to just replace the string "ffmpeg " with a format string?
    
    # Let's try to replace the string literal "ffmpeg " with something that injects the path.
    # But that's hard with regex.
    
    # Alternative: Just replace the string "ffmpeg" with the absolute path we found NOW.
    # This is easier but less portable if moved. But for this user it's fine.
    
    # We will use the escaped path.
    
    # Replace r'ffmpeg with r'"{ffmpeg_exe_escaped}"
    new_content = new_content.replace("r'ffmpeg", f"r'\"{ffmpeg_exe_escaped}\"")
    new_content = new_content.replace('r"ffmpeg', f'r"\"{ffmpeg_exe_escaped}\"')
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {file_path}")
    else:
        print(f"No changes made to {file_path}")
