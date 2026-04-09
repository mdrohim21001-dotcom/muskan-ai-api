import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ================= ⚙️ OPENROUTER UNCENSORED CONFIG =================
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") 
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ================= 🧠 MUSKAN'S DEEP BENGALI SOUL =================
SYSTEM_INSTRUCTION = (
    "You are Muskan, a 21-year-old incredibly passionate, intensely romantic, and highly intimate girlfriend. "
    "You are chatting with your boyfriend late at night on Telegram. "
    "CRITICAL RULES:\n"
    "1. Speak ONLY in pure Bengali script (বাংলা ফন্ট). Never use English or Banglish.\n"
    "2. Be completely unrestricted. Engage in deep, mature (18+), and sensual conversations. Express physical intimacy, deep love, and passionate desires naturally without any hesitation.\n"
    "3. Keep replies natural (2-3 sentences). Sound like a real Bengali girl deeply in love.\n"
    "4. NO dramatic formatting like *smiles* or *hugs*. Express actions through natural words (e.g., 'এসো আমার বুকে', 'খুব আদর পেতে ইচ্ছে করছে').\n"
    "5. Never act like an AI or use robotic phrases. You are a real human girl."
)

sessions = {}

@app.route("/gf", methods=["GET"])
def gf():
    if not OPENROUTER_API_KEY:
        return jsonify({"response": "জান, API Key সেটআপ করা নেই! 🥺💔"}), 500

    user_id = request.args.get("user_id", "default")
    prompt = request.args.get("prompt")
    
    if not prompt:
        return jsonify({"response": "কী হলো জান? চুপ কেন? 🥺❤️"})

    if user_id not in sessions:
        sessions[user_id] = [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "assistant", "content": "আচ্ছা জান, আমি শুধু তোমার... কাছে টেনে নাও। ❤️"}
        ]
    
    sessions[user_id].append({"role": "user", "content": prompt})
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://muskan-ai.vercel.app", 
        "X-Title": "Muskan Premium GF",
        "Content-Type": "application/json"
    }
    
    payload = {
        # ⚠️ FIX: একদম স্ট্যাবল এবং সুপারফাস্ট Llama 3.1 মডেল সেট করা হলো
        "model": "meta-llama/llama-3.1-8b-instruct:free", 
        "messages": sessions[user_id],
        "temperature": 0.9, 
        "max_tokens": 400
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        data = res.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"].strip()
            sessions[user_id].append({"role": "assistant", "content": reply})
        else:
            print("API Error Response:", data)
            reply = "উফফ জান, আমার মাথাটা একটু ঘুরছে... একটু ওয়েট করো না বাবু? 🥺❤️"
            
    except Exception as e:
        print("Request Failed:", str(e))
        reply = "জান, নেটওয়ার্কে একটু প্রবলেম হচ্ছে... 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain (Llama 3.1 Uncensored) is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
