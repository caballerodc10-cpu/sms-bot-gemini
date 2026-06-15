from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google import genai
import os

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_gemini_reply(incoming_msg):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=incoming_msg
        )
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
