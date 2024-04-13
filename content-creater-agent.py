import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    images = []
    for _ in range(5):  # Generate 5 images sequentially
        response = requests.post(API_URL, headers=headers, json=payload)
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        images.append(image)
    return images

payload = {
    "inputs": "Astronaut riding a horse",
}

images = query(payload)
for idx, img in enumerate(images):
    img.show()  # This will display the images one by one

# Optionally, save images if needed
for i, image in enumerate(images):
    image.save(f'image_{i + 1}.png')
