import os
import torch
import open_clip
from PIL import Image
from torchvision import transforms

# 1. Cargar modelo CLIP
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
model.eval()

# 2. Obtener clases (nombres de las carpetas del dataset)
DATASET_PATH = 'dataset'
titulos = [nombre for nombre in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, nombre))]
print(f"🎬 Películas disponibles para clasificar: {titulos}")

# 3. Preguntar por imagen a clasificar
imagen_path = input("📷 Ingresa la ruta de la imagen a clasificar: ").strip()

# 4. Verificar que la imagen exista
if not os.path.exists(imagen_path):
    print("❌ No se encontró la imagen. Verifica la ruta.")
    exit()

# 5. Procesar imagen
try:
    image = preprocess(Image.open(imagen_path).convert("RGB")).unsqueeze(0)
except Exception as e:
    print(f"❌ Error al cargar la imagen: {e}")
    exit()

# 6. Embeddings y comparación
text_inputs = tokenizer(titulos)

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text_inputs)

# 7. Similaridad
similarity = (image_features @ text_features.T).softmax(dim=-1)[0]

# 8. Resultados ordenados
resultados = list(zip(titulos, similarity.tolist()))
resultados.sort(key=lambda x: x[1], reverse=True)

print("\n🔍 Resultados de predicción:")
for titulo, score in resultados:
    print(f"{titulo}: {score:.4f}")

print(f"\n🎯 Predicción final: {resultados[0][0]}")
