#!/bin/bash
# cron_jobs.sh
# Ce script est prévu pour être appelé par cron et réaliser deux tâches :
# 1. Mettre à jour les données via le scrapper.
# 2. Générer le rapport quotidien à 20h (optionnel).

# Chemin absolu vers le répertoire de ton projet - modifie-le en fonction de ton installation
PROJECT_DIR="/chemin/vers/ton/projet"

# 1. Exécuter le scrapper pour mettre à jour les données
cd "$PROJECT_DIR/scraping"
./scrapper.sh

# 2. Générer le rapport quotidien à 20h
# On récupère l'heure courante au format HH (00 à 23)
CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -eq "20" ]; then
    echo "Génération du rapport quotidien..."
    # Ici, tu peux ajouter la commande pour générer le rapport quotidien.
    # Par exemple, si tu as un script pour cela, décommente la ligne suivante :
    # cd "$PROJECT_DIR/rapport"
    # ./generate_daily_report.sh
fi
#