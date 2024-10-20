import os
import requests
import base64
import cv2
import numpy as np
import shutil
from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from gradio_client import Client as GradioClient, file
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

user_sessions = {}

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

gradio_client = GradioClient("Nymbo/Virtual-Try-On")

NGROK_URL = os.getenv("NGROK_URL")
print(NGROK_URL)

@app.post("/")
async def index():
    return {"message": "This is the virtual try-on chatbot API."}

@app.post("/webhook")
async def webhook(request: Request):
    form = await request.form()
    sender_number = form.get('From')
    media_url = form.get('MediaUrl0')

    print(f"Received media URL: {media_url}")

    resp = MessagingResponse()

    if not media_url:
        resp.message("We didn't receive an image. Please try sending your image again.")
        return JSONResponse(content=str(resp), media_type="application/xml")

    if sender_number not in user_sessions:
        user_sessions[sender_number] = {"person_image": media_url}
        resp.message("Great! Now please send the image of the garment you want to try on.")
    elif 'garment_image' not in user_sessions[sender_number]:
        user_sessions[sender_number]['garment_image'] = media_url
        try_on_image_url = await send_to_gradio(
            user_sessions[sender_number]['person_image'], media_url
        )

        if try_on_image_url:
            send_media_message(sender_number, try_on_image_url)
            resp.message("Here is your virtual try-on result!")
        else:
            resp.message("Sorry, something went wrong with the try-on process.")
        del user_sessions[sender_number]
    else:
        resp.message("Please send your image to begin the virtual try-on process.")

    return JSONResponse(content=str(resp), media_type="application/xml")

async def send_to_gradio(person_image_url, garment_image_url):
    person_image_path = await download_image(person_image_url, 'person_image.jpg')
    garment_image_path = await download_image(garment_image_url, 'garment_image.jpg')

    if not person_image_path or not garment_image_path:
        print("Error: One of the images could not be downloaded.")
        return None

    try:
        result = gradio_client.predict(
            dict={"background": file(person_image_path), "layers": [], "composite": None},
            garm_img=file(garment_image_path),
            garment_des="A cool description of the garment",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )

        if result and os.path.exists(result[0]):
            img = cv2.imread(result[0])
            static_dir = 'static'
            os.makedirs(static_dir, exist_ok=True)
            target_path_png = os.path.join(static_dir, 'result.png')
            cv2.imwrite(target_path_png, img)
            return f"{NGROK_URL}/static/result.png"

        print("No image returned from the API.")
        return None

    except Exception as e:
        print(f"Error interacting with Gradio API: {e}")
        return None

def send_media_message(to_number, media_url):
    message = twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body="Here is your virtual try-on result:",
        media_url=[media_url],
        to=to_number
    )
    print(f"Sent media message to {to_number}. Message SID: {message.sid}")

async def download_image(media_url, filename):
    try:
        message_sid = media_url.split('/')[-3]
        media_sid = media_url.split('/')[-1]
        media = twilio_client.api.accounts(TWILIO_ACCOUNT_SID).messages(message_sid).media(media_sid).fetch()
        image_url = f"https://api.twilio.com{media.uri.replace('.json', '')}"
        response = requests.get(image_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        print(f"Failed to download image: {response.status_code}")
        return None
    except Exception as err:
        print(f"Error downloading image from Twilio: {err}")
        return None

@app.get("/static/{filename}")
async def serve_static_file(filename: str):
    file_path = os.path.join('static', filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='image/png')
    raise HTTPException(status_code=404, detail="File not found")
