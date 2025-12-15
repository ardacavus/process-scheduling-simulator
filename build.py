import customtkinter
import os
import subprocess
import sys

# 1. Locate CustomTkinter path dynamically
ctk_path = os.path.dirname(customtkinter.__file__)
print(f"CustomTkinter path found: {ctk_path}")

# 2. Determine OS separator (';' for Windows, ':' for Unix)
separator = ';' if os.name == 'nt' else ':'

# 3. Prepare PyInstaller command
# --add-data "SOURCE;DESTINATION"
command = [
    "pyinstaller",
    "--noconsole",       # Hide console window
    "--onefile",         # Bundle everything into a single EXE
    f"--add-data={ctk_path}{separator}customtkinter", # Include theme files
    "--name=CS305_Scheduler_Ultimate", # Output filename
    "gui.py"             # Entry point
]

print("\nStarting build process...")
print("Executing command:", " ".join(command))
print("-" * 50)

# 4. Execute the command
try:
    subprocess.run(command, check=True, shell=(os.name == 'nt'))
    print("\n" + "="*50)
    print("✅ SUCCESS! Executable created.")
    print("Check the 'dist' folder for the output file.")
    print("="*50)
except subprocess.CalledProcessError as e:
    print("\n" + "="*50)
    print("❌ ERROR: Build failed.")
    print("Details:", e)
    print("="*50)