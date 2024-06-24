import openai
import os
import time
import numpy as np
from prompts import (system_prompt_1, system_prompt_2, system_prompt_3,
                     greeting_prompt, special_prompt)

# Ensure API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable in app.yaml.")

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatBot:
    def __init__(self):
        self.session = None
        self.messages = [
            {"role": "system", "content": system_prompt_2},
            {"role": "assistant", "content": greeting_prompt}
        ]

    def user_input(self, user_input):
        """Appends user input to the message history."""
        self.messages.append({"role": "user", "content": user_input})

    def reminder(self, reminder):
        """Appends a system reminder to the message history."""
        self.messages.append({"role": "system", "content": reminder})

    def set_messages(self, messages):
        """Sets the entire message history."""
        self.messages = messages

    def run_bot(self):
        """Runs the bot and returns the response."""
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.messages
            )
            chat_response = completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": chat_response})
            return chat_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, there was an error processing your request."
