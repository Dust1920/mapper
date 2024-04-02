import general_codes as gc
import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "monospace"
# Flechas, Texto, Ejes


def call_template(region, template):
    files = os.listdir('geodata\\Mexico')
    for f in files:
        try:
            f.index(region)
            id = f[:2]
        except:
            continue
    temp_df = pd.read_excel(f'templates\\{id}.xlsx', sheet_name=template, index_col=0)
    return temp_df


def print_regions(texts,p, ax, **kwargs):
    n_cols = kwargs.get('ncols',2)
    block = len(texts) // n_cols
    sep_x = kwargs.get('sx', 0.9e5)
    sep_y = kwargs.get('sy', 0.15e5)
    mun_x = p[0]
    mun_y = p[1]
    for k,mun in enumerate(texts):
        cve = f'0{k+1}' if k+1<10 else f'{k+1}'
        text = f'{cve} {mun}'
        ax.annotate(text=text, xy = (mun_x, mun_y), xytext= (mun_x + k // block * sep_x ,mun_y - k % block *sep_y),
                    fontsize = 12)
        

def legend_df(xs):
    u = xs[['legend_colors','legend_names']]
    i = 0
    while pd.isna(u.iloc[i, 0]) == False:
        i = i + 1
    ud = u.iloc[:i,:]
    ud.reset_index(drop = True, inplace = True)
    return ud

def create_legend(legend_df, leg_cf, x,y, ax1, **kwargs):
    s = kwargs.get('sep', 0.02)
    for i in legend_df.index:
        leg_c, leg_t = legend_df.loc[i,'legend_colors'], legend_df.loc[i,'legend_names']
        leg_cf[2] = leg_cf[2] if leg_cf[2] != 'None' else None
        ax1.annotate(f'● {leg_t}', xy = (1.5e6,2e6), xytext=(x * 1e6, (y - s * i) * 1e6)
                    , color = leg_c, weight = leg_cf[2], fontsize = leg_cf[0])
        

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
    try:
        legend = template.loc[ib_0, 'legend_colors']
        if not pd.isna(legend):
                leg_df = legend_df(template)
                leg_conf = gc.text_to_list(template.loc[ib_0,'legend_config'])
                x, y = template.loc[ib_0, 'legend_x'], template.loc[ib_0, 'legend_y']
                create_legend(leg_df,leg_conf, x, y, ax, **kwargs)
                box =template.loc[ib_0,'legend_border_style']
                if int(box[0]):
                    c1  =gc.text_to_list(template.loc[ib_0,'legend_border_corner1'])
                    c_dim = gc.text_to_list(template.loc[ib_0, 'legend_border_dims'])
                    style = template.loc[ib_0, 'legend_border_style']
                    if pd.isna(style):
                        gc.plot_rectangle(c1, c_dim, ax)
                    else:
                        style = gc.text_to_list(style)
                        gc.plot_rectangle(c1, c_dim, ax, config = style)
    except Exception as e:
            print(e)
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
        map.boundary.plot(color = bd[1], lw = bd[2], ax = ax)
    if not template.loc[ib_0, 'axis']:
        ax.set_axis_off()
    return 0

# plt.Rectangle((0.2, 0.2), 0.6, 0.6, fill=None, color='black', linestyle='-', linewidth=2)
# ax.add_patch(plt.Rectangle((0.2, 0.2), 0.6, 0.6, fill=None, color='black', linestyle='-', linewidth=2))
    

# chicago.plot(
#     column="POP2010",
#     legend=True,
#     scheme="quantiles",
#     figsize=(15, 10),
#     missing_kwds={
#         "color": "lightgrey",
#         "edgecolor": "red",
#         "hatch": "///",
#         "label": "Missing values",
#     },
# )