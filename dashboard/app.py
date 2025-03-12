# dashboard/app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Fonction pour charger et préparer les données
def load_data():
    try:
        # Lire le fichier CSV contenant les données
        df = pd.read_csv('../data/temperatures.csv')
        # Convertir la colonne timestamp en format datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print("Erreur lors du chargement des données :", e)
        return pd.DataFrame(columns=["timestamp", "temperature"])

# Créer l'instance de l'application Dash
app = dash.Dash(__name__)

# Layout de l'application
app.layout = html.Div(children=[
    html.H1("Dashboard de prévisions météo"),
    dcc.Graph(id='temperature-graph'),
    # Un intervalle pour mettre à jour le graphique toutes les 5 minutes (300000 ms)
    dcc.Interval(
        id='interval-component',
        interval=300000,  # en millisecondes
        n_intervals=0
    )
])

# Callback pour mettre à jour le graphique en fonction des nouvelles données
@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = load_data()
    if df.empty:
        # Si aucune donnée n'est disponible, créer une figure vide
        fig = px.line(title="Pas de données disponibles")
    else:
        # Créer un graphique linéaire avec l'évolution des températures
        fig = px.line(df, x='timestamp', y='temperature',
                      title="Évolution des températures")
    return fig

# Lancer le serveur de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
