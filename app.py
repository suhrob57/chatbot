from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Xabar bo'sh!"}), 400

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        
        if response.status_code == 200:
            return jsonify({"reply": response.json()["choices"][0]["message"]["content"]})
        else:
            return jsonify({"error": f"API xatosi: {response.text}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server xatosi: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
