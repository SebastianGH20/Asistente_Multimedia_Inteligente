import os
import shutil

origen = 'portadas'
destino = 'dataset'

# Crear carpeta de destino si no existe
os.makedirs(destino, exist_ok=True)

# Recorremos las imágenes de la carpeta 'portadas'
for archivo in os.listdir(origen):
    if archivo.endswith('.jpg'):
        nombre_pelicula = archivo.replace('.jpg', '')
        ruta_clase = os.path.join(destino, nombre_pelicula)
        os.makedirs(ruta_clase, exist_ok=True)

        # Mover la imagen a su carpeta correspondiente
        ruta_origen = os.path.join(origen, archivo)
        ruta_destino = os.path.join(ruta_clase, archivo)
        shutil.move(ruta_origen, ruta_destino)

print("✅ Imágenes organizadas por carpeta (una por película).")
