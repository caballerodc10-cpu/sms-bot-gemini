from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_reply(incoming_msg):
    try:
        response = model.generate_content(incoming_msg)
        return response.text
    except Exception as e:
        return "Error: " + str(e)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    reply_text = get_gemini_reply(incoming_msg)
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "")
    reply_text = get_gemini_reply(incoming_msg)
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

@app.route("/", methods=["GET"])
def health():
    return "Bot WhatsApp + SMS activo!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
