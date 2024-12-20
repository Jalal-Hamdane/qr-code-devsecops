from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import qrcode
import boto3
import uuid
import os

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Configuration CORS
origins = ["http://localhost:3001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autorise uniquement le frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de requête
class URLRequest(BaseModel):
    url: str

# Route de test
@app.get("/")
async def root():
    return {"message": "Backend is running and ready to generate QR codes!"}

# Route principale pour générer un QR code
@app.post("/api/generate")
async def generate_qr_code(request: URLRequest):
    try:
        # Étape 1 : Génération du QR Code
        qr = qrcode.QRCode()
        qr.add_data(request.url)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        file_name = f"{uuid.uuid4()}.png"
        img.save(file_name)

        # Étape 2 : Téléchargement sur S3
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        bucket_name = os.getenv("BUCKET_NAME", "default-bucket")
        s3_client.upload_file(file_name, bucket_name, file_name)

        # Étape 3 : Génération de l'URL du QR Code
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        os.remove(file_name)

        return {"qrCodeUrl": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
