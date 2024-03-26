import general_codes as gc
import geopandas as gpd
import numpy as np
from matplotlib.colors import ListedColormap


def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    hex_str = hex_str[1:]
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(0,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]


def gradient_cmap(col_limits, n_colors):
     return ListedColormap(get_color_gradient(col_limits[0],col_limits[1], n_colors))


def custom_cmap(colors: dict):
    ncols = len(colors.values())
    colormap = [colors[i] for i in range(ncols)]
    return ListedColormap(colormap)    


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