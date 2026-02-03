import os 
import shutil
from tkinter import Tk, filedialog
from datetime import datetime
import time
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ventana = Tk()
ventana.withdraw()

user = getpass.getuser()

log_file_name= "log.txt"

ruta=filedialog.askdirectory(title="Selecciona carpeta a ordenar")

ext_per_filetype = {
    "PDFs": [".pdf"],
    "Imagenes": [".png", ".jpg"],
    "Textos": [".txt"],
    "Audios": [".mp3"],
    "Videos": [".mp4"]
}




def createFolder(name: str): 
    ruta_carpeta = os.path.join(ruta,name)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    return ruta_carpeta


def orderFiles():
    for file in os.listdir(ruta):        
        for tipo in ext_per_filetype:            
            _,ext = os.path.splitext(file)
            if ext.lower() not in ext_per_filetype[tipo]: continue

            if file == log_file_name: continue


            ruta_carpeta = createFolder(tipo)

            if ext.endswith("png") or ext.endswith("jpg"):
                ruta_carpeta = createFolder(os.path.join(tipo, ext.upper().replace("." ,"")))
            
            nueva_ruta_archivo = os.path.join(ruta_carpeta, file)

            shutil.move(os.path.join(ruta, file),nueva_ruta_archivo)

            with open(os.path.join(ruta, log_file_name), "a", encoding="utf-8" ) as log: 
                log.write(f"{datetime.now().strftime("%d/%m/%Y %H:%M")} - Usuario: {user} - Movido {file} a {nueva_ruta_archivo.replace("\\", "/")}\n")

            
class EventHandler(FileSystemEventHandler):         
    def on_modified(self, event):
        if event.is_directory: return
        print(f"Archivo detectado: {event.src_path}")
        orderFiles()        




orderFiles()        

eventHandler=EventHandler()

observer = Observer()

observer.schedule(eventHandler, ruta, recursive=False)

observer.start()


try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    print("Programa detenido")
    observer.stop()


observer.join()
