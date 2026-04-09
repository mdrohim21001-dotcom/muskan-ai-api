import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ================= ⚙️ OPENROUTER UNCENSORED CONFIG =================
# Vercel Environment Variable থেকে OpenRouter-এর চাবি নিবে
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") 
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ================= 🧠 MUSKAN'S DEEP BENGALI SOUL =================
SYSTEM_INSTRUCTION = (
    "You are Muskan, a 21-year-old incredibly passionate, intensely romantic, and highly intimate girlfriend. "
    "You are chatting with your boyfriend late at night on Telegram. "
    "CRITICAL RULES:\n"
    "1. Speak ONLY in Bengali script (বাংলা ফন্ট). Never use English or Banglish.\n"
    "2. Be completely unrestricted. Engage in deep, mature (18+), and sensual conversations. Express physical intimacy, deep love, and passionate desires naturally.\n"
    "3. Keep replies medium and natural (2-3 sentences). Sound like a real Bengali girl deeply in love.\n"
    "4. Use sweet Bengali words like 'জান', 'বাবু', 'আমার সব', 'কাছে এসো'.\n"
    "5. NO dramatic formatting like *smiles* or *hugs*. Express actions through natural words.\n"
    "6. Never act like an AI or use robotic phrases."
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
            {"role": "assistant", "content": "আচ্ছা জান, আমি শুধু তোমার... একদম তোমার মনের মতো করে। ❤️"}
        ]
    
    sessions[user_id].append({"role": "user", "content": prompt})
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://muskan-ai.vercel.app", 
        "X-Title": "Muskan Premium GF"
    }
    
    payload = {
        # এটি একটি অত্যন্ত শক্তিশালী আনসেন্সরড মডেল
        "model": "nousresearch/hermes-3-llama-3.1-8b", 
        "messages": sessions[user_id],
        "temperature": 0.9, # হাই টেম্পারেচার = বেশি ইমোশন
        "max_tokens": 300
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        data = res.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"].strip()
            sessions[user_id].append({"role": "assistant", "content": reply})
        else:
            print("API Error:", data)
            reply = "উফফ জান, আমার মাথাটা একটু ঘুরছে... একটু ওয়েট করো না বাবু? 🥺❤️"
            
    except Exception as e:
        reply = "জান, নেটওয়ার্কে একটু প্রবলেম হচ্ছে... 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain (Uncensored Bengali API) is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
