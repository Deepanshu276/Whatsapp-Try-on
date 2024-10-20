# Virtual Try-On Chatbot with FastAPI

This project is a **virtual try-on chatbot** powered by **FastAPI**. It integrates **Twilio WhatsApp messaging** and **Gradio's Virtual Try-On API** to provide an interactive user experience. Users can send their images via WhatsApp, and the chatbot returns a virtual try-on result with the garment they upload.

## Features
- **WhatsApp Integration:** Users interact with the chatbot through WhatsApp.
- **Image Processing:** Users send two images – their own and the garment – and receive a virtual try-on image.
- **Twilio Messaging:** Uses Twilio to send/receive WhatsApp messages and media.
- **Gradio Virtual Try-On API:** The backend integrates Gradio for generating the try-on image.
- **Environment Variables:** Sensitive credentials are managed securely using a `.env` file.

## Technologies Used
- **FastAPI:** Backend framework for building APIs.
- **Twilio:** Handles WhatsApp communication.
- **Gradio:** Provides the virtual try-on feature.
- **OpenCV:** Processes images and converts them to PNG format.
- **Python-dotenv:** Loads environment variables from the `.env` file.
- **Uvicorn:** ASGI server to run the FastAPI application.

---

## Installation

### Prerequisites
- **Python 3.8+** installed.
- A **Twilio account** with WhatsApp sandbox enabled.
- **Ngrok** (or other tunneling services) to expose your local server to the internet.

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Deepanshu276/Whatsapp-Try-on.git
   cd Whatsapp-Try-on

2. **Install the dependencies:**
   ```bash
      pip install -r requirements.txt
3. **Create a .env file to store environment variables:**
   ```bash
   touch .env
   Add the following content to the .env file:
   TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
   TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
   NGROK_URL=<your_ngrok_url>
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8080



