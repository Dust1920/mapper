import general_codes as gc
import pandas as pd
# Flechas, Texto, Ejes

def legend_df(xs):
    u = xs[['legend_colors','legend_names']]
    i = 0
    while pd.isna(u.iloc[i, 0]) == False:
        i = i + 1
    ud = u.iloc[:i,:]
    ud.reset_index(drop = True, inplace = True)
    return ud

def create_legend(leg_df):
    return 0

def text_block(content, c_text, ax, **kwargs):
    text_conf = kwargs.get('text_cf',[24,'black'])
    fs = text_conf[0]
    fc = text_conf[1]
    fw = text_conf[2] if text_conf[2] != 'None' else None
    ax.annotate(content, xy= c_text, xytext= c_text,
                fontsize = fs, color = fc, weight = fw)

def arrow_block(content, c_flecha, c_text, config, ax, **kwargs):
    text_conf = kwargs.get('text_cf',[24,'black', 'None'])
    fs = text_conf[0]
    fc = text_conf[1]
    fw = text_conf[2] if text_conf[2] != 'None' else None
    if len(config) == 2:
        arrow_cfig = {
            'arrowstyle': config[0],
            'color': config[1]
        }
    else:
        arrow_cfig = {
            'width': config[0],
            'color': config[1],
            'headwidth': config[2],
            'headlength': config[3]
        }
    ax.annotate(content, xy= c_flecha, xytext= c_text, arrowprops = arrow_cfig,
                fontsize = fs, color = fc, weight = fw)

def read_template(map, template, ax, **kwargs):
    color_t = template['color_relleno']
    map.plot(color = color_t, ax = ax)
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
            arrow_block(template.loc[reg,'texto'], f_coords, t_coords, flecha_sets, ax,
                        text_cf = text_cfig)
        else:
            text_block(template.loc[reg,'texto'], t_coords, ax,
                       text_cf = text_cfig)
    if int(ac_bd[0]):
        bd = gc.text_to_list(template.loc[ib_0,'bd'])
        print(bd)
        map.boundary.plot(color = bd[1], lw = bd[2], ax = ax)
    if not template.loc[ib_0, 'axis']:
        ax.set_axis_off()
    return 0

def read_template(map, template, ax):
    color_t = template['color_relleno']
    map.plot(color = color_t, ax = ax)
    ib_0 = list(template.index)[0]
    try:
        legend = template.loc[ib_0, 'legend_colors']
        if not pd.isna(legend):
                legend_df = legend_df(template)
                leg_conf = template.loc[ib_0,'legend_config']
                create_legend(legend_df, ax)
    except:
            print('AAA')
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
            arrow_block(template.loc[reg,'texto'], f_coords, t_coords, flecha_sets, ax,
                        text_cf = text_cfig)
        else:
            text_block(template.loc[reg,'texto'], t_coords, ax,
                       text_cf = text_cfig)
    if int(ac_bd[0]):
        bd = gc.text_to_list(template.loc[ib_0,'bd'])
        print(bd)
        map.boundary.plot(color = bd[1], lw = bd[2], ax = ax)
    if not template.loc[ib_0, 'axis']:
        ax.set_axis_off()
    return 0
