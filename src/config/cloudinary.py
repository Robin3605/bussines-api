import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()  # 👈 muy importante, debe ir antes de config()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)