# iss-tracker
Simply iss-tracker

Costruisci l'immagine Docker:

bash

podman build -t iss-tracker .

Esegui il container:

bash

podman run -d -p 5000:5000 iss-tracker

Accedi all'applicazione: Apri il tuo browser e vai a http://localhost:5000. Dovresti vedere la mappa con la posizione della ISS e il popup con l'immagine.

