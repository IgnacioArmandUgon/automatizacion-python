import os 
import shutil
from tkinter import Tk, filedialog
from datetime import datetime
import getpass

ventana = Tk()
ventana.withdraw()

user = getpass.getuser()

log_file_name= "log.txt"

ruta= filedialog.askdirectory(title="Selecciona carpeta a ordenar")

ext_per_filetype = {
    "Imagenes": [".png", ".jpg"],
    "Textos": [".txt"],
    "PDFs": [".pdf"],
    "Audios": [".mp3"],
    "Videos": [".mp4"]
}

# tipos = extenciones_por_tipo.keys()


def createFolder(name: str): 
    ruta_carpeta = os.path.join(ruta,name)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    return ruta_carpeta


for file in os.listdir(ruta):
    for tipo in ext_per_filetype:
        _,ext = os.path.splitext(file)
        if ext.lower() in ext_per_filetype[tipo]:

            if file.startswith(log_file_name): break

            ruta_carpeta = createFolder(tipo)

            nueva_ruta_archivo =  os.path.join(ruta_carpeta, file)

            shutil.move(os.path.join(ruta, file),nueva_ruta_archivo)
            
            with open(os.path.join(ruta, log_file_name), "a", encoding="utf-8" ) as log: 
                log.write(f"{datetime.now().strftime("%d/%m/%Y %H:%M")} - Usuario: {user} - Movido {file} a {nueva_ruta_archivo.replace("\\", "/")}\n")

            
