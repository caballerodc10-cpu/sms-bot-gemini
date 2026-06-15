from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def get_gemini_reply(incoming_msg):
    try:
        response = model.generate_content(incoming_msg)
        return response.text
    except Exception as e:
        return "Error: " + str(e)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    resp = MessagingResponse()
    reply = get_gemini_reply(incoming_msg)
    resp.message(reply)
    return str(resp)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "")
    resp = MessagingResponse()
    reply = get_gemini_reply(incoming_msg)
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
