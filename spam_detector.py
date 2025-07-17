import pandas as pd
import numpy as np
import re
import pickle
import os
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

# Function to detect file format and read accordingly
def read_data_file(file_path):
    """
    Detects file format and reads data accordingly, handling CSV files with incorrect extensions
    """
    print(f"Attempting to read file: {file_path}")
    
    # First check if it's actually a CSV file regardless of extension
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if ',' in first_line and first_line.startswith('Category'):
                print(f"File appears to be a CSV file with header: {first_line}")
                return pd.read_csv(file_path)
    except UnicodeDecodeError:
        print("File is not a plain text CSV file, trying Excel formats...")
    
    # Try different Excel engines
    try:
        print("Trying openpyxl engine...")
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"openpyxl engine failed: {str(e)}")
        
        try:
            print("Trying xlrd engine...")
            return pd.read_excel(file_path, engine='xlrd')
        except Exception as e:
            print(f"xlrd engine failed: {str(e)}")
            
            # Last resort - try reading as CSV with different encodings
            try:
                print("Trying CSV with latin-1 encoding...")
                return pd.read_csv(file_path, encoding='latin-1')
            except Exception as e:
                print(f"CSV with latin-1 encoding failed: {str(e)}")
                raise Exception(f"Could not read file {file_path} in any supported format")

# Download required NLTK resources
def download_nltk_resources():
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        print("NLTK resources downloaded successfully.")
    except Exception as e:
        print(f"Error downloading NLTK resources: {e}")

# Data preprocessing functions
def preprocess_data(df):
    # Convert text to lowercase
    df['message'] = df['message'].str.lower()
    
    # Clean text - remove special characters
    df['message'] = df['message'].apply(lambda x: re.sub("[^'.,a-z0-9 ]+", " ", x))
    
    # Lemmatize text
    lem = WordNetLemmatizer()
    df['message'] = df['message'].apply(lambda x: ' '.join([lem.lemmatize(i, pos='v') for i in x.split()]))
    
    # Remove most frequent and least frequent words
    term_frequency = pd.Series(' '.join(df['message']).split()).value_counts()
    most_freq_words = term_frequency.head(20)
    least_freq_words = term_frequency[term_frequency <= 1]
    
    df['message'] = df['message'].apply(lambda x: ' '.join([word for word in x.split() if word not in most_freq_words]))
    df['message'] = df['message'].apply(lambda x: ' '.join([word for word in x.split() if word not in least_freq_words]))
    
    return df

# Train model function
def train_model(file_path):
    try:
        # Read the dataset using the new function
        df = read_data_file(file_path)
        print(f"Successfully read file with {len(df)} rows and columns: {df.columns.tolist()}")
        
        # Ensure correct column names
        if 'Category' in df.columns and 'Message' in df.columns:
            print("Renaming columns from 'Category'/'Message' to 'spam'/'message'")
            df.columns = ['spam', 'message']
        
        # Preprocess data
        print("Preprocessing data...")
        df = preprocess_data(df)
        
        # Convert categorical labels to binary
        print("Converting labels to binary...")
        df['spam'] = df['spam'].apply(lambda x: 1 if x == 'spam' else 0)
        
        # Split features and target
        x = df['message']
        y = df['spam']
        
        # Split data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
        
        # Vectorize text data
        cv = CountVectorizer()
        x_train_cv = cv.fit_transform(x_train)
        x_test_cv = cv.transform(x_test)
        
        # Train model
        svm = LinearSVC()
        svm.fit(x_train_cv, y_train)
        
        # Evaluate model
        y_pred = svm.predict(x_test_cv)
        report = classification_report(y_test, y_pred)
        print("Model Training Complete")
        print("Classification Report:")
        print(report)
        
        # Save model and vectorizer
        os.makedirs('spam_nlp', exist_ok=True)
        pickle.dump(cv, open('spam_nlp/cv.pkl', 'wb'))
        pickle.dump(svm, open('spam_nlp/svm.pkl', 'wb'))
        
        print("Model and vectorizer saved successfully.")
        return True
        
    except Exception as e:
        print(f"Error training model: {e}")
        return False

# Load model function
def load_model():
    try:
        cv = pickle.load(open('spam_nlp/cv.pkl', 'rb'))
        svm = pickle.load(open('spam_nlp/svm.pkl', 'rb'))
        return cv, svm
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

