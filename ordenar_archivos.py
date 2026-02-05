import os 
import shutil
import threading
from tkinter import Tk, filedialog, Button, Label
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

def wait_until_free(path, retries=10, delay=0.5):
    for _ in range(retries):
        try:
            with open(path, "rb"):
                return True
        except PermissionError:
            time.sleep(delay)
    return False

def orderFiles():
    
    for file in os.listdir(ruta):        
        for tipo in ext_per_filetype:            
            _,ext = os.path.splitext(file)

            if ext.lower() not in ext_per_filetype[tipo]: continue
            if file == log_file_name: continue

            if not wait_until_free(os.path.join(ruta, file)):                
                print(f"No se pudo acceder al archivo {file}. Saltando...")
                continue

            ruta_carpeta = createFolder(tipo)

            if ext.endswith("png") or ext.endswith("jpg"):
                ruta_carpeta = createFolder(os.path.join(tipo, ext.upper().replace("." ,"")))
            
            nueva_ruta_archivo = os.path.join(ruta_carpeta, file)

            
            shutil.move(os.path.join(ruta, file), nueva_ruta_archivo)

            with open(os.path.join(ruta, log_file_name), "a", encoding="utf-8" ) as log: 
                log.write(f"{datetime.now().strftime("%d/%m/%Y %H:%M")} - Usuario: {user} - Movido {file} a {nueva_ruta_archivo.replace("\\", "/")}\n")

            
class EventHandler(FileSystemEventHandler):         
    def on_created(self, event):
        if event.is_directory: return
        
        print(f"Archivo detectado: {event.src_path}")
        orderFiles()        




orderFiles()        

eventHandler=EventHandler()

observer = Observer()

observer.schedule(eventHandler, ruta, recursive=False)

def start_watch(): 
    observer.start()

def stop_watch():
    observer.stop()
    observer.join()
    ventana.quit()

ventana.deiconify()
ventana.title("Vigilando")
ventana.geometry("400x150")

Label(ventana, text="Vigilando carpeta", wraplength=350).pack(pady=10)
Button(ventana, text="Detener programa", command=stop_watch).pack(pady=10)

watch_thread=threading.Thread(target=start_watch, daemon=True)
watch_thread.start()

ventana.mainloop() 
