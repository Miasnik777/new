import requests
import json
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Функция для загрузки данных с URL
def load_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("records", [])
    else:
        print(f"Ошибка загрузки данных: статус-код {response.status_code}")
        return []

# Загружаем данные
url = "http://backend:8000/nocodb-data/"
data = load_data(url)

# Преобразование данных в DataFrame
df = pd.DataFrame(data)

# Настройка внешнего стиля
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Создание приложения Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Макет приложения
app.layout = html.Div(
    children=[
        html.H1("Скорость и точность ввода текста"),
        dcc.Graph(id="graph-with-slider"),
        html.P("Выберите устройство:"),
        dcc.Dropdown(
            id="device-dropdown",
            options=[{"label": row["устройство"], "value": row["Id"]} for _, row in df.iterrows()],
            value=df["Id"][0],
            clearable=False,
        ),
    ],
)

# Callback для обновления графика
@app.callback(
    Output("graph-with-slider", "figure"),
    Input("device-dropdown", "value"))
def update_figure(selected_device_id):
    filtered_df = df.query(f"Id == {selected_device_id}")
    fig = px.bar(filtered_df, x="устройство", y=["скорость", "точность"],
                 barmode="group", title=f"Скорость и точность для выбранного устройства")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)