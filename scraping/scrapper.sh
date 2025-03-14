#!/bin/bash
# scrapper.sh
# Ce script récupère la page de prévisions météo pour Paris et extrait les températures horaires.

# 1. Définir l'URL de la page à scraper
URL="https://www.lachainemeteo.com/meteo-france/ville-33/previsions-meteo-paris-heure-par-heure"

# 2. Télécharger le contenu HTML de la page en mode silencieux (-s)
html=$(curl -s "$URL")

# 3. Vérifier que le téléchargement a réussi
if [ -z "$html" ]; then
    echo "Erreur : impossible de télécharger le contenu de $URL"
    exit 1
fi

# 4. Utiliser grep avec une expression régulière pour extraire les températures.
#    La regex '[0-9]{1,2}°C' recherche une ou deux chiffres suivis de '°C'
#    Cela permet d'extraire des valeurs comme "5°C", "12°C" ou "25°C".
temperatures=$(echo "$html" | grep -Eo '[0-9]{1,2}°C')

# 5. Afficher les températures extraites
echo "Les températures relevées sur la page :"
echo "$temperatures"

echo "$temperatures" > ../data/temperatures.txt


#on va créer un csv pout le stockage des données


# Récupérer la date et l'heure actuelles
now=$(date '+%Y-%m-%d %H:%M:%S')

# Extraire les températures (ici, on prend la première trouvée pour simplifier)
temp=$(echo "$html" | grep -Eo '[0-9]{1,2}°C' | head -n 1)

# Retirer le "°C" pour ne garder que le nombre
temp_number=$(echo "$temp" | sed 's/°C//')

# Ajouter une ligne au fichier CSV (en-tête : timestamp,temperature)
echo "$now,$temp_number" >> ../data/temperatures.csv

