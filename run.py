#!/usr/bin/env python3
"""
Runner script for the Spam Email Detector project.
Provides a command-line interface to run different parts of the application.
"""

import os
import sys
import subprocess

def print_header():
    """Print a header for the application."""
    print("\n" + "=" * 60)
    print("               SPAM EMAIL DETECTOR")
    print("=" * 60)

def check_venv():
    """Check if running in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def run_command(command):
    """Run a command and return its output."""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def show_menu():
    """Display the main menu."""
    print("\nChoose an option:")
    print("1. Convert data file")
    print("2. Run GUI application")
    print("3. Run command-line test")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    return choice

def main():
    """Main function to run the application."""
    print_header()
    
    # Check if running in a virtual environment - STRICT ENFORCEMENT
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
    
    # Check if required files exist
    if not os.path.exists("convert_data.py") or not os.path.exists("spam_detector.py") or not os.path.exists("test_model.py"):
        print("\nERROR: Required files not found.")
        print("Make sure you are running this script from the project root directory.")
        sys.exit(1)
    
    print("\nVirtual environment is active. Proceeding...")
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            print("\nConverting data file...")
            run_command("python convert_data.py")
        elif choice == '2':
            print("\nStarting GUI application...")
            run_command("python spam_detector.py")
        elif choice == '3':
            print("\nStarting command-line test...")
            text = input("Enter email text to analyze (or press Enter to run interactively): ")
            if text:
                run_command(f'python test_model.py "{text}"')
            else:
                run_command("python test_model.py")
        elif choice == '4':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 