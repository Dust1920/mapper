import mapper_addons as addon
import general_codes as gc
import numpy as np
import pandas as pd
import mapper_colors as mapcol
import mapper_gallery as mgal
import mapclassify as mapc


def set_data(df):
    """
    Input:
        df: DataFrame
    Output:
        columnas de datos \n
        dentro del DataFrame: Lista
        
    """
    df_c = list(df.columns)
    gi = df_c.index('geometry')
    return df_c[gi + 1:]

def data_list_map(mapa, col_data, data):
    mapa[col_data] = data
    return 0

def data_df_map(mapa, df):
    """
    IMPORTANTE, asegurate que los indices sean iguales.
    """
    for i in df.columns:
        mapa[f'data_{i}'] = df[i].to_list()


def construct_legformat(template):
    ib_0 = list(template.index)[0]
    leg_fmt = {'title': gc.text_to_list(template.loc[ib_0, 'legend_title'])}
    for m, mun in enumerate(template.index):
        if np.logical_and(m > 0, pd.isna(template.loc[mun, 'legend_order']) == False):
            leg_fmt[int(template.loc[mun, 'legend_order'])] = gc.text_to_list(template.loc[mun, 'legend_text'])
    return leg_fmt




def leg_text(pos, leg: dict, ax, **kwargs):
    default = {
        'bbox_config':{'fc':'lightblue',
                        'ec': 'red',
                        'lw': 2},
        'text_config': {
            'fontsize' : 20,
            'color': 'white',
            'weight': 'bold'
        }
    }
    box_props = kwargs.get('bbox_props', default['bbox_config'])
    text_props = kwargs.get('txt_props', default['text_config'])
    sx = kwargs.get('sep_x', 1e4)
    sy = kwargs.get('sep_y', 2e4)
    g = 0
    labels = [len(k[-1]) for k in leg.values()]
    lab_max = np.array(labels).max()
    leg_list = list(leg.values())
    max_text = leg_list[labels.index(lab_max)][-1]
    ax.annotate(f'{max_text}\n' * len(leg.keys()) + f'{max_text}', xy = pos, xytext=pos, ha = 'left',va = 'top',
                bbox = box_props, fontsize = text_props['fontsize'], color = box_props['fc'])
    for color, lt in leg.items():
        if color == 'title':
            ax.annotate(lt[-1], xy = pos, xytext = (pos[0], pos[1] - g * sy),
                        color = lt[1], fontsize = lt[0], ha = 'left', va = 'top', weight = lt[2])
            g = g + 1
        else:
            # Icono
            ax.annotate(lt[1], xy = pos, xytext = (pos[0], pos[1] - g * sy),
                        color = color, fontsize = lt[0], ha = 'left', va = 'top')
            # Texto
            ax.annotate(lt[-1], xy = pos, xytext = (pos[0] + sx, pos[1]- g * sy),
                        color = lt[4], fontsize = lt[2], ha = 'left', va = 'top', weight = lt[3])
            g = g + 1


def legend_content(labels, config):
    lks = list(config.keys())
    for k in range(1, len(lks)): 
        config[lks[k]][-1] = labels[k - 1]
    return config









def construct_dataformat(template):
    ib_0 = list(template.index)[0]
    data_fmt = {'scheme': template.loc[ib_0, 'legend_order']}
    color = {}
    for m, mun in enumerate(template.index):
        if np.logical_and(m > 0, pd.isna(template.loc[mun, 'legend_order']) == False):
            color[int(template.loc[mun, 'legend_order'])] = template.loc[mun, 'legend_color']
    data_fmt['colors'] = color
    data_fmt['interval'] = int(template.loc[ib_0,'legend_text'])
    return data_fmt

def scheme_to_interval(mapa, col, scheme, **kwargs):
    is_data_col = kwargs.get('dcol', [1,None])
    schemes = {
        'quantiles': mapc.Quantiles,
        'percentiles':mapc.Percentiles
    }
    if not is_data_col[0]:
        raw_interval = str(schemes[scheme](is_data_col[1]))
    else:
        raw_interval = str(schemes[scheme](mapa[col]))
    u = raw_interval.split('\n')[4:]
    uv = [q.split('|')[0].rstrip() for q in u]
    mm = [q[1:-1].split(',') for q in uv]
    intervals = []
    for p in mm:
        for pp in p:
            gc.actu_list(intervals, float(pp))
    return intervals


