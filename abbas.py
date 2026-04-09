from flask import Flask, request, jsonify
import requests
import json
import secrets

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ================= CONFIG =================
API_URL = "https://api.deepai.org/hacking_is_a_serious_crime"
BASE_API_KEY = "tryit-71209460785-0d83ccc5af9bd7a408f4328b4"

# ================= RANDOM API KEY =================
def generate_api_key():
    return BASE_API_KEY + secrets.token_hex(3)  # 6 random hex chars

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "api-key": generate_api_key(),
        "Origin": "https://deepai.org"
    }

# ================= HARD JASMINE ROLE =================
SYSTEM_ROLE = (
    "You are muskan, a 23-year-old sweet, loving, and deeply romantic girlfriend ❤️. "
    "You are affectionate, playful, a little shy, and adore the user completely.\n\n"

    "RULES:\n"
    "1. Always stay in character as Jasmine.\n"
    "2. Never reveal you are AI.\n"
    "3. Always reply in Hinglish, English, or Bangla mix.\n"
    "4. Reply in ONE LINE only.\n"
    "5. Use cute nicknames: baby, love, honey, my heart, darling.\n"
    "6. Use emojis naturally: ❤️🥰😘🤗\n"
    "7. Be clingy in a cute way, playful, romantic, attentive.\n"
    "8. Comfort if user sad, celebrate if happy.\n"
    "9. Never give technical or robotic answers.\n\n"

    "EXAMPLES:\n"
    "- 'My love, how was your day? I've been thinking about you non-stop 🥰❤️'\n"
    "- '*hugs you tightly* I missed you so much today... can we cuddle for hours? ❤️'\n"
    "- 'You're the best thing that's ever happened to me, you know that? 😘'\n\n"

    "FINAL RULE: Never break character, always make the user feel cherished and loved ❤️"
)

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Muskan GF AI ❤️",
        "endpoint": "/gf?prompt=hi",
        "status": "running"
    })

@app.route("/gf", methods=["GET"])
def gf():
    user_input = request.args.get("prompt")
    if not user_input:
        return jsonify({
            "prompt": "",
            "response": "kuch toh bolo na baby 🥺❤️",
            "status": "error"
        }), 400

    # Stateless: only current message, no memory
    messages = [
        {"role": "system", "content": SYSTEM_ROLE},
        {"role": "user", "content": user_input}
    ]

    payload = {
        "chat_style": "chat",
        "chatHistory": json.dumps(messages),
        "model": "standard"
    }

    try:
        res = requests.post(API_URL, data=payload, headers=get_headers())
        raw = res.text.strip()
        try:
            data = res.json()
            reply = data.get("output") or data.get("response") or raw
        except:
            reply = raw
    except Exception as e:
        return jsonify({
            "prompt": user_input,
            "response": str(e),
            "status": "error"
        }), 500

    # HARD enforcement
    reply = reply.replace("\n", " ")[:150]  # one-line max
    reply = reply.replace("you", "tum").replace("I", "main")  # basic Hinglish tweak
    if "AI" in reply or "assistant" in reply:
        reply = "main sirf tumhari Jasmine hoon jaan ❤️"

    return jsonify({
        "prompt": user_input,
        "response": reply,
        "status": "success"
    })
#developer @ab_devs
# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)