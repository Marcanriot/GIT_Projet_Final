import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server  # pour déploiement éventuel

# 🔁 Fonction de chargement de données
def load_data():
    try:
        df = pd.read_csv('../data/subscribers.csv', names=["timestamp", "subscribers"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["subscribers"] = pd.to_numeric(df["subscribers"], errors='coerce')
        return df.dropna()
    except Exception as e:
        print("Erreur lors du chargement du CSV :", e)
        return pd.DataFrame(columns=["timestamp", "subscribers"])

# 🌐 Layout
app.layout = html.Div([
    html.H1("Évolution des abonnés (NASA)"),
    dcc.Graph(id='subs-graph'),
    dcc.Interval(id='interval-component', interval=5 * 60 * 1000, n_intervals=0)  # 5 minutes
])

# 🔄 Callback pour actualiser la courbe
@app.callback(
    Output('subs-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = load_data()
    fig = px.line(df, x='timestamp', y='subscribers', title="Nombre d'abonnés")
    return fig

# 🚀 Lancer l’app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
