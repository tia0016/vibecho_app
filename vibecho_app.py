from flask import Flask, render_template, request
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    raise Exception("Spotify client ID and secret must be set in the .env file")


def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = blip_processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption


def clean_keywords(caption):
    # Extract only words, remove punctuation, lowercase
    words = re.findall(r'\b\w+\b', caption.lower())
    return words


def get_spotify_recommendations(keywords, top_n=10):
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )

    query = " ".join(keywords[:5])
    print(f"Searching Spotify with query: {query}")
    results = sp.search(q=query, type='track', limit=top_n)

    tracks = [
        {
            "title": item['name'],
            "artist": item['artists'][0]['name'],
            "url": item['external_urls']['spotify'],
            "preview_url": item['preview_url']
        }
        for item in results['tracks']['items'] if item['preview_url']
    ]

    if not tracks:
        print("No tracks with preview found. Trying fallback query: happy summer party")
        results = sp.search(q="happy summer party", type='track', limit=top_n)
        tracks = [
            {
                "title": item['name'],
                "artist": item['artists'][0]['name'],
                "url": item['external_urls']['spotify'],
                "preview_url": item['preview_url']
            }
            for item in results['tracks']['items'] if item['preview_url']
        ]

    top_song = tracks[0] if tracks else None
    more_songs = tracks[1:] if len(tracks) > 1 else []
    return top_song, more_songs


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)

            caption = generate_caption(image_path)
            keywords = clean_keywords(caption)

            top_song, more_songs = get_spotify_recommendations(keywords)

            return render_template(
                'index.html',
                uploaded=True,
                image_path=image_path,
                caption=caption,
                top_song=top_song,
                more_songs=more_songs,
                logo="vibecho_logo.png"
            )

    return render_template('index.html', uploaded=False, logo="vibecho_logo.png")


if __name__ == '__main__':
    app.run(debug=True)
