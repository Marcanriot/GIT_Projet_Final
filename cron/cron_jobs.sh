#!/bin/bash
# cron_jobs.sh
# Ce script est prévu pour être appelé par cron et réaliser deux tâches :
# 1. Mettre à jour les données via le scrapper dynamique Python.
# 2. Générer le rapport quotidien à 20h (optionnel).

# Chemin absolu vers le répertoire de ton projet
# À adapter en fonction de ton installation
PROJECT_DIR="/GIT_Projet_final"

# 1. Exécuter le scrapper Python pour mettre à jour les données (nombre d'abonnés)
cd "$PROJECT_DIR/scraping"

# Si tu utilises un environnement virtuel, active-le avant :
source "$PROJECT_DIR/venv/bin/activate"

# Lancer le script Python dynamique (Selenium)
python scrapper_dynamic.py

# 2. Générer le rapport quotidien à 20h
CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -eq "20" ]; then
    echo "Génération du rapport quotidien..."
    # Ici, tu peux ajouter la commande pour générer le rapport quotidien.
    # Par exemple, si tu as un script pour cela, décommente la ligne suivante :
    # cd "$PROJECT_DIR/rapport"
    # ./generate_daily_report.sh
fi
