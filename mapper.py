import mapper_colors as map_color
import mapper_data as map_data
import mapper_getfiles as map_file
import geopandas as gpd


def new_map(**kwargs):
    state = kwargs.get('region','all')
    mptype = kwargs.get('mptype','mun')
    map_file.get_statefile(state)
    try:
        id = map_file.states_n[state]
    except:
        print('RepMX')
    if state == 'all':
        state = 'rpmex'
        mptype = 'ent'
        id = '00'
    file_path = f'geodata\\region\\{state}\\conjunto_de_datos\\{id}{mptype}.shp'
    df = gpd.read_file(file_path)
    if state == 'rpmex':
        df = df.sort_values('CVE_ENT')
    else:
        df = df.sort_values('CVE_MUN')
    df.drop(columns= ['CVEGEO'], inplace = True)
    df.set_index(['NOMGEO'], drop = True, inplace = True)
    return df


def color_data_map(mapa, data, col_data, color, color_rule, **kwargs):
    mapa = map_data.data_map(mapa, data, col_data)
    mapa = map_color.color_map(mapa, color, color_rule, **kwargs)
    return mapa 


def template_map(mapa, template, ax):
    return 0


def boundary(mapa: gpd.GeoDataFrame, ax, **kwargs):
    default_config = {
        'Active': 1,
        'Line' : 1,
        'Color': 'black'
    }
    boundary_config = kwargs.get('bd_config',default_config)
    if boundary_config['Active']:
        mapa.boundary.plot(lw = boundary_config['Line'], color = boundary_config['Color']) 