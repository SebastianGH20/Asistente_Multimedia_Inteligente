import tmdbsimple as tmdb
import requests
import os

# 👇 Reemplaza 'TU_API_KEY' con la API Key que obtuviste de TMDB
tmdb.API_KEY = '66f858c7b4ee87fc8b1b69d550e9bebb'

# Lista de películas (puedes agregar o cambiar según necesites)
peliculas = ['Inception', 'Interstellar', 'The Matrix', 'The Godfather']

# Carpeta donde se guardarán las imágenes
carpeta_destino = 'portadas'
os.makedirs(carpeta_destino, exist_ok=True)

# Bucle para buscar y descargar la portada de cada película
for titulo in peliculas:
    search = tmdb.Search()
    response = search.movie(query=titulo)

    if search.results:
        poster_path = search.results[0]['poster_path']
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            nombre_archivo = os.path.join(carpeta_destino, f"{titulo}.jpg")
            
            # Descargar la imagen
            img_data = requests.get(image_url).content
            with open(nombre_archivo, 'wb') as handler:
                handler.write(img_data)

            print(f"✅ Descargada portada de '{titulo}'")
        else:
            print(f"⚠️ No hay portada para '{titulo}'")
    else:
        print(f"❌ No se encontró la película '{titulo}'")
