# GIT_Projet_Final

## Description

Ce projet a pour but de scrapper les données du site : 

https://socialcounts.org/youtube-live-subscriber-count/UCX6OQ3DkcsbYNE6H8uQQuVA. 

Ce site répertorie en direct le nombre d'abonnés du youtuber MrBeast. Nous avons effectué ce choix car le premier site que nous avions voulu scrapper provoquait trop d'erreurs et rendait l'analyse de données impossible. Lors de notre reprise du projet, nous avons fait un retour à 0 et nous sommes partis de nouveaux fichiers car les anciens contenaient les données de l'ancien site. 

Nous avons donc commencé par vérifier que le scrapping de données de ce site fonctionnait et c'était le cas. Par la suite, nous nous sommes penchés sur le fond du dashboard. Nous avons commencé par tester de nombreux calculs et nous nous sommes arrêtés sur ceux qui nous paraissaient les plus appropriés.

Le cœur du projet repose sur deux composants :
- Un **script de scrapping** automatique lancé régulièrement
- Un **dashboard web** interactif, codé avec **Dash** et **Plotly**

## Technologies utilisées

- **Python 3.9**
- **Dash** et **Plotly** pour le dashboard web
- **Pandas** pour la manipulation de données
- **Bash** pour le scrapping automatique
- **Linux** (VM Ubuntu / EC2)
- **Cron** pour répéter le scrapping
- Un fichier **CSV** contenant les dates et le nombre d'abonnés

## Fonctionnalités du dashboard

### Graphique principal
- Affiche l’évolution du nombre d’abonnés dans le temps
- Mise à jour automatique toutes les 5 minutes

### Statistiques dynamiques
Sous le graphique, sont affichées en temps réel :
- Nombre d’abonnés gagnés dans la dernière heure
- Nombre d’abonnés gagnés depuis minuit
- Taux de croissance sur la journée
- Heure du pic d’abonnements

### Rapport journalier automatique
Un second onglet « Rapport du jour » affiche chaque soir à 20h :
- Le total d’abonnés gagnés dans la journée
- La croissance en pourcentage
- La durée de suivi
- Les heures du premier et du dernier relevé
- La moyenne d’abonnés gagnés par heure
- L’heure du pic d’abonnement

Avant 20h, le rapport affiché est celui de la veille.

## Architecture du projet 

<pre>
├── main.py              # Dashboard Dash (frontend + calculs)
├── scrap.sh             # Script bash de scrapping toutes les 5 min
├── subscribers.csv      # Fichier de données (timestamp, abonnés)
├── requirements.txt     # Dépendances Python
└── README.md            # Présentation du projet
</pre>

## Auteurs
Henriot Marc-Antoine

Khadraoui Elyess


## 
Projet développé dans le cadre du module Advanced Python, Git & Linux.
