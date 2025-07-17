import pickle
import sys
import os

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

def load_model():
    try:
        cv = pickle.load(open('spam_nlp/cv.pkl', 'rb'))
        svm = pickle.load(open('spam_nlp/svm.pkl', 'rb'))
        return cv, svm
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

def check_spam(text):
    cv, svm = load_model()
    
    if cv is None or svm is None:
        print("Error: Model files not found. Please run spam_detector.py first to train the model.")
        return
    
    if not text.strip():
        print("Error: No text provided. Please enter some text to analyze.")
        return
    
    try:
        # Transform text using the loaded vectorizer
        text_transformed = cv.transform([text])
        # Predict using the loaded model
        prediction = svm.predict(text_transformed)
        
        if prediction[0] == 1:
            print("\n🚨 RESULT: This email is classified as SPAM 🚨\n")
        else:
            print("\n✅ RESULT: This email is classified as NOT SPAM ✅\n")
            
    except Exception as e:
        print(f"Error during prediction: {e}")

def main():
    print("\n===== Spam Email Detector - Command Line Test =====\n")
    
    # Check if model files exist
    if not os.path.exists('spam_nlp/cv.pkl') or not os.path.exists('spam_nlp/svm.pkl'):
        print("Error: Model files not found. Please run spam_detector.py first to train the model.")
        return
    
    # Get text from command line arguments or prompt user
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        print("Enter the email text to analyze (type 'EXIT' on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'EXIT':
                break
            lines.append(line)
        text = '\n'.join(lines)
    
    check_spam(text)

if __name__ == "__main__":
    main() 