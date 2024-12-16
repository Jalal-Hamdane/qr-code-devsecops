from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()

import qrcode
import boto3
import uuid
import os
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration CORS
origins = [
    "http://localhost:3000",  # Frontend local
    "http://127.0.0.1:3000"  # Autres variantes locales
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autorisez le frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME", "votre-bucket-s3")

# Log des variables d'environnement AWS pour vérifier leur présence
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    logger.error("AWS credentials are missing. Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
if BUCKET_NAME == "votre-bucket-s3":
    logger.warning("Using default bucket name 'votre-bucket-s3'. Check your BUCKET_NAME environment variable.")

# Initialisation du client S3
try:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    logger.info("S3 client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize S3 client: {e}")

# Modèle de requête
class URLRequest(BaseModel):
    url: str

@app.post("/api/generate")
async def generate_qr_code(request: URLRequest):
    logger.info(f"Received URL: {request.url}")

    try:
        # Étape 1 : Génération du QR Code
        qr = qrcode.QRCode()
        qr.add_data(request.url)
        qr.make(fit=True)
        logger.debug("QR Code data added successfully.")

        img = qr.make_image(fill="black", back_color="white")
        file_name = f"{uuid.uuid4()}.png"
        img.save(file_name)
        logger.info(f"QR Code saved as file: {file_name}")

        # Étape 2 : Téléchargement sur S3
        try:
            s3_client.upload_file(file_name, BUCKET_NAME, file_name)
            logger.info(f"File {file_name} uploaded to S3 bucket {BUCKET_NAME} successfully.")
        except Exception as s3_error:
            logger.error(f"Failed to upload {file_name} to S3: {s3_error}")
            raise HTTPException(status_code=500, detail=f"Failed to upload {file_name} to S3: {s3_error}")

        # Étape 3 : Génération de l'URL
        s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        logger.info(f"S3 URL generated: {s3_url}")

        # Suppression du fichier local
        os.remove(file_name)
        logger.debug(f"Local file {file_name} deleted successfully.")

        # Retour du résultat
        return {"qrCodeUrl": s3_url}

    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
