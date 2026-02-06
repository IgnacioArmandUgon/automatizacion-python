import os 

dir="C:/automatizacion-python/archivos-prueba-renombrar"
prefix="image_"
ext=(".jpg", ".png")

files= [
    file for file in os.listdir(dir)
    if file.lower().endswith(ext)
]


undo_dir=os.path.join(dir, "undo.bat")

with open(undo_dir, "w", encoding="utf-8") as undo_file:
    for i, filename in enumerate(files, start=1):
        current_ext= os.path.splitext(filename)[1].lower()
        new_name= f"{prefix}{i:03}{current_ext}"
        current_dir= os.path.join(dir, filename)
        new_dir= os.path.join(dir, new_name)
        os.rename(current_dir, new_dir)
        undo_file.write(f'rename "{new_name}" "{filename}"\n')
# Comando para que el mismo archivo .bat se borre
undo_file.write("del \"%~f0\"\n")