import folium
import requests
import time


def get_iss_location():
    """Ottiene la posizione attuale della ISS."""
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP
        data = response.json()
        latitude = float(data['iss_position']['latitude'])
        longitude = float(data['iss_position']['longitude'])
        return latitude, longitude
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta all'API: {e}")
        return None, None

def create_map(latitude, longitude):
    """Crea la mappa Folium e aggiunge il marker ISS."""
    m = folium.Map(location=[latitude, longitude], zoom_start=3)

    # URL dell'immagine fornita (sostituiscila con l'URL valido se necessario)
    image_url = "https://media.istockphoto.com/id/1790878880/vector/space-station-vector-glyph-icon-for-personal-and-commercial-use.jpg?s=612x612&w=0&k=20&c=R4D_7Iuwp7ywmuxd8pXrJgtEa70WO5e6dAQzfxrLnqM="

    # Crea l'elemento IFrame per l'immagine
    iframe = folium.IFrame(f'<img src="{image_url}" width="100">',
                             width=120,  # Larghezza dell'IFrame
                             height=120) # Altezza dell'IFrame

    # Crea il popup con l'IFrame
    popup = folium.Popup(iframe, max_width=2650)

    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=folium.Icon(color="red", icon="rocket", prefix='fa'),
    ).add_to(m)

    return m

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    latitude, longitude = get_iss_location()
    if latitude is None or longitude is None:
        return "Impossibile ottenere la posizione della ISS."

    m = create_map(latitude, longitude)
    map_html = m._repr_html_()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Posizione ISS in Tempo Reale</title>
    </head>
    <body>
        <h1>Posizione ISS in Tempo Reale</h1>
        <div>{{ map_html|safe }}</div>
    </body>
    </html>
    """, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
