import os
import time
import re
import tmdbsimple as tmdb
import requests
import tensorflow as tf
import unicodedata

# CONFIGURACIÓN
API_KEY = '66f858c7b4ee87fc8b1b69d550e9bebb'
tmdb.API_KEY = API_KEY

DATASET_DIR = 'dataset'
os.makedirs(DATASET_DIR, exist_ok=True)

NUM_PAGINAS = 50  # 5 páginas x 20 películas = 100 portadas
IMAGEN_SIZE = (224, 224)
BATCH_SIZE = 32

descargadas = 0

# ✅ Función para limpiar nombres inválidos en carpetas de Windows
def limpiar_nombre(nombre):
    # Normaliza caracteres (elimina tildes, diéresis, etc.)
    nombre = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode()
    # Reemplaza espacios y caracteres conflictivos
    nombre = re.sub(r'[<>:"/\\|?*]', '', nombre)
    nombre = nombre.strip()
    return nombre

print("📥 Paso 1: Descargando portadas de TMDB...\n")

for pagina in range(1, NUM_PAGINAS + 1):
    print(f"🔄 Página {pagina}...")
    popular = tmdb.Movies().popular(page=pagina)

    for pelicula in popular['results']:
        titulo_original = pelicula['title']
        titulo_limpio = limpiar_nombre(titulo_original)
        poster_path = pelicula['poster_path']

        if not poster_path:
            print(f"⚠️ Sin imagen: {titulo_original}")
            continue

        carpeta_pelicula = os.path.join(DATASET_DIR, titulo_limpio)
        os.makedirs(carpeta_pelicula, exist_ok=True)
        nombre_archivo = os.path.join(carpeta_pelicula, f"{titulo_limpio}.jpg")

        if os.path.exists(nombre_archivo):
            print(f"🔁 Ya existe: {titulo_original}")
            continue

        try:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            img_data = requests.get(image_url, timeout=10).content
            with open(nombre_archivo, 'wb') as handler:
                handler.write(img_data)
            print(f"✅ Guardado: {titulo_original}")
            descargadas += 1
        except Exception as e:
            print(f"❌ Error con {titulo_original}: {e}")

        time.sleep(0.2)  # Pausa por respeto a la API

print(f"\n🎉 Se descargaron {descargadas} portadas en total.")

# -------------------------------------
# 🧠 Paso 2: Cargar el dataset con TensorFlow
# -------------------------------------

print("\n📚 Paso 2: Cargando dataset desde carpeta 'dataset'...")

dataset = tf.keras.preprocessing.image_dataset_from_directory(
    DATASET_DIR,
    labels='inferred',
    label_mode='categorical',
    image_size=IMAGEN_SIZE,
    batch_size=BATCH_SIZE
)

print(f"\n✅ Dataset cargado con {len(dataset.class_names)} clases:")
print(dataset.class_names)
