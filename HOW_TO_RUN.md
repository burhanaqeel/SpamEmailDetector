# How to Run the Spam Email Detector

This guide provides step-by-step instructions on how to set up and run the Spam Email Detector project using the command line.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.7 or higher
- pip package manager

## Installation Steps

1. **Clone or download the repository**

   If you downloaded a ZIP file, extract it to a folder of your choice.

2. **Open a terminal or command prompt**

   Navigate to the project directory:

   ```bash
   cd path/to/spam-email-detector
   ```

3. **Create a virtual environment**

   ```bash
   # Create a new virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

   You'll know the virtual environment is activated when you see `(venv)` at the beginning of your command prompt.

   > **IMPORTANT**: The virtual environment **MUST** be activated before running any scripts in this project. All scripts will check for this and refuse to run if the virtual environment is not active.

4. **Install the required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the necessary Python libraries including pandas, numpy, scikit-learn, nltk, etc.

## Running the Application

### Quick Start with the Runner Script

The easiest way to run the application is using the provided runner script:

```bash
python run.py
```

This will display a menu with options to:
1. Convert the data file
2. Run the GUI application
3. Run the command-line test
4. Exit

The script will check if you're running in a virtual environment and will refuse to run if it's not activated.

### Step 1: Convert the Data File

The first time you run the application, you need to convert the data file to the proper format:

```bash
python convert_data.py
```

This will:
- Detect the data file format
- Convert it to a proper CSV format
- Save it as `mail_data.csv`

### Step 2: Run the Application

#### Option 1: GUI Application

To run the application with a graphical user interface:

```bash
python spam_detector.py
```

The first time you run this, it will:
- Download necessary NLTK resources
- Train the model using the provided dataset
- Save the trained model to the spam_nlp directory
- Launch the graphical user interface

#### Option 2: Command Line Testing

For quick testing from the command line:

```bash
python test_model.py "Your email text to analyze here"
```

Or run without arguments to enter text interactively:

```bash
python test_model.py
```

## Sample Emails for Testing

Here are some sample emails you can use to test the classifier:

### Likely Spam Examples:

```
URGENT! You have won a 1 week FREE membership in our £100,000 Prize Jackpot! Txt the word: CLAIM to No: 81010
```

```
Congratulations! You've been selected to receive a $1000 Walmart gift card. Click here to claim now: http://claim-your-prize.com
```

### Likely Non-Spam Examples:

```
Hi John, just checking if we're still on for lunch tomorrow at 12:30? Let me know if you need to reschedule. Thanks!
```

```
Your monthly account statement is now available. Please log in to your online banking to view the details. If you have any questions, contact customer service.
```

## Troubleshooting

If you encounter any issues:

1. **Virtual environment errors**
   - Make sure the virtual environment is activated before running any scripts
   - You should see `(venv)` at the beginning of your command prompt

2. **Model not found errors**
   - Make sure you've run `spam_detector.py` at least once to train and save the model

3. **Import errors**
   - Verify that you've installed all dependencies with `pip install -r requirements.txt`
   - Try installing the specific missing package, e.g., `pip install pandas`

4. **File not found errors**
   - Ensure you're running the commands from the project's root directory
   - Check that the dataset file `mail_data.csv` exists in the project directory

5. **NLTK resource errors**
   - If you see errors about missing NLTK resources, run the following in a Python shell:
     ```python
     import nltk
     nltk.download('stopwords')
     nltk.download('punkt')
     nltk.download('wordnet')
     nltk.download('omw-1.4')
     ```