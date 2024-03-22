import os
import urls
import requests
import zipfile # Librería para trabajar con .zip


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


url = urls.mexico
# Creamos la carpeta 
if not os.path.exists('geodata'):
    os.mkdir('geodata')

geodata = 'geodata'

if not os.path.exists('geodata\\Mexico.zip'):
    data = requests.get(url, stream = True)
    with open('geodata\\Mexico.zip', "wb") as f:
        for c, chunk in enumerate(data.iter_content(chunk_size=512)):
            print(c / 6246342 ) # Aprox Size Charge Bar
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

folder_states = 'geodata\\Mexico'
folder_region = 'geodata\\region'
create_folder(folder_states)
with zipfile.ZipFile('geodata\\Mexico.zip','r') as zip:
    zip.extractall('geodata\\Mexico')
create_folder(folder_region)

create_folder("templates\\Mexico")
