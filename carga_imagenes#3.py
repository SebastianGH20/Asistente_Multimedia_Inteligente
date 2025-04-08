import tensorflow as tf

# Carga las imágenes desde las carpetas organizadas por clase
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    'dataset',
    labels='inferred',         # Infere la etiqueta desde el nombre de la carpeta
    label_mode='categorical',  # Puede ser 'int', 'categorical' o 'binary'
    image_size=(224, 224),     # Redimensiona las imágenes
    batch_size=32              # Agrupa en lotes
)

# Mostrar algunas info del dataset
class_names = dataset.class_names
print(f"Clases detectadas: {class_names}")
