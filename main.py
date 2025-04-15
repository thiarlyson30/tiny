from flask import Flask, redirect, request, jsonify
import requests, os

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = "https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/token"
AUTH_URL = "https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth"

@app.route("/")
def home():
    return redirect(f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid&response_type=code")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found", 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=data, headers=headers)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)