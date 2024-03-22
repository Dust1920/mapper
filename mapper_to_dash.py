import mapper as Mapper
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

from dash import Dash, dcc, html, Input, Output


app = Dash(__name__)


app.layout = html.Div([
    html.H4('Prueba'),
    html.P("Mapa de Sonora"),
    dcc.RadioItems(
        id='candidate', 
        options=["Joly", "Coderre", "Bergeron"],
        value="Coderre",
        inline=True
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    sonora = Mapper.new_map(region = 'sonora')
    sonora2 = sonora.to_crs("EPSG:4326")
    geo_df = sonora2

    fig = px.choropleth_mapbox(geo_df,
                            geojson=geo_df.geometry,
                            locations=geo_df.index,
                            center={"lat": 28.5517, "lon": -110.7073},
                            mapbox_style="open-street-map",
                            zoom=5)
    return fig


app.run_server(debug=True)


df = px.data.election()

