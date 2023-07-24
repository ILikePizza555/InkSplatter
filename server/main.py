import base64
import httpx

from fastapi import FastAPI
from google.cloud import vision
from io import BytesIO
from PIL import Image
from urllib.parse import unquote

app = FastAPI()

def get_crop_hints(image_bytes: bytes, aspect_ratios: list[float] = [1.66]):
    vision_client = vision.ImageAnnotatorClient()

    image = vision.Image(image_bytes)
    crop_hints_params = vision.CropHintsParams(aspect_ratios=aspect_ratios)
    image_context = vision.ImageContext(crop_hints_params=crop_hints_params)

    response = vision_client.crop_hints(image=image, image_context=image_context)
    hint = response.crop_hints_annotation.crop_hints[0]
    verticies = [(v.get("x", 0), v.get("y", 0)) for v in hint.boundingPoly.vertices]

    return {
        "verticies": verticies,
        "confidence": hint.confidence,
        "importanceFraction": hint.importanceFraction
    }

app.get("/")
async def get_image(image_url: str):
    async with httpx.AsyncClient() as client:
        img_url_response = await client.get(unquote(image_url))
        img_url_response.raise_for_status()

    crop_hints = get_crop_hints(img_url_response.content)

    image = Image.open(img_url_response.content)
    response_image_bytes = BytesIO()
    image.crop((*crop_hints[0], *crop_hints[2])).save(response_image_bytes, format="jpeg")

    return {
        image: base64.b64encode(response_image_bytes.getvalue())
    }