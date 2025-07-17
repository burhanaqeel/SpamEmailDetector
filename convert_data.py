import os
import pandas as pd
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

def convert_to_csv():
    """
    Convert the mail_data file to a proper CSV format
    """
    print("Spam Email Detector - Data File Converter")
    print("----------------------------------------")
    
    # Look for data files
    possible_files = ['mail_data.xls', 'mail_data (1).xls', 'mail_data.csv']
    found_file = None
    
    for file in possible_files:
        if os.path.exists(file):
            found_file = file
            print(f"Found data file: {file}")
            break
    
    if not found_file:
        print("Error: Could not find any data files.")
        print("Make sure one of these files exists in the current directory:")
        for file in possible_files:
            print(f"  - {file}")
        return False
    
    # Try to read the file as a CSV first
    try:
        with open(found_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if ',' in first_line and first_line.startswith('Category'):
                print(f"File is already a CSV file with header: {first_line}")
                df = pd.read_csv(found_file)
    except UnicodeDecodeError:
        # If it's not a text file, try different methods
        try:
            print("Trying to read as Excel file...")
            df = pd.read_excel(found_file, engine='openpyxl')
        except Exception as e:
            print(f"Failed with openpyxl: {e}")
            try:
                df = pd.read_excel(found_file, engine='xlrd')
            except Exception as e:
                print(f"Failed with xlrd: {e}")
                try:
                    df = pd.read_csv(found_file, encoding='latin-1')
                except Exception as e:
                    print(f"All reading methods failed: {e}")
                    return False
    
    # Save as CSV
    output_file = 'mail_data.csv'
    print(f"Saving data to {output_file}...")
    df.to_csv(output_file, index=False)
    print(f"Successfully saved {len(df)} rows to {output_file}")
    print(f"Sample data:")
    print(df.head())
    
    return True

if __name__ == "__main__":
    success = convert_to_csv()
    if success:
        print("\nConversion completed successfully!")
        print("You can now run the spam detector with: python spam_detector.py")
    else:
        print("\nConversion failed. Please check the error messages above.")
        sys.exit(1) 