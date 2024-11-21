import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Listening", "Please say a math expression (e.g., 'two plus two')...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            expression_label.config(text=f"Expression: {text}")
            return text
        except sr.UnknownValueError:
            messagebox.showwarning("Warning", "Could not understand the audio.")
            return None
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results; check your internet connection.")
            return None

def parse_and_calculate(expression):
    # Basic parsing for common math terms
    expression = expression.lower()
    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("times", "*")
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("divided by", "/")
    
    try:
        # Evaluate the parsed expression
        result = eval(expression)
        return result
    except Exception as e:
        messagebox.showerror("Error", f"Error evaluating expression: {e}")
        return None

def calculate_from_speech():
    spoken_text = recognize_speech()
    if spoken_text:
        result = parse_and_calculate(spoken_text)
        if result is not None:
            result_label.config(text=f"Result: {result}")
        else:
            result_label.config(text="Result: Error")

# Setup Tkinter UI
root = tk.Tk()
root.title("Voice Calculator")

# Instructions Label
instructions = tk.Label(root, text="Press 'Speak' to say a math expression")
instructions.pack(pady=10)

# Expression Label
expression_label = tk.Label(root, text="Expression: ")
expression_label.pack(pady=5)

# Result Label
result_label = tk.Label(root, text="Result: ")
result_label.pack(pady=5)

# Speak Button
speak_button = tk.Button(root, text="Speak", command=calculate_from_speech)
speak_button.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=5)

# Run the application
root.mainloop()
