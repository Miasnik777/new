# import dash
# from dash import dcc, html, Input, Output
# import pandas as pd
# import requests

# # Загружаем данные
# URL = "http://backend:8000/nocodb-data/"
# data = requests.get(URL).json()
# df = pd.DataFrame(data["records"])

# df = df.dropna(subset=["monitoring_id"])  # Убираем пустые записи

# df["monitoring_time"] = pd.to_datetime(df["monitoring_time"])

# df = df.sort_values("monitoring_time", ascending=True)

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1("Мониторинг виртуальных машин"),
#     dcc.Graph(id="cpu-usage-graph"),
#     dcc.Graph(id="memory-usage-graph"),
#     dcc.Interval(
#         id='interval-component',
#         interval=5000,  # Обновление каждые 5 секунд
#         n_intervals=0
#     )
# ])

# @app.callback(
#     [
#         Output("cpu-usage-graph", "figure"),
#         Output("memory-usage-graph", "figure")
#     ],
#     Input("interval-component", "n_intervals")
# )
# def update_graphs(n):
#     data = requests.get(URL).json()
#     df = pd.DataFrame(data["records"])
#     df = df.dropna(subset=["monitoring_id"])  # Убираем пустые записи
#     df["monitoring_time"] = pd.to_datetime(df["monitoring_time"])
#     df = df.sort_values("monitoring_time", ascending=True)
    
#     cpu_fig = {
#         "data": [{
#             "x": df["monitoring_time"],
#             "y": df["cpu_usage"],
#             "type": "line",
#             "name": "CPU Usage (%)"
#         }],
#         "layout": {"title": "Использование процессора"}
#     }
    
#     memory_fig = {
#         "data": [{
#             "x": df["monitoring_time"],
#             "y": df["memory_usage"],
#             "type": "line",
#             "name": "Memory Usage (%)"
#         }],
#         "layout": {"title": "Использование памяти"}
#     }
    
#     return cpu_fig, memory_fig

# if __name__ == "__main__":
#     app.run_server(debug=True)

# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                       value='lifeExp',
                       inline=True,
                       id='radio-buttons-final')
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
