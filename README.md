# 📧 Spam Email Detector

<div align="center">
  
  ![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
  ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-NLP-green.svg)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)
  
  <img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="400">
  
  **A powerful machine learning application to detect spam emails using Natural Language Processing**

</div>

## 🌟 Features

- **🤖 Machine Learning** - Uses Support Vector Classification to detect spam with high accuracy
- **📊 NLP Processing** - Advanced text preprocessing including tokenization, lemmatization, and stopword removal
- **🎨 Modern UI** - Clean, intuitive interface built with Tkinter
- **⚡ Real-time Analysis** - Instant classification of email text
- **🔄 Retrainable Model** - Can be retrained with new data to improve accuracy

## 📋 Table of Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/burhanaqeel/SpamEmailDetector.git
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

   > **IMPORTANT**: The virtual environment **MUST** be activated before running any scripts in this project. All scripts will check for this and refuse to run if the virtual environment is not active.

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Quick Start

The easiest way to run the application is using the provided runner script:

```bash
python run.py
```

This will display a menu with options to:
1. Convert the data file
2. Run the GUI application
3. Run the command-line test
4. Exit

### Data Preparation

Before running the application for the first time, convert the data file to the proper format:

```bash
python convert_data.py
```

### GUI Application

Run the main application with a graphical user interface:

```bash
python spam_detector.py
```

### Command Line Testing

For quick testing from the command line:

```bash
python test_model.py "Your email text to analyze here"
```

Or run without arguments to enter text interactively:

```bash
python test_model.py
```

## 🔍 How It Works

### Data Preprocessing

1. **Text Cleaning** - Removes special characters and converts text to lowercase
2. **Tokenization** - Breaks text into individual words
3. **Lemmatization** - Reduces words to their base form (e.g., "running" → "run")
4. **Stopword Removal** - Eliminates common words that don't add meaning

### Machine Learning Model

The application uses a Linear Support Vector Classifier (LinearSVC) to classify emails. This model:

- Is trained on a dataset of 5,000+ labeled emails
- Uses a bag-of-words approach with CountVectorizer
- Achieves high precision and recall for spam detection

## 📁 Project Structure

```
spam-email-detector/
├── spam_detector.py        # Main application file with GUI
├── test_model.py           # Command-line test tool
├── convert_data.py         # Data conversion utility
├── run.py                  # Runner script with menu interface
├── cleanup.py              # Project cleanup utility
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── HOW_TO_RUN.md           # Detailed instructions
├── .gitignore              # Git ignore file
├── mail_data.csv           # Dataset in CSV format
└── spam_nlp/               # Directory for saved models
    ├── cv.pkl              # Saved CountVectorizer
    └── svm.pkl             # Saved SVM model
```

## 🛠️ Technologies Used

- **Python** - Core programming language
- **scikit-learn** - Machine learning library for the SVM model
- **NLTK** - Natural Language Toolkit for text processing
- **Pandas** - Data manipulation and analysis
- **Tkinter** - GUI framework

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>Developed with ❤️ by <a href="https://github.com/burhanaqeel">Burhan Aqeel</a></p>
  <p>Star ⭐ this repository if you find it useful!</p>
</div>
