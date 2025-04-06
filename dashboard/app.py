import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

def load_data():
    df = pd.read_csv('../data/subscribers.csv')

    # 🔧 Conversion explicite des types
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')

    # 🔍 Supprimer les lignes avec valeurs manquantes (si format invalide)
    df.dropna(subset=['timestamp', 'subscribers'], inplace=True)
    return df

app.layout = html.Div([
    html.H1("Évolution des abonnés (NASA)"),
    dcc.Graph(id='subs-graph'),
    dcc.Interval(id='interval-component', interval=300000, n_intervals=0)  # 5 min
])

@app.callback(
    dash.dependencies.Output('subs-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = load_data()
    fig = px.line(df, x='timestamp', y='subscribers', title="Nombre d'abonnés")
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
