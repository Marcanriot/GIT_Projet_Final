import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import os

# Charger les données CSV
def load_data():
    if os.path.exists("subscribers.csv"):
        df = pd.read_csv("subscribers.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    else:
        return pd.DataFrame(columns=["timestamp", "subscribers"])

# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "MrBeast Live Subscribers Dashboard"

# Mise en page
app.layout = html.Div([
    html.H1("📈 Évolution des abonnés de MrBeast", style={"textAlign": "center"}),

    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0),  # Auto-refresh toutes les 60 sec

    dcc.Graph(id="subscriber-graph")
])

# Callback pour mettre à jour le graphique
@app.callback(
    dash.Output("subscriber-graph", "figure"),
    [dash.Input("interval-component", "n_intervals")]
)
def update_graph(n):
    df = load_data()
    if df.empty:
        fig = px.line(title="Aucune donnée disponible")
    else:
        fig = px.line(df, x="timestamp", y="subscribers",
                      title="Nombre d'abonnés MrBeast dans le temps",
                      markers=True)
        fig.update_layout(xaxis_title="Heure", yaxis_title="Abonnés", template="plotly_white")
    return fig

# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)
