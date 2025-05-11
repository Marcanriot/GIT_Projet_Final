#!/bin/bash

# URL du compteur de MrBeast
url="https://socialcounts.org/youtube-live-subscriber-count/UCX6OQ3DkcsbYNE6H8uQQuVA"

# Fichier CSV de sortie
output_file="subscribers.csv"

# Si le fichier n'existe pas encore, ajoute l'en-tête
if [ ! -f "$output_file" ]; then
    echo "timestamp,subscribers" > "$output_file"
fi

# Télécharger la page
html=$(curl -s "$url")

# Extraire le nombre d'abonnés à partir de la balise avec la classe spécifique
subs=$(echo "$html" | grep -oP '<div class="id_odometer__dDC1d mainOdometer">\K[0-9]+')

# Obtenir l'heure actuelle au format ISO 8601
timestamp=$(date -Iseconds)

# Enregistrer dans le CSV
echo "$timestamp,$subs" >> "$output_file"

# Affichage de contrôle
echo "[$times]()
