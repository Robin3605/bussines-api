from src.helpers.api_responses import APIResponses, ConflictError
from src.repository.product import ProductRepository
from src.schemas.products import ProductCreate, ProductUpdate
from fastapi import HTTPException
from src.models.products import Products
import traceback
from src.utils.cloudinary import upload_images_to_cloudinary
from typing import List

class ProductController:
    @staticmethod
    async def register_product(product_data: ProductCreate, image_urls: List[str]):
        try:
            # new_url = await upload_images_to_cloudinary(product_data.thumbnails)    
            new_product = Products(
                title=product_data.title,
                description=product_data.description,
                stock=product_data.stock,
                price=product_data.price,
                category=product_data.category,
                thumbnails=image_urls
            )

            user = await ProductRepository.create_product(new_product)
            
            return user
        except Exception as e:
            print("❌ Error exacto al crear product:")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error creando product: {str(e)}")

    @staticmethod
    async def update_product(id: str, user_data: ProductUpdate):
        try:
            existing = await ProductRepository.get_by_id(id)
            if not existing:
                raise ConflictError("producto no encontrado")

            updated_product = await ProductRepository.update_one(id, user_data)
            return updated_product
        except Exception as e:
            raise APIResponses(500, f"Error al actualizar product: {e}")

    @staticmethod
    async def get_all_products():
        try:
            products = await ProductRepository.get_all()
            if not products:
                raise ConflictError("No hay products creados")
            return products
        except Exception as e:
            raise APIResponses(500, f"Error al obtener products: {e}")

    @staticmethod
    async def get_product_by_id(id: str):
        try:
            product = await ProductRepository.get_by_id(id)
            if not product:
                raise ConflictError("product no encontrado")
            return product
        except Exception as e:
            raise APIResponses(500, f"Error al obtener product: {e}")

    @staticmethod
    async def delete_product(id: str):
        try:
            existing = await ProductRepository.get_by_id(id)
            if not existing:
                raise ConflictError("product no encontrado")

            deleted = await ProductRepository.delete_one(id)
            return True
        except Exception as e:
            raise APIResponses(500, f"Error al eliminar product: {e}")