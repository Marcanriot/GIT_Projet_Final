import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import os
from datetime import timedelta


# Charger les données CSV
def load_data():
    if os.path.exists("subscribers.csv"):
        df = pd.read_csv("subscribers.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    else:
        return pd.DataFrame(columns=["timestamp", "subscribers"])


# Abonnés gagnés dernière heure
def subscribers_last_hour(df):
    if df.empty:
        return "⏳ Pas de données disponibles."
    now = pd.Timestamp.now(tz="UTC")
    one_hour_ago = now - timedelta(hours=1)
    df_last_hour = df[df["timestamp"] >= one_hour_ago]
    if df_last_hour.shape[0] < 2:
        return "⏳ Pas assez de données dans la dernière heure."
    df_last_hour = df_last_hour.dropna(subset=["subscribers"])
    start = df_last_hour["subscribers"].iloc[0]
    end = df_last_hour["subscribers"].iloc[-1]
    try:
        gained = int(end - start)
    except:
        return "Erreur de calcul sur les données."
    return f"Abonnés gagnés (dernière heure) : {gained:,}"


def subscribers_today(df):
    today = pd.Timestamp.now(tz="UTC").normalize()
    df_today = df[df["timestamp"] >= today]
    if len(df_today) < 2:
        return "Pas assez de données pour aujourd’hui."
    start = df_today["subscribers"].iloc[0]
    end = df_today["subscribers"].iloc[-1]
    return f" Abonnés gagnés : {end - start:,}"


def daily_growth_percent(df):
    today = pd.Timestamp.now(tz="UTC").normalize()
    df_today = df[df["timestamp"] >= today]
    if len(df_today) < 2:
        return "⏳ Pas assez de données pour aujourd’hui."
    start = df_today["subscribers"].iloc[0]
    end = df_today["subscribers"].iloc[-1]
    growth = ((end - start) / start) * 100 if start else 0
    return f"Taux de croissance : {growth:.2f}%"


def peak_growth_time(df):
    today = pd.Timestamp.now(tz="UTC").normalize()
    df_today = df[df["timestamp"] >= today].copy()
    if len(df_today) < 2:
        return "⏳ Pas assez de données pour aujourd’hui."
    df_today["diff"] = df_today["subscribers"].diff()
    peak_row = df_today.loc[df_today["diff"].idxmax()]
    peak_time = peak_row["timestamp"].strftime('%H:%M')
    peak_gain = int(peak_row["diff"])
    return f"Pic de +{peak_gain} abonnés à {peak_time}"


# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "MrBeast Live Subscribers Dashboard"

app.layout = html.Div([
    html.H1("MrBeast - Dashboard abonnés", style={
        "textAlign": "center",
        "marginBottom": "40px"
    }),

    dcc.Tabs(id="tabs", value="live", children=[
        dcc.Tab(label="Temps réel", value="live"),
        dcc.Tab(label="Rapport du jour", value="report")
    ], style={"fontWeight": "bold"}),

    html.Div(id="tab-content"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0)
], style={
    "fontFamily": "Arial, sans-serif",
    "padding": "20px",
    "backgroundColor": "#e6f2ff",
    "minHeight": "100vh"
})

# Affichage par onglet
@app.callback(
    dash.Output("tab-content", "children"),
    [dash.Input("tabs", "value"),
     dash.Input("interval-component", "n_intervals")]
)

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
