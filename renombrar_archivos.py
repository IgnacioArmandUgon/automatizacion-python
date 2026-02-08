import os 
from tkinter import Tk, filedialog, Button, Label, messagebox, Frame, Entry, LEFT, RIGHT
import getpass

def selectFolder():
    folder=filedialog.askdirectory(title="Selecciona carpeta a ordenar")    
    dir_input.insert(0,folder)

def renameFiles():
    folder=dir_input.get()
    prefix=prefix_input.get()
    ext=tuple(ext_input.get().split(","))

    files= [
        file for file in os.listdir(folder)
        if file.lower().endswith(ext)
    ]


    undo_dir=os.path.join(folder, "undo.bat")

    with open(undo_dir, "w", encoding="utf-8") as undo_file:
        for i, filename in enumerate(files, start=1):
            current_ext= os.path.splitext(filename)[1].lower()
            new_name= f"{prefix}{i:03}{current_ext}"
            current_dir= os.path.join(folder, filename)
            new_dir= os.path.join(folder, new_name)
            os.rename(current_dir, new_dir)
            undo_file.write(f'rename "{new_name}" "{filename}"\n')
    # Comando para que el mismo archivo .bat se borre
    undo_file.write("del \"%~f0\"\n")


#------------Interfaz-------------#

user = getpass.getuser()

ventana = Tk()
ventana.geometry("400x220")
ventana.resizable(False,False)
ventana.title("Rename files")

Label(ventana, text="Carpeta de trabajo: ").pack(pady=5)

folder_frame=Frame(ventana)
folder_frame.pack()
dir_input=Entry(folder_frame, width=50)
dir_input.pack(padx=5, side=LEFT)
Button(folder_frame,text="Examinar", command=selectFolder).pack(side=RIGHT)

Label(ventana, text="Prefijo de los archivos").pack(padx=5)
prefix_input=Entry(ventana, width=60)
prefix_input.insert(0, "Imagen_")
prefix_input.pack()

Label(ventana, text="Extenciones (separadas por comas)").pack(padx=5)
ext_input=Entry(ventana, width=60)
ext_input.insert(0, ".jpg, .png")
ext_input.pack()

Button(ventana,text="Renombrar", command=renameFiles, bg="#04ba04", fg="white", padx=10).pack(pady=15)

ventana.mainloop()


