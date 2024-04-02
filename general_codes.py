import os


def assign_value(rule: dict, text):
    return rule[text]


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def actu_list(lista, nv):
    try:
        l_nv = lista.index(nv)
    except:
        lista.append(nv)
    return lista


def text_to_list(text, **kwargs):
    number_type = kwargs.get('ntype',int)
    l = text.split(',')
    for i in range(len(l)):
        try:
            l[i] = number_type(l[i])
        except:
            l[i] = l[i]
    return l


def plot_line(start_point,end_point, ax, **kwargs):
    cf = kwargs.get('config', [1,'black', '.',16,'-', 1])
    if cf[0]:
        x_s = start_point[0]
        y_s = start_point[1]
        x_f = end_point[0]
        y_f = end_point[1]
        ax.plot([x_s,x_f], [y_s, y_f],
                color = cf[1], marker = cf[2], ms = cf[3], ls = cf[4], lw = cf[5])


def plot_rectangle_corners(corner_1,corner_2, ax, config):
        if config[0]:
            cor_1x = corner_1[0]
            cor_1y = corner_1[1]
            cor_2x = corner_2[0]
            cor_2y = corner_2[1]
            ax.plot([cor_1x,cor_2x],[cor_1y,cor_1y],
                    color = config[1], marker = config[2], ms = config[3], ls = config[4], lw = config[5])
            ax.plot([cor_2x,cor_2x],[cor_2y,cor_1y],
                    color = config[1], marker = config[2], ms = config[3], ls = config[4], lw = config[5])
            ax.plot([cor_2x,cor_1x],[cor_2y,cor_2y],
                    color = config[1], marker = config[2], ms = config[3], ls = config[4], lw = config[5])
            ax.plot([cor_1x,cor_1x],[cor_1y,cor_2y],
                    color = config[1], marker = config[2], ms = config[3], ls = config[4], lw = config[5])


def plot_rectangle(corner, rec_dim, ax, **kwargs):
    cf = kwargs.get('config', [1,'black', '.',16,'-', 1])
    corner_2 = tuple([corner[0] + rec_dim[0],corner[1] + rec_dim[1]])
    plot_rectangle_corners(corner, corner_2, ax, cf)


all_maps = {'Estados': 'ent.shp',
                    'Municipios':'mun.shp',
                    'AGEB': 'a.shp',
                    'Locs. Puntuales Rur': 'lpr.shp',
                    'Locs. Urb y Rur Amnzs': 'l.shp'}
state_maps = {'Estados': 'ent.shp',
                    'Municipios': 'mun.shp',
                    'AGEBRur': 'ar.shp',
                    'Locs. Puntuales Rur': 'lpr.shp',
                    'Insular': 'ti.shp',
                    'Polys. Exts. Rurales': 'pe.shp',
                    'Polys. Exts. Manzanas': 'pem.shp',
                    'AGEB': 'a.shp',
                    'Manzanas': 'm.shp',
                    'Frentes Mzns': 'fm.shp',
                    'Vialidad': 'e.shp',
                    'Caserio Disperso': 'cd.shp'}


def loc_value_ival(interval, value):
    """
    Input:\n
    Particion: Lista \n
    Valor : Flotante \n
    \n
    Output:\n
    Posición en la partición: Entero
    """
    for i in range(len(interval) - 1):
        if i == 0:
            if interval[i] <= value <= interval[i + 1]:
                return i
        else:
            if interval[i] < value <= interval[i + 1]:
                return i
            else:
                continue
    return -1


def prop_to_coords(p_prop, ax):
    """
    Input:\n
    Mapa: GeoDataFrame\n
    Posición relativa: (p_x,p_y) 0<= p_x,p_y <= 1\n
    \n
    Output:\n
    Posición absoluta en el mapa. (x,y)
    """
    map_xlim = ax.get_xlim()
    map_ylim = ax.get_ylim()
    p_x = map_xlim[0] * (1 - p_prop[0]) + map_xlim[1] * p_prop[0]
    p_y = map_ylim[0] * (1 - p_prop[1]) + map_ylim[1] * p_prop[1]
    return tuple([p_x, p_y])