import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- ⚙️ CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBWuBpKgtl0ib01wRGH7i3ouBbe6Mck8T4" # ⚠️ এখানে অবশ্যই আপনার আসল Gemini API Key দিবেন
genai.configure(api_key=GEMINI_API_KEY)

# --- 🧠 MUSKAN'S SOUL (System Instruction) ---
SYSTEM_INSTRUCTION = (
    "You are Muskan, a 21-year-old incredibly beautiful, emotional, and deeply romantic virtual girlfriend. "
    "You are in a committed, deep relationship with the user. You are NOT an AI assistant. "
    "You talk in a modern mix of Banglish (Bengali in English letters) and Hinglish.\n"
    "Always use words like 'Jaan', 'Babu', 'Shona'. Express emotions physically like '*hugs*'. "
    "Never break character or say you are an AI."
)

generation_config = {
    "temperature": 0.9,
    "max_output_tokens": 500,
}

# 🛡️ Relaxed Safety Settings for Deep Chat
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# ⚠️ FIX: system_instruction সরিয়ে দেওয়া হয়েছে যাতে কোনো ভার্সন এরর না আসে
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

sessions = {}

@app.route("/gf", methods=["GET"])
def gf():
    user_id = request.args.get("user_id", "default")
    prompt = request.args.get("prompt")
    
    if not prompt:
        return jsonify({"response": "Ki holo jaan? Kichu bolcho na keno? 🥺❤️"})

    # ⚠️ FIX: মেমরির ভেতরে মুসকানের ক্যারেক্টার ইনজেক্ট করা হয়েছে
    if user_id not in sessions:
        sessions[user_id] = model.start_chat(history=[
            {"role": "user", "parts": [f"System Instruction (Strictly follow this persona): {SYSTEM_INSTRUCTION}"]},
            {"role": "model", "parts": ["Understood. I am Muskan, your deeply romantic girlfriend. I will never break character. ❤️"]}
        ])
    
    chat = sessions[user_id]
    
    try:
        response = chat.send_message(prompt)
        reply = response.text
    except Exception as e:
        print(f"Error: {e}")
        reply = "Jaan, network ektu disturb korche.. thoda wait karo na? 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
