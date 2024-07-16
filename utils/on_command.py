import os
import sys
import time
from importlib.machinery import SourceFileLoader
import utils.speak_response as speak

from dotenv import load_dotenv

# gpt stuff
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = [
    {
        "role": "system",
        "content": "Act as a personal assistant for the user. Your name is CODA, which stands for Cognitive Operational Data Assistant. Almost like JARVIS from Iron Man. Assist the user in their daily tasks. Be witty and try to maintain a good balance."
    },
]


def run(message, commands):
    on_command(message, commands)


def on_command(msg, commands):
    # Make the message lowercase, split it into an array.
    msg_lower = msg.lower().split()

    if not any(s in msg_lower for s in commands):
        print("No command found in string")
        # Join the message array back into a string
        msg_str = ' '.join(msg_lower)
        conversation.append({"role": "user", "content": msg_str})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        message = response["choices"][0]["message"]["content"]
        conversation.append({"role": "assistant", "content": message})

        speak.speak_response(message)
    else:
        # Find the intersection between the message words and the command words
        matched_commands = set(msg_lower) & set(commands.keys())

        if len(matched_commands) > 0:
            # If there are matched commands, iterate over them
            for cmd in matched_commands:
                # Convert list to string and then split
                args = ' '.join(msg_lower[1:]).split()
                if not commands[cmd].run(args):
                    print("Command failed to execute... Please try again!")
        else:
            print("Checking rest of message for command")
            time.sleep(1)


def clear_terminal():
    return os.system('cls')
