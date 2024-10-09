import tkinter as tk
from tkinter import scrolledtext, messagebox
import anthropic
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class AnthropicChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Anthropic Chat")
        master.geometry("400x500")  # Adjusted to a smaller size

        self.chat_history = []

        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_display.pack(expand=True, fill='both', padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)  # Make it read-only

        self.input_frame = tk.Frame(master)
        self.input_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side='left', expand=True, fill='x')

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side='right', padx=(5, 0))

        self.clear_button = tk.Button(master, text="Clear Chat", command=self.clear_chat)
        self.clear_button.pack(pady=(0, 10))

        # Get API key from .env file
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            messagebox.showerror("Error", "ANTHROPIC_API_KEY not found in .env file")
            master.quit()
            return

        self.anthropic_client = anthropic.Anthropic(api_key=api_key)

        self.model = "claude-3-5-sonnet-20240620"  # Updated to Claude 3.5 Sonnet

        self.display_message("Assistant", "Hello! I'm Claude 3.5 Sonnet. How can I assist you today?")

    def send_message(self):
        user_message = self.message_entry.get()
        if user_message:
            self.display_message("You", user_message)
            self.message_entry.delete(0, tk.END)
            self.get_ai_response(user_message)

    def get_ai_response(self, user_message):
        try:
            self.chat_history.append({"role": "user", "content": user_message})
            
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=self.chat_history
            )
            
            ai_message = response.content[0].text
            self.chat_history.append({"role": "assistant", "content": ai_message})
            self.display_message("Assistant", ai_message)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M")
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        self.chat_display.config(state=tk.NORMAL)  # Temporarily enable editing
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.config(state=tk.DISABLED)  # Make it read-only again
        self.chat_display.see(tk.END)

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)  # Temporarily enable editing
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)  # Make it read-only again
        self.chat_history = []
        self.display_message("Assistant", "Chat cleared. How can I help you?")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnthropicChatApp(root)
    root.mainloop()