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
   git clone Deepanshu276
   cd Deepanshu276
