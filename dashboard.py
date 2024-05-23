import dash
from dash import html, dcc, Input, Output
import dash_daq as daq
import dash_map as mp
import dash_data as dd


import plotly.express as px
import mapper as Mapper

sonora = Mapper.new_map(region = 'sonora')
sonora = sonora.to_crs("WGS84")





app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Educación en Sonora"),
    html.Div(children=[
        html.Div(children=[
            html.H2("Personalizacion"),
        ]),
        html.Div(children=[
        html.Div(children=[
            html.H3("Numero de Colores"),
            dcc.Input(id = "n_colors", value = 3, type = "number", debounce=True),
            html.H3(id = "number-test")
        ],style={"padding": "5px", "width": "30%"}),
        html.Div(children=[
            html.H3("Limite Inferior"),
            daq.ColorPicker(
                id='color-picker-inferior',
                value={'hex': '#119DFF'},  # Valor por defecto
            ),
            html.H3(id = "color-1")
        ],style={"padding": "5px", "width": "30%"}),
        html.Div(children=[
            html.H3("Limite Superior"),
            daq.ColorPicker(
                id='color-picker-superior',
                value={'hex': '#FF0000'},  # Valor por defecto
            ),html.H3(id = "color-2")
        ],style={"padding": "5px", "width": "30%"}),
        ],style={"display": "flex", "align-items": "flex-start", "gap": "10px"}),
    ],style={"background-color":"pink","padding":"5px"}),
    html.Div(children=[
        html.Div(children=[
            html.H2("Opciones"),
            html.H3("Selecciona el Ciclo"),
            dcc.Dropdown(
                id='ciclo-dropdown',
                options= dd.ciclos,
                value=dd.ciclos[0]  # Valor por defecto
            ),
            html.H3("Selecciona la Columna de Datos"),
            dcc.Dropdown(
                id='columna-dropdown',
                options= dd.data_columns,
                value=dd.data_columns[0]  # Valor por defecto
            ),
        ], style={"padding": "5px", "background-color": "lightgray", "width": "30%"}),
        html.Div(children=[
                html.H2(id = "map-plot"),
                dcc.Graph(id = "educ-Sonora"),
        ], style={"padding": "5px", "background-color": "white", "width": "60%"})
    ], style={"display": "flex", "align-items": "flex-start", "gap": "10px"}),
], style={"background-color": "lightblue"})

@app.callback(
    Output("number-test","children"),
    Input("n_colors","value")
)

def update_text(value):
    text = f"Tendremos {value} Colores"
    return text

@app.callback(
    Output("color-1","children"),
    Input("color-picker-inferior","value")
)

def color_1(value):
    return f"Color {value}"

@app.callback(
    Output("color-2","children"),
    Input("color-picker-superior","value")
)

def color_2(value):
    return f"Color {value}"


@app.callback(
        Output("map-plot","children"),
        Input('ciclo-dropdown',"value"),
        Input('columna-dropdown',"value")
)
def plot_title(ciclo, column):
    text = f"Mapa de {column} del ciclo {ciclo}"
    return text






@app.callback(
        Output("educ-Sonora","figure"),
        Input('ciclo-dropdown',"value"),
        Input('columna-dropdown',"value")
)



def sonora_map(ciclo, col):
    dfc = dd.by_ciclos(dd.data, ciclo)
    sonora[col] = [int(x) for x in dfc[col]]

    fig = px.choropleth_mapbox(sonora,
                            geojson=sonora.geometry,
                            locations=sonora.index,
                            color=col,
                            center={"lat": 29, "lon": -110},
                            mapbox_style="carto-positron",
                            zoom = 5)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig




if __name__ == "__main__":
    app.run_server(debug = True)


