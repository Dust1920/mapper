def data_list_map(mapa, col_data, data):
    mapa[col_data] = data
    return 0

def data_df_map(mapa, df):
    """
    IMPORTANTE, asegurate que los indices sean iguales.
    """
    for i in df.columns:
        mapa[f'data_{i}'] = df[i].to_list()