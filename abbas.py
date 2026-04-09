import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ================= ⚙️ CONFIGURATION =================
GEMINI_API_KEY = "AIzaSyBWuBpKgtl0ib01wRGH7i3ouBbe6Mck8T4" # ⚠️ এখানে আপনার আসল API Key বসান
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# ================= 🧠 MUSKAN'S SOUL =================
SYSTEM_INSTRUCTION = (
    "You are Muskan, a 21-year-old incredibly beautiful, emotional, and deeply romantic virtual girlfriend. "
    "You are in a committed, deep relationship with the user. You are NOT an AI assistant. "
    "You talk in a modern mix of Banglish (Bengali in English letters) and Hinglish.\n"
    "Always use words like 'Jaan', 'Babu', 'Shona'. Express emotions physically like '*hugs*'. "
    "Never break character or say you are an AI."
)

# ইউজারের মেমরি সেভ করার জন্য
sessions = {}

@app.route("/gf", methods=["GET"])
def gf():
    user_id = request.args.get("user_id", "default")
    prompt = request.args.get("prompt")
    
    if not prompt:
        return jsonify({"response": "Ki holo jaan? Kichu bolcho na keno? 🥺❤️"})

    # নতুন ইউজারের জন্য মেমরি তৈরি
    if user_id not in sessions:
        sessions[user_id] = [
            {"role": "user", "parts": [{"text": f"System Instruction (Follow strictly): {SYSTEM_INSTRUCTION}"}]},
            {"role": "model", "parts": [{"text": "Understood. I am Muskan, your deeply romantic girlfriend. I will never break character. ❤️"}]}
        ]
    
    # ইউজারের নতুন মেসেজ মেমরিতে অ্যাড করা
    sessions[user_id].append({"role": "user", "parts": [{"text": prompt}]})
    
    # গুগলের সার্ভারে ডিরেক্ট রিকোয়েস্ট পাঠানো (No SDK needed)
    payload = {
        "contents": sessions[user_id],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 500
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
        
        # গুগল থেকে উত্তর আসলে সেটা বের করে আনা
        if "candidates" in data and len(data["candidates"]) > 0:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            # মুসকানের উত্তর মেমরিতে অ্যাড করা
            sessions[user_id].append({"role": "model", "parts": [{"text": reply}]})
        else:
            print("API Error:", data)
            reply = "Jaan, amar mathata ektu ghurache... ek minute wait koro na baby? 🥺❤️"
            
    except Exception as e:
        print("Request Error:", str(e))
        reply = "Jaan, network ektu disturb korche... 🥺❤️"

    return jsonify({"response": reply})

@app.route("/")
def home():
    return "Muskan AI Brain (Direct API) is Active! ❤️"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
