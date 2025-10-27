from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from src.schemas.products import ProductCreate, ProductResponse, ProductUpdate
from src.controllers.products import ProductController
from src.helpers.api_responses import APIResponses
from typing import List, Optional
from src.repository.product import ProductRepository
from src.utils.cloudinary import upload_images_to_cloudinary



router = APIRouter(prefix="/products", tags=["Products"])
@router.post("/", response_model=ProductResponse)
async def register_product(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    category: List[str] = Form(...),
    thumbnails: Optional[List[UploadFile]] = File(default=None)
):
    try:
        # Subir imágenes a Cloudinary
        urls = []
        if thumbnails:
            urls = await upload_images_to_cloudinary(thumbnails)

        # Crear el objeto pydantic para pasarlo al controller
        product_data = ProductCreate(
            title=title,
            description=description,
            price=price,
            stock=stock,
            category=category,
            thumbnails=urls,
        )

        # Registrar producto
        product = await ProductController.register_product(product_data, urls)
        return product

    except Exception as e:
        print("❌ Error al crear producto:", e)
        raise HTTPException(status_code=500, detail=f"Error creando producto: {e}")

@router.get("/", response_model=List[ProductResponse])
async def get_all_products_in_db():
    try:
        products = await ProductController.get_all_products()
        return [ProductRepository.serialize_product(product) for product in products]
    except Exception as e:
        print("❌ Error exacto al crear product:", e)
        raise HTTPException(status_code=500, detail=f"Error creando product: {e}")

@router.get("/{id}", response_model=ProductResponse)
async def get_one_product_by_id(id: str):
    try:
        product = await ProductController.get_product_by_id(id)
        return ProductRepository.serialize_product(product)
    except Exception as e:
        print("❌ Error exacto al crear product:", e)
        raise HTTPException(status_code=500, detail=f"Error creando product: {e}")

@router.put("/{id}", response_model=ProductResponse)
async def update_one_product(id: str, product_data: ProductUpdate):
    try:
        product = await ProductController.update_product(id, product_data)
        return ProductRepository.serialize_product(product)
    except Exception as e:
        print("❌ Error exacto al crear product:", e)
        raise HTTPException(status_code=500, detail=f"Error creando product: {e}")

@router.delete("/{id}")
async def delete_one_product(id: str):
    try:
        await ProductController.delete_product(id)
        return {"message": "product eliminado correctamente"}
    except Exception as e:
        print("❌ Error exacto al crear product:", e)
        raise HTTPException(status_code=500, detail=f"Error creando product: {e}")