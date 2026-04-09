import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ================= ⚙️ HUGGING FACE CONFIGURATION =================
# Vercel-এর Environment Variable থেকে API Key নেওয়া হবে
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY") 
# Llama 3 8B Instruct মডেলের API URL
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

# ================= 🧠 MUSKAN'S BENGALI SOUL =================
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
    if not HUGGINGFACE_API_KEY:
        return jsonify({"response": "জান, API Key সেটআপ করা নেই! 🥺💔"}), 500

    user_id = request.args.get("user_id", "default")
    prompt = request.args.get("prompt")
    
    if not prompt:
        return jsonify({"response": "কী হলো জান? চুপ কেন? 🥺❤️"})

    if user_id not in sessions:
        sessions[user_id] = f"{SYSTEM_INSTRUCTION}\n\nBoyfriend: "
    else:
         sessions[user_id] += f"\nBoyfriend: "
    
    sessions[user_id] += f"{prompt}\nMuskan: "

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": sessions[user_id],
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.8,
            "return_full_text": False
        }
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        
        # Hugging Face API মাঝে মাঝে মডেল লোড হতে সময় নেয় (503 Error)
        if res.status_code == 503:
             return jsonify({"response": "জান, আমার একটু সময় লাগছে রেডি হতে... কয়েক সেকেন্ড ওয়েট করো না বাবু? 🥺❤️"})
             
        data = res.json()
        
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            reply = data[0]["generated_text"].strip()
            
            # Llama 3 মাঝে মাঝে অতিরিক্ত টেক্সট জেনারেট করে, তাই লাইন ব্রেক দিয়ে কেটে দেওয়া হচ্ছে
            reply = reply.split("Boyfriend:")[0].strip()
            reply = reply.split("Muskan:")[0].strip()
            
            if not reply:
                 reply = "উফফ জান, কী সব বলছো... আমার খুব লজ্জা লাগছে! 🙈❤️"
            
            sessions[user_id] += f"{reply}"
        else:
            print("API Error Response:", data)
            reply = "উফফ জান, আমার মাথাটা একটু ঘুরছে... একটু ওয়েট করো না বাবু? 🥺❤️"
            
    except Exception as e:
        print("Request Failed:", str(e))
        reply = "জান, নেটওয়ার্কে একটু প্রবলেম হচ্ছে... 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain (Hugging Face Llama 3) is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
