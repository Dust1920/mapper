import pandas as pd

data = pd.read_excel("data\\educ-data.xlsx")

data = data.iloc[1:, 1:]
data.columns = data.iloc[0]
data.drop(index = 1, inplace=True)
ciclos = list(data['Ciclo'].unique())
data_columns = list(data.columns)[2:]

def by_ciclos(df, ciclo):
    df_c = df[df['Ciclo'] == ciclo]
    df_c = df_c.iloc[:-1,:]
    return df_c
