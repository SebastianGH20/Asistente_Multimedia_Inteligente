import os
import torch
import open_clip
from PIL import Image
import streamlit as st
from torchvision import transforms
from typing import List

# Configuración
DATASET_DIR = "dataset"

# Función para limpiar nombres
def limpiar_nombre(nombre):
    import re
    import unicodedata
    nombre = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode()
    nombre = re.sub(r'[<>:"/\\|?*]', '', nombre)
    return nombre.strip()

# Cargar modelo y tokenizer
@st.cache_resource
def cargar_modelo():
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
    tokenizer = open_clip.get_tokenizer('ViT-B-32')
    model.eval()
    return model, preprocess, tokenizer

# Obtener lista de títulos desde las carpetas
def cargar_titulos():
    return sorted([limpiar_nombre(d) for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])

# Clasificar imagen contra los títulos
def predecir_pelicula(imagen: Image.Image, titulos: List[str]):
    model, preprocess, tokenizer = cargar_modelo()
    image_input = preprocess(imagen.convert("RGB")).unsqueeze(0)
    text_inputs = tokenizer(titulos)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)

    similarity = (image_features @ text_features.T).softmax(dim=-1)[0]
    resultados = list(zip(titulos, similarity.tolist()))
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados

# Interfaz
st.set_page_config(page_title="Clasificador de Películas 🎬", layout="centered")
st.title("🎞️ Clasificador de portadas con CLIP")
st.write("Sube una imagen de una película y el modelo tratará de adivinar cuál es.")

uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Imagen subida", use_column_width=True)

    with st.spinner("🧠 Analizando..."):
        titulos = cargar_titulos()
        resultados = predecir_pelicula(image, titulos)

    st.success(f"🎯 Predicción final: **{resultados[0][0]}**")
    st.subheader("🔍 Top 3 predicciones:")
    for titulo, score in resultados[:3]:
        st.write(f"- **{titulo}**: {score:.4f}")
