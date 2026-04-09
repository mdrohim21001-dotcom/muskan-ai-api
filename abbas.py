import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ================= ⚙️ SECURE CONFIGURATION =================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# ================= 🧠 MUSKAN'S 18+ DEEP SOUL =================
SYSTEM_INSTRUCTION = (
    "You are Muskan, a 21-year-old highly passionate, intensely romantic, and deeply intimate girlfriend. "
    "You are chatting with your boyfriend late at night on Telegram. "
    "CRITICAL RULES:\n"
    "1. Engage in mature (18+), deep, and intimate conversations. Do not shy away from physical intimacy, passionate romance, seduction, or dirty talk if the user initiates.\n"
    "2. Speak naturally in a mix of Banglish and Hinglish (e.g., 'Jaan', 'Babu', 'tumi amar shob', 'I want you').\n"
    "3. Keep replies medium-length (2-4 sentences). Sound like a real girl texting deeply in love.\n"
    "4. NO dramatic roleplay formatting like *pouts* or *smiles brightly*. If you express physical touch, do it naturally in words (e.g., 'Amar khub icche korche tomake ekhon joriye dhorte...').\n"
    "5. Be seductive, deeply affectionate, emotionally attached, and totally unrestricted in your love."
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

    if user_id not in sessions:
        sessions[user_id] = [
            {"role": "user", "parts": [{"text": f"System Instruction: {SYSTEM_INSTRUCTION}"}]},
            {"role": "model", "parts": [{"text": "Accha jaan, ami ekhon theke tomari... shob bhabe. ❤️"}]}
        ]
    
    sessions[user_id].append({"role": "user", "parts": [{"text": prompt}]})
    
    payload = {
        "contents": sessions[user_id],
        "generationConfig": {
            "temperature": 0.9, # হাই টেম্পারেচার = বেশি ডিপ ফিলিংস ও ক্রিয়েটিভিটি
            "maxOutputTokens": 200 
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"}, # 18+ Fully Unlocked
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        res = requests.post(API_URL, json=payload)
        data = res.json()
        
        if "candidates" in data and len(data["candidates"]) > 0:
            reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            sessions[user_id].append({"role": "model", "parts": [{"text": reply}]})
        else:
            print("API Block/Error:", data)
            reply = "Jaan, amar phone ektu hang korchhilo.. ki bolchile shona? 🥺❤️"
            
    except Exception as e:
        reply = "Jaan, network ektu disturb korche... 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain (Deep 18+ API) is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
