import general_codes as gc
import mapper_data as mapdata
import geopandas as gpd
import numpy as np
from matplotlib.colors import ListedColormap
import mapper_addons as addon

def generate_color(**kwargs):
    a = kwargs.get('alpha', 1)
    hx = kwargs.get('hex', 1)
    red = np.random.uniform()
    green = np.random.uniform()
    blue = np.random.uniform()
    if hx:
        red_h = int(red * 255)
        green_h = int(green * 255)
        blue_h = int(blue * 255)
        alpha = int(a * 255)
        rgb_h = '#' + "".join([hex(red_h)[2:], hex(green_h)[2:], hex(blue_h)[2:], hex(alpha)[2:]])
        return rgb_h
    else:
        rgb = (red, green, blue, a)
    return rgb

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


def adapt_cmap(cmap: dict, partition):
    ncolors = len(partition) - 1
    if len(cmap.values()) >= ncolors:
        return {i:cmap[i] for i in range(ncolors)}
    else:
        k = len(cmap.values())
        while k < ncolors:
            cmap[k] = generate_color()
            k = k + 1
        return cmap



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
def cmap_by_partition(mapa, data, scheme, colors, **kwargs):
    partition = mapdata.scheme_to_interval(mapa, data, scheme, **kwargs)
    part_cmap = adapt_cmap(colors, partition)
    return partition, part_cmap

def color_by_data(mapa, col, scheme, colors, **kwargs):
    is_data_col = kwargs.get('dcol', [1,None])
    partition, pmap = cmap_by_partition(mapa, col, scheme, colors, **kwargs)
    if not is_data_col[0]:
        col_data = is_data_col[1]
    else:
        col_data = mapa[col].to_list()
    data_codes = [gc.loc_value_ival(partition, round(d, 2)) for d in col_data]
    color_data = [pmap[d] for d in data_codes]
    return color_data