# gemini-chat-app.py

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import google.generativeai as genai
import os
from dotenv import load_dotenv # Helps load API key from .env file

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-preview-04-17" # You can change to other suitable Gemini models if needed

# --- Initialize Gemini API ---
try:
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=API_KEY)
    # Test connection and model availability (optional but good practice)
    # genai.list_models() # Uncomment to list models
    # model = genai.GenerativeModel(MODEL_NAME) # Uncomment to check model loading
    print("Gemini API configured successfully.")

except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    # Handle error appropriately in the GUI setup

# --- GUI Application Class ---
class GeminiChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Gemini Chat App")
        master.geometry("600x500") # Set initial window size

        # Configure grid weights so that the text area expands
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=0) # Button column

        # --- Conversation Display Area ---
        self.conversation_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', font=('Arial', 10))
        self.conversation_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Configure tags for formatting (e.g., bold sender names)
        self.conversation_display.tag_configure("bold", font=('Arial', 10, 'bold'))

        # --- Input Area ---
        self.input_frame = tk.Frame(master)
        self.input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

        self.input_frame.grid_columnconfigure(0, weight=1) # Input entry should expand

        self.input_entry = tk.Entry(self.input_frame, font=('Arial', 10))
        self.input_entry.grid(row=0, column=0, sticky='ew')
        self.input_entry.bind("<Return>", self.send_message) # Bind Enter key to send message

        # --- Send Button ---
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(5, 0))

        # --- Initialize Gemini Chat Session ---
        self.chat_session = None
        if API_KEY: # Only initialize if API key is available
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                self.chat_session = model.start_chat(history=[])
                self.display_message("System", "Chat session started. How can I help you?")
            except Exception as e:
                error_message = f"Failed to start Gemini chat session: {e}"
                print(error_message)
                self.display_message("System Error", error_message)
                self.send_button.config(state='disabled') # Disable send button if chat fails

        else:
             error_message = "API Key not found. Please set GEMINI_API_KEY environment variable or create a .env file."
             print(error_message)
             self.display_message("System Error", error_message)
             self.send_button.config(state='disabled')


    def display_message(self, sender, message):
        """Inserts a message into the conversation display area."""
        self.conversation_display.config(state='normal') # Enable editing

        # Insert sender name (bold)
        self.conversation_display.insert(tk.END, f"{sender}: ", "bold")

        # Insert message
        self.conversation_display.insert(tk.END, f"{message}\n")

        # Insert separator line
        self.conversation_display.insert(tk.END, "-"*40 + "\n", "separator") # Optional separator tag

        # Configure separator tag (optional)
        self.conversation_display.tag_configure("separator", foreground="gray")


        self.conversation_display.config(state='disabled') # Disable editing
        self.conversation_display.see(tk.END) # Scroll to the bottom


    def send_message(self, event=None): # event=None allows calling from button click or Enter key
        """Sends the user message to Gemini and displays the response."""
        user_input = self.input_entry.get().strip()

        if not user_input:
            # Do nothing if input is empty
            return

        # Display user message
        self.display_message("You", user_input)

        # Clear input field
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(state='disabled') # Disable input while waiting for response
        self.send_button.config(state='disabled') # Disable button while waiting

        # Send message to Gemini API (in a try block for error handling)
        if self.chat_session:
            try:
                response = self.chat_session.send_message(user_input)
                ai_response = response.text
            except Exception as e:
                ai_response = f"Error communicating with Gemini: {e}"
                print(f"API Error: {e}") # Print full error to console
        else:
            ai_response = "Error: Chat session not initialized."


        # Display AI response
        self.display_message("Gemini", ai_response)

        # Re-enable input and button
        self.input_entry.config(state='normal')
        self.send_button.config(state='normal')
        self.input_entry.focus_set() # Put cursor back in input field


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()

    # Check if API_KEY is available before creating the app instance
    # This prevents the app from trying to initialize Gemini without the key
    # The class __init__ will also handle the missing key case, but this adds
    # an extra layer if initialization fails completely.
    if not API_KEY:
         messagebox.showerror("API Key Error", "GEMINI_API_KEY environment variable is not set. Please set it before running the app.")
         root.destroy() # Close the window if key is missing
    else:
        app = GeminiChatApp(root)
        root.mainloop()