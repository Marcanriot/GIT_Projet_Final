#!/bin/bash
# scrapper.sh
# Récupère la température la plus récente depuis Infoclimat (Paris Seine - Tour Zamansky / Jussieu)

# 1. URL de la page à scraper
URL="https://www.infoclimat.fr/observations-meteo/temps-reel/paris-seine-tour-zamansky-jussieu/0000h.html?unit=unitus"

# 2. Récupérer le contenu HTML
html=$(curl -s -L \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36" \
  "$URL")

# 3. Vérifier si le contenu a bien été récupéré
if [ -z "$html" ]; then
    echo "Erreur : impossible de télécharger le contenu de $URL"
    exit 1
fi

# 4. Extraire la température la plus récente (en haut du tableau)
#    Sur Infoclimat, la colonne "Température" est souvent marquée par <td class="tc icuTxtRd">XX.X °C</td>
#    La commande ci-dessous cherche un motif du type "XX.X °C" et prend la première occurrence (head -n1).
temperature=$(echo "$html" \
  | grep -oP '(?<=<td class="tc icuTxtRd">)[0-9]{1,2}\.[0-9](?= °C</td>)' \
  | head -n1)

# 5. Vérifier si la température a été trouvée
if [ -z "$temperature" ]; then
    echo "Erreur : aucune température trouvée. (Peut-être du JavaScript ou structure différente ?)"
    exit 1
fi

# 6. Générer un timestamp
now=$(date '+%Y-%m-%d %H:%M:%S')

# 7. Écrire la donnée dans le fichier CSV
#    Assurez-vous d'avoir créé ce fichier (une seule fois) avec un en-tête :
#       echo "timestamp,temperature" > ../data/temperatures.csv
echo "$now,$temperature" >> ../data/temperatures.csv

# 8. Afficher un message de confirmation
echo "Scraping OK : $now -> $temperature °C"