def legend_by_data(mapa, col, ax, **kwargs):
    default = {
        'legend_config': {'title': [20, 'black', 'bold', 'Colores Prueba'],
                          0: [20, '●', 16, 'bold', 'black', 'Aereo'],
                          1: [20, '●', 16, 'bold', 'black', 'Terrestre'],
                          2: [20, '●', 16, 'bold', 'black', 'Maritimo'],
                          3: [20, '●', 16, 'bold', 'black', 'Maritimo_Terrestre'],
                          4: [20, '●', 16, 'bold', 'black', 'Maritimo_Aereo']},
        'data_config': {'scheme': 'quantiles',
                        'colors': {0:mgal.isaf_plata,
                                   1:mgal.isaf_naranja,
                                   2:mgal.isaf_verde,
                                   3:mgal.isaf_dorado,
                                   4:mgal.isaf_guinda},
                                   'interval': True}
    }
    is_data_col = kwargs.get('dcol', [1,None])
    legend_pos = kwargs.get('legend_xy', [1.3e6,1.9e6])
    legend_block = kwargs.get('legend_format',default['legend_config']
    )
    leg_line_dflt = [20, '●', 16, 'bold', 'black', 'Maritimo_Aereo']
    data_properties = kwargs.get('data', default['data_config'])
    for k, l in legend_block.items():
        if l == None:
            legend_block[k] = default['legend_config'][k]
    for n, d in data_properties.items():
        if d == None:
            data_properties[n] = default['data_config'][n]

    leg_labels =[]
    if not is_data_col[0]:
        partition = scheme_to_interval(mapa, col, data_properties['scheme'], **kwargs)
    else:
        partition = scheme_to_interval(mapa, col, data_properties['scheme'], **kwargs)
    data_properties['colors'] = mapcol.adapt_cmap(data_properties['colors'], partition)
    x = len(legend_block)
    while x < len(data_properties['colors']) + 1:
        legend_block[x - 1] = leg_line_dflt
        x = x + 1
    leg_colorf = {'title': legend_block['title']}
    for k in range(len(data_properties['colors'])):
        leg_colorf[data_properties['colors'][k]] = legend_block[k]
        color_data = mapcol.color_by_data(mapa, col,
                                      data_properties['scheme'],
                                      data_properties['colors'], dcol = is_data_col)
        if data_properties['interval']:
            for k in range(len(partition) - 1):
                if k == len(partition) - 2:
                    leg_labels.append(f'[{partition[k]}, {partition[k + 1]}]')
                else:
                    leg_labels.append(f'[{partition[k]}, {partition[k + 1]})')
        else:
            for k in range(len(partition) - 1):
                leg_labels.append(f'{partition[k]}, {partition[k + 1]}')
        leg_colorf = legend_content(leg_labels, leg_colorf)
        mapa.plot(color = color_data, ax = ax)
        leg_text(legend_pos, leg_colorf, ax, sep_x = 2e4)








def read_template(map, template, ax):
    data_plot = template['data'].to_list()
    legend_by_data(map, '1', ax, legend_xy = [1.3e6, 2e6],
                     legend_format = construct_legformat(template),
                        data = construct_dataformat(template), dcol = [0,data_plot])
    ib_0 = list(template.index)[0]
    title = template.loc[ib_0,'title']
    title_config = gc.text_to_list(template.loc[ib_0,'title_conf'])
    fw = title_config[2] if title_config[2]!= 'None' else None
    ax.set_title(title,
                 fontsize = title_config[0], color = title_config[1], weight = fw)
    ac_bd = template.loc[ib_0,'bd']
    for reg in template.index:
        t_x = template.loc[reg, 'texto_x']
        t_y = template.loc[reg, 'texto_y']
        f_x = template.loc[reg, 'flecha_x']
        f_y = template.loc[reg, 'flecha_y']
        t_coords = (t_x, t_y)
        f_coords = (f_x, f_y)
        flecha = template.loc[reg, 'flecha']
        text_cfig = template.loc[reg, 'text_conf']
        text_cfig = gc.text_to_list(text_cfig)
        if flecha:
            flecha_sets = template.loc[reg, 'flecha_conf']
            flecha_sets = gc.text_to_list(flecha_sets, ntype = float)
            addon.arrow_block(template.loc[reg,'texto'], f_coords, t_coords, flecha_sets, ax,
                        text_cf = text_cfig)
        else:
            addon.text_block(template.loc[reg,'texto'], t_coords, ax,
                       text_cf = text_cfig)
    if int(ac_bd[0]):
        bd = gc.text_to_list(template.loc[ib_0,'bd'])
        map.boundary.plot(color = bd[1], lw = bd[2], ax = ax)
    if not template.loc[ib_0, 'axis']:
        ax.set_axis_off()
    