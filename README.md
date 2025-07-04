# 🎵 VibEcho
> *Upload your vibe. Hear your echo.*

**VibEcho** is an AI-powered web application that captures the mood of your photo and recommends songs that match its vibe.  
It uses BLIP (a vision-language AI model) to generate captions and the Spotify API to suggest music — creating a unique sensory connection between images and audio.

---

#  Features

-  Upload any photo — a selfie, a scenic view, a vibe check
-  Get an AI-generated caption with **BLIP** (Bootstrapped Language Image Pretraining)
-  Receive Spotify-based song recommendations that match your photo's mood
-  Instagram-inspired, clean, responsive interface

---

## Get Started

# Clone the repository
git clone https://github.com/tia0016/vibecho_app.git
cd vibecho_app

# Install dependencies
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up your Spotify API credentials
-Visit Spotify Developer Dashboard
-Create an app
-Note down your Client ID and Client Secret

# Configure environment variables
Create a .env file in the root folder:
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret

# ▶️ Run the App
-python vibecho_app.py
-eg Open http://127.0.0.1:5000/ in your browser.

#  Project Structure
├── static/uploads/           # Uploaded images
├── templates/index.html      # Frontend template
├── vibecho_app.py            # Main Flask app
├── .env                      # Spotify keys (not committed)
├── .gitignore                # Ignore secrets & cache
├── requirements.txt          # Python dependencies
├── README.md                 # This file

---

#  Built With
-Python & Flask
-BLIP (HuggingFace) — Image captioning
-Spotify Web API — Music recommendations
-HTML, CSS, Jinja2 Templates

---

# Acknowledgements
BLIP — Image captioning model

Spotify Web API — Music data & previews

Flask — Web framework

# Acknowledgements
-BLIP — Image captioning model
-Spotify Web API — Music data & previews
-Flask — Web framework

# Author
Built with by @tia0016
