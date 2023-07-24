"""Server component for image API."""
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from PIL import Image
from io import BytesIO

load_dotenv()

app = FastAPI(title="Inksplatter API")

@app.get("/image")
async def image():
    image_bytes = BytesIO()
    image = Image.open("image_data/oofycolorful_cloud_hop.jpg")
    image.thumbnail((800, 480))
    image.save(image_bytes, "jpeg")
    return Response(image_bytes.getvalue(), media_type="image/jpeg")
    

@app.get("/")
async def root():
    return {"url": "http://10.0.0.3:8000/image", "title": "Cloud Hop by OofyColorful"}