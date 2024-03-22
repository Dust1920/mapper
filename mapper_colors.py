import general_codes as gc
import geopandas as gpd


def code_values(codes: list, colors: dict):
    """
    Crea un diccionario personalizado con una galería de colores y \nun codigo para cada color. 
    """
    y = {codes[i]: colors[key] for i, key in enumerate(colors.keys())}
    return y


def code_data(mapa, col, color_rules: dict):
    """
    Asigna un color a cada dato de una columna en específico \nmediante unas reglas de color. 
    """
    mapa[f'color_{col}'] = mapa[col].agg(lambda x: gc.assign_value(color_rules, x))


def color_map(mp: gpd.GeoDataFrame, col, color_rules, ax):
    code_data(mp, col, color_rules)
    mp.plot(color = mp[f'color_{col}'].to_list(), ax = ax)
    mp.boundary.plot(color = 'white', lw = 1, ax = ax)
    ax.set_axis_off()