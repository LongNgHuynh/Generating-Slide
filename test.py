from models.LLMs import GPT_4o
from PIL import Image
import os
import base64
import io

def pil_to_base64(image):
    """Convert PIL image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")

def get_image_description(image_path, llm, resize_to=(512, 512)):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at: {image_path}")
    
    # Open and resize the image
    image = Image.open(image_path).convert("RGB")  # Ensure consistent mode
    image = image.resize(resize_to)

    base64_image = pil_to_base64(image)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the content of this image in detail."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    response = llm.invoke(messages)
    return response

# Example usage
image_path = "./data/Overview_of_AI_4.jpg"
llm = GPT_4o()
results = get_image_description(image_path, llm)
print(results)
