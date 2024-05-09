import os
from datetime import datetime

import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import AskGPT
import GptInfra
import requests
import urllib.request
from pydub import AudioSegment
import certifi
import logging
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Add a rotating handler to prevent log files from growing indefinitely
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logger.addHandler(handler)

@app.route("/wa")
def wa_hello():
    logger.info("Received a request on /wa")
    return "Hello, World!"

@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    # Load the Whisper model

    resp = MessagingResponse()
    reply=resp.message()
   
    msg = request.form.get('Body').lower() # Reading the message from the whatsapp
    num_media = int(request.values.get("NumMedia", 0))  # Check for media items
    if num_media > 0:  # This means there is at least one media item, likely a voice recording
        media_url = request.values.get("MediaUrl0")  # URL of the media item
        #audio_content = requests.get(media_url)
        response = requests.get(media_url, verify=certifi.where())
        # Save the audio to a temporary file (Whisper needs a file path)
        temp_audio_path = "temp_audio.ogg"
        with open("temp_audio.ogg", "wb") as f:
          f.write(response.content)

        # Transcribe the voice message using Whisper
        client = OpenAI(api_key=GptInfra.get_api_key())
        result = client.audio.transcriptions.create(model="whisper-1", file=open(temp_audio_path, 'rb'))
        transcript = result.text
        os.remove("temp_audio.ogg")  # Clean up the temp file       
        # Use the transcribed text as the message
        msg = transcript.lower()
        PrompetQuestion = GptInfra.Build_Prompet(msg)
        # Get the answer
        Answer = str(GptInfra.SendToGpt(PrompetQuestion))
        reply.body(Answer)
        return str(resp)
    # Get the message time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    

    print("msg-->",msg) # Printing the message on the console, for debugging purpose
    
    
    # Create reply
    # ========================================
    # Help menu
    if msg.startswith("/h"):
        resp.message("Commands:\n\n/q [question] - Ask a question\n/s [message] - Save a message\n/f [message] - Find related messages\n/h - Show this help menu")

    # Question answering
    elif msg.startswith("/q "):
        # Get the question
        question = msg.split("/q ")[1]
        # Construct the prompt
        PrompetQuestion = GptInfra.Build_Prompet(question)
        # Get the answer
        Answer = GptInfra.SendToGpt(PrompetQuestion)
        resp.message(Answer)
        return str(resp)
if __name__ == "__main__":	
     app.run(debug=True,host='localhost', port=8000)