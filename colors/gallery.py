from matplotlib.colors import ListedColormap

## Lista de colores
c1 = '#3F709E'  # Fuerte (Verde)
c2 = '#3F7777'  # Medio (Azul Fuerte)
c3 = '#AAD8E2'  # Bajo (Azul Claro)



## Conjuntos de Colores
urban_map = {0: c1,  # Fuerte
            1: c2,  # Medio
            2: c3}  # Bajo


## Galerias

def colorset_to_gallery(colorset:dict):
    f = colorset.values()
    return ListedColormap(list(f))

