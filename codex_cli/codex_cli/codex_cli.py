import argparse
import datetime
import os
import sys
import time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# === Configuration ===
API_KEY = "AIzaSyCqFBx6oipXXFL8GiY4ongMPzUQiGHtWhE"  # REPLACE with your Gemini 2.0 API Key
MODEL_NAME = "models/gemini-1.5-flash-latest"
LOG_DIR = "logs"
THEME = "dark"  # or "light"
STRATEGY_TEMPLATES = {
    "simple_rsi": "build a simple trading bot using RSI (14)",
    "breakout": "create a python script for breakout trading strategy using Bollinger Bands"
}

# === Setup ===
genai.configure(api_key=API_KEY)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# === Helpers ===
def log_to_file(content):
    filename = f"{LOG_DIR}/codex_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 Output saved to {filename}")

def print_colored(text, mode="info"):
    if THEME == "light":
        colors = {"info": "\033[94m", "success": "\033[92m", "error": "\033[91m", "end": "\033[0m"}
    else:
        colors = {"info": "\033[96m", "success": "\033[92m", "error": "\033[91m", "end": "\033[0m"}
    print(f"{colors.get(mode, '')}{text}{colors['end']}")

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print_colored(f"❌ Error with Gemini API: {e}", "error")
        return "Failed to get a response from Gemini."

def ask_gemini_with_image(image_path, prompt="Describe this image"):
    try:
        image = Image.open(image_path)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        print_colored(f"❌ Error with Gemini Image Input: {e}", "error")
        return "Failed to get a response from Gemini."

# === Modes ===
def default_mode(user_input):
    print_colored("[🔹 DEFAULT MODE] Asking Gemini...", "info")
    answer = ask_gemini(user_input)
    print_colored("\n[✅ RESPONSE]\n" + answer, "success")
    log_to_file(answer)

def fullauto_mode(user_input):
    print_colored("[🤖 FULLAUTO MODE] Generating full solution...", "info")
    prompt = f"Write complete working code with explanation for: {user_input}"
    answer = ask_gemini(prompt)
    print_colored("\n[✅ FULLAUTO RESPONSE]\n" + answer, "success")
    log_to_file(answer)

def explain_mode(user_input):
    print_colored("[📘 EXPLAIN MODE] Explaining code or concept...", "info")
    prompt = f"Explain this code or concept in detail: {user_input}"
    answer = ask_gemini(prompt)
    print_colored("\n[✅ EXPLANATION]\n" + answer, "success")
    log_to_file(answer)

def fix_mode(user_input):
    print_colored("[🛠️ FIX MODE] Trying to fix issues...", "info")
    prompt = f"Fix the bugs in this code: {user_input}"
    answer = ask_gemini(prompt)
    print_colored("\n[✅ FIXED CODE]\n" + answer, "success")
    log_to_file(answer)

def chat_mode():
    print_colored("[💬 CHAT MODE] Start chatting with Gemini! Type 'exit' to stop.", "info")
    chat = genai.GenerativeModel(MODEL_NAME).start_chat()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = chat.send_message(user_input)
        print_colored(f"Gemini: {response.text}\n", "success")

def file_input_mode(filepath):
    if not os.path.isfile(filepath):
        print_colored("File not found.", "error")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    explain_mode(code)

def image_input_mode(image_path):
    print_colored(f"[🖼️ IMAGE MODE] Analyzing image: {image_path}", "info")
    answer = ask_gemini_with_image(image_path)
    print_colored("\n[✅ IMAGE RESPONSE]\n" + answer, "success")
    log_to_file(answer)

# === CLI Interface ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Mode: default, fullauto, explain, fix, chat, file, image")
    parser.add_argument("--input", help="Your prompt, file path, or image path")
    parser.add_argument("--template", help="Use a built-in template", choices=STRATEGY_TEMPLATES.keys())
    args = parser.parse_args()

    if args.template:
        user_input = STRATEGY_TEMPLATES[args.template]
    elif args.input:
        user_input = args.input
    else:
        user_input = input("Enter your prompt: ")

    if args.mode:
        mode = args.mode
    else:
        mode = input("Enter mode [default|fullauto|explain|fix|chat|file|image]: ").lower()

    if mode == "default":
        default_mode(user_input)
    elif mode == "fullauto":
        fullauto_mode(user_input)
    elif mode == "explain":
        explain_mode(user_input)
    elif mode == "fix":
        fix_mode(user_input)
    elif mode == "chat":
        chat_mode()
    elif mode == "file":
        file_input_mode(user_input)
    elif mode == "image":
        image_input_mode(user_input)
    else:
        print_colored("Invalid mode selected.", "error")

if __name__ == "__main__":
    main()
