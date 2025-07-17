#!/usr/bin/env python3
"""
Cleanup script for the Spam Email Detector project.
Removes unnecessary files and keeps only the essential ones.
"""

import os
import shutil
import sys

# Check if running in a virtual environment
def check_venv():
    """Check if running in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if not check_venv():
    print("\nERROR: Virtual environment is not activated.")
    print("You must activate the virtual environment before running this script.")
    print("\nTo activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("  venv\\Scripts\\activate")
    else:  # macOS/Linux
        print("  source venv/bin/activate")
    
    print("\nExiting. Please activate the virtual environment and try again.")
    sys.exit(1)

def cleanup_project():
    """Clean up the project directory by removing unnecessary files."""
    print("Cleaning up the Spam Email Detector project...")
    
    # Files to keep
    files_to_keep = [
        "spam_detector.py",
        "test_model.py",
        "convert_data.py",
        "requirements.txt",
        "README.md",
        "HOW_TO_RUN.md",
        ".gitignore",
        "mail_data.csv",
        "cleanup.py",  # Keep this script
        "run.py"  # Add run.py to the list of files to keep
    ]
    
    # Directories to keep
    dirs_to_keep = [
        "venv",
        "spam_nlp"
    ]
    
    # Get all files and directories in the current directory
    all_items = os.listdir(".")
    
    # Remove files that are not in the keep list
    for item in all_items:
        if os.path.isfile(item) and item not in files_to_keep:
            print(f"Removing file: {item}")
            try:
                os.remove(item)
            except Exception as e:
                print(f"  Error removing {item}: {e}")
        elif os.path.isdir(item) and item not in dirs_to_keep:
            print(f"Removing directory: {item}")
            try:
                shutil.rmtree(item)
            except Exception as e:
                print(f"  Error removing directory {item}: {e}")
    
    print("\nProject cleaned up successfully!")
    print("\nRemaining files:")
    for item in sorted(os.listdir(".")):
        if os.path.isdir(item):
            print(f"📁 {item}/")
        else:
            print(f"📄 {item}")

if __name__ == "__main__":
    # Ask for confirmation
    print("This script will remove all unnecessary files from the project.")
    print("The following files will be kept:")
    for file in sorted(["spam_detector.py", "test_model.py", "convert_data.py", 
                 "requirements.txt", "README.md", "HOW_TO_RUN.md", 
                 ".gitignore", "mail_data.csv", "cleanup.py"]):
        print(f"  - {file}")
    print("\nThe following directories will be kept:")
    for dir in sorted(["venv", "spam_nlp"]):
        print(f"  - {dir}/")
    
    confirm = input("\nDo you want to continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Cleanup cancelled.")
        sys.exit(0)
    
    cleanup_project() 