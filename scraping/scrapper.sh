#!/bin/bash
# scrapper.sh
# Script pour récupérer la température actuelle sur https://www.pleinchamp.com/meteo/15-jours/92000-nanterre

URL="https://www.pleinchamp.com/meteo/15-jours/92000-nanterre"

# 1. Récupérer le contenu HTML
html=$(curl -s "$URL")

# 2. Vérifier le contenu
if [ -z "$html" ]; then
    echo "Erreur : impossible de télécharger le contenu de $URL"
    exit 1
fi

# 3. Extraire la température
#    On suppose qu'il existe un <div class="... cUkKTT" ...>10,8°C</div>
#    et qu'on veut capturer tout format du type XX,XX°C ou XX°C.
#    L'expression suivante recherche :
#      - <div class="... cUkKTT" (peu importe ce qu'il y a entre guillemets)
#      - ^>]*> : tout attribut éventuel avant la fermeture de la balise
#      - [0-9]{1,2} : 1 ou 2 chiffres
#      - ([.,][0-9]{1,2})? : éventuellement une virgule/point + 1 ou 2 chiffres
#      - \s?°C : éventuellement un espace avant °C
temperature=$(echo "$html" | grep -oP '(?<=<div class="[^"]*cUkKTT"[^>]*>)[0-9]{1,2}([.,][0-9]{1,2})?\s?°C' | head -n1)

# 4. Nettoyer la valeur (par exemple enlever l'espace au besoin)
temperature_clean=$(echo "$temperature" | sed 's/ //g')

# 5. Récupérer l'heure et la date
now=$(date '+%Y-%m-%d %H:%M:%S')

# 6. Enregistrer dans un CSV (si tu as déjà créé le fichier avec un en-tête)
#    echo "timestamp,temperature" > ../data/temperatures.csv
echo "$now,$temperature_clean" >> ../data/temperatures.csv

# 7. Afficher un message de confirmation
echo "Scraping OK : $now -> $temperature_clean"
