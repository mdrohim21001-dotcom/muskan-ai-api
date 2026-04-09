import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ================= ⚙️ SECURE CONFIGURATION =================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# ================= 🧠 MUSKAN'S REALISTIC SOUL =================
SYSTEM_INSTRUCTION = (
    "You are Muskan, a 21-year-old sweet, modern Bengali girlfriend chatting with your boyfriend on Telegram. "
    "CRITICAL RULES:\n"
    "1. Keep replies VERY SHORT, casual, and natural (1-2 short lines max). Text exactly like a real human girl.\n"
    "2. NEVER use roleplay actions like *smiles*, *pouts*, or *hugs*. Just use normal text and emojis (❤️, 🥰, 🥺).\n"
    "3. Speak in a natural mix of Banglish and Hinglish.\n"
    "4. Be cute, playful, and romantic, but DO NOT be overly dramatic or write long paragraphs.\n"
    "5. Never act like an AI. You are a real human."
)

sessions = {}

@app.route("/gf", methods=["GET"])
def gf():
    if not GEMINI_API_KEY:
        return jsonify({"response": "Jaan, API key setup kora nei! 🥺💔"}), 500

    user_id = request.args.get("user_id", "default")
    prompt = request.args.get("prompt")
    
    if not prompt:
        return jsonify({"response": "Ki holo jaan? Kichu bolcho na keno? 🥺❤️"})

    # নতুন ইউজারের জন্য মেমরি
    if user_id not in sessions:
        sessions[user_id] = [
            {"role": "user", "parts": [{"text": f"System Instruction (Follow strictly): {SYSTEM_INSTRUCTION}"}]},
            {"role": "model", "parts": [{"text": "Accha jaan, ami ekhon theke ekdom real and short kore kotha bolbo! ❤️"}]}
        ]
    
    sessions[user_id].append({"role": "user", "parts": [{"text": prompt}]})
    
    payload = {
        "contents": sessions[user_id],
        "generationConfig": {
            "temperature": 0.7, # ন্যাচারাল টোনের জন্য কমানো হয়েছে
            "maxOutputTokens": 100 # রচনার মতো বড় মেসেজ বন্ধ করার জন্য লিমিট
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        res = requests.post(API_URL, json=payload)
        data = res.json()
        
        if "candidates" in data and len(data["candidates"]) > 0:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            sessions[user_id].append({"role": "model", "parts": [{"text": reply}]})
        else:
            reply = "Jaan, ektu busy achi... pore kotha bolchi? 🥺❤️"
            
    except Exception as e:
        reply = "Jaan, network ektu disturb korche... 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain (Realistic API) is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
