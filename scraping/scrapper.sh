#!/bin/bash
# scrapper.sh
# Script pour récupérer la température actuelle à Puteaux depuis lameteoagricole.net

# 1. URL de la page
URL="https://www.lameteoagricole.net/previsions-meteo-agricole/Puteaux-92800.html"

# 2. Récupérer le contenu HTML
html=$(curl -s "$URL")

# 3. Vérifier si on a récupéré quelque chose
if [ -z "$html" ]; then
    echo "Erreur : impossible de télécharger le contenu de $URL"
    exit 1
fi

# 4. Extraire la température actuelle
#    On cherche un pattern du type "XX°C" dans le HTML.
#    Par exemple : grep -oP '[0-9]{1,2}(?=°C)'
#    On peut affiner la regex si nécessaire (en tenant compte de la structure HTML réelle).
temperature=$(echo "$html" | grep -oP '(?<=<span class="d-inline"[^>]*>)[0-9]+')


# 5. Récupérer la date et l'heure courantes
now=$(date '+%Y-%m-%d %H:%M:%S')

# 6. Enregistrer dans un fichier CSV (timestamp,temperature)
#    Assure-toi d'avoir créé ce fichier avec un en-tête :
#      echo "timestamp,temperature" > ../data/temperatures.csv
echo "$now,$temperature" >> ../data/temperatures.csv

# 7. Afficher un message dans le terminal
echo "Scraping OK : $now -> ${temperature}°C"