# GUI Application
class SpamDetectorApp:
    def __init__(self, root):
        self.root = root
        self.cv, self.svm = load_model()
        
        if self.cv is None or self.svm is None:
            messagebox.showerror("Error", "Failed to load model. Please train the model first.")
            self.root.destroy()
            return
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Spam Email Detector")
        
        # Set window size and position
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure colors
        self.root.configure(bg="#F5F5F5")
        
        # Header frame
        header_frame = tk.Frame(self.root, bg="#4285F4", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        # App title
        title_label = tk.Label(header_frame, text="Spam Email Detector", font=("Helvetica", 28, "bold"), bg="#4285F4", fg="white")
        title_label.pack()
        
        # Description label
        desc_label = tk.Label(header_frame, text="Analyze emails using machine learning to detect spam", font=("Helvetica", 14), bg="#4285F4", fg="white")
        desc_label.pack(pady=(5, 0))
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#F5F5F5", padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions label
        instructions_label = tk.Label(content_frame, text="Enter the email text you want to analyze:", font=("Helvetica", 16), bg="#F5F5F5", fg="#333333")
        instructions_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Text input area with scrollbar
        self.text_box = scrolledtext.ScrolledText(content_frame, height=10, font=("Arial", 12), wrap=tk.WORD, padx=10, pady=10)
        self.text_box.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg="#F5F5F5")
        buttons_frame.pack(fill=tk.X)
        
        # Check button
        self.check_button = tk.Button(
            buttons_frame, 
            text="Check Email", 
            command=self.check_spam, 
            font=("Helvetica", 14, "bold"),
            bg="#4285F4", 
            fg="white",
            padx=20, 
            pady=10,
            borderwidth=0,
            cursor="hand2"
        )
        self.check_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_button = tk.Button(
            buttons_frame, 
            text="Clear", 
            command=self.clear_text, 
            font=("Helvetica", 14),
            bg="#9E9E9E", 
            fg="white",
            padx=20, 
            pady=10,
            borderwidth=0,
            cursor="hand2"
        )
        self.clear_button.pack(side=tk.LEFT)
        
        # Result frame
        self.result_frame = tk.Frame(content_frame, bg="#F5F5F5", pady=20)
        self.result_frame.pack(fill=tk.X)
        
        # Result label
        self.result_label = tk.Label(self.result_frame, text="", font=("Helvetica", 16, "bold"), bg="#F5F5F5")
        self.result_label.pack()
        
        # Bind hover effects
        self.check_button.bind("<Enter>", lambda e: self.on_enter(e, self.check_button, "#3367D6"))
        self.check_button.bind("<Leave>", lambda e: self.on_leave(e, self.check_button, "#4285F4"))
        self.clear_button.bind("<Enter>", lambda e: self.on_enter(e, self.clear_button, "#757575"))
        self.clear_button.bind("<Leave>", lambda e: self.on_leave(e, self.clear_button, "#9E9E9E"))
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#E0E0E0", padx=20, pady=10)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_text = tk.Label(
            footer_frame, 
            text="Spam Email Detector | Powered by Machine Learning", 
            font=("Helvetica", 10), 
            bg="#E0E0E0", 
            fg="#757575"
        )
        footer_text.pack()
    
    def on_enter(self, event, button, color):
        button.config(bg=color)
    
    def on_leave(self, event, button, color):
        button.config(bg=color)
    
    def check_spam(self):
        user_text = self.text_box.get("1.0", tk.END).strip()
        
        if not user_text:
            messagebox.showerror("Error", "You didn't type anything. Enter an email to check.")
            return
        
        try:
            # Check if models are loaded properly
            if self.cv is None or self.svm is None:
                messagebox.showerror("Error", "Model not loaded properly. Please restart the application.")
                return
                
            # Transform text using the loaded vectorizer
            text_transformed = self.cv.transform([user_text])
            # Predict using the loaded model
            prediction = self.svm.predict(text_transformed)
            
            # Display result
            self.result_frame.config(bg="#F5F5F5")
            if prediction[0] == 1:
                self.result_label.config(text="Result: This email is SPAM", fg="#D32F2F")
                messagebox.showwarning("Result", "This email has been classified as SPAM.")
            else:
                self.result_label.config(text="Result: This email is NOT spam", fg="#388E3C")
                messagebox.showinfo("Result", "This email has been classified as NOT spam.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_text(self):
        self.text_box.delete("1.0", tk.END)
        self.result_label.config(text="")

# Main function
def main():
    # Check if model files exist, if not train the model
    if not os.path.exists('spam_nlp/cv.pkl') or not os.path.exists('spam_nlp/svm.pkl'):
        print("Model files not found. Training new model...")
        download_nltk_resources()
        
        # Look for the dataset file
        data_file = None
        if os.path.exists('mail_data.csv'):
            data_file = 'mail_data.csv'
            print(f"Found dataset: {data_file}")
        elif os.path.exists('mail_data.xls'):
            data_file = 'mail_data.xls'
            print(f"Found dataset: {data_file}")
        elif os.path.exists('mail_data (1).xls'):
            data_file = 'mail_data (1).xls'
            print(f"Found dataset: {data_file}")
        
        if data_file:
            print(f"Training model using dataset: {data_file}")
            success = train_model(data_file)
            if not success:
                print("Failed to train model. Exiting...")
                return
        else:
            print("Dataset file not found. Please make sure 'mail_data.csv' or 'mail_data.xls' exists.")
            print("Current directory:", os.getcwd())
            print("Files in current directory:", os.listdir())
            return
    
    # Start the GUI application
    print("Starting GUI application...")
    root = tk.Tk()
    app = SpamDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 