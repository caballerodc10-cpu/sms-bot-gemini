from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests as http_requests
import json

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def get_gemini_reply(incoming_msg):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": incoming_msg}]}]
        }
        resp = http_requests.post(url, json=payload, timeout=30)
        print(f"Gemini status: {resp.status_code}, body: {resp.text[:300]}")
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error Gemini {resp.status_code}: {resp.text[:150]}"
    except Exception as e:
        print(f"Exception: {e}")
        return "Error: " + str(e)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    print(f"SMS: {incoming_msg}")
    resp = MessagingResponse()
    resp.message(get_gemini_reply(incoming_msg))
    return str(resp)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "")
    print(f"WA received: {incoming_msg}")
    reply = get_gemini_reply(incoming_msg)
    print(f"WA reply: {reply[:100]}")
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
