from src.repository.cart import CartRepository
from src.helpers.api_responses import APIResponses, ConflictError
from src.schemas.cart import CartResponse

class CartController:

    @staticmethod
    async def get_cart(user_id: str):
        try:
            cart = await CartRepository.get_cart_by_user_id(user_id)
            if not cart:
                cart = await CartRepository.create_cart(user_id)

            # Serializa aquí (strings en product_id / user_id)
            serialized = CartRepository.serialize_cart(cart)
            return CartResponse(**serialized)
        except Exception as e:
            raise APIResponses(500, f"Error obteniendo carrito: {e}")

    @staticmethod
    async def add_item(user_id: str, product_id: str, quantity: int):
        try:
            cart = await CartRepository.add_item_to_cart(user_id, product_id, quantity)
            serialized = CartRepository.serialize_cart(cart)
            return CartResponse(**serialized)
        except Exception as e:
            raise APIResponses(500, f"Error agregando producto al carrito: {e}")

    @staticmethod
    async def remove_item(user_id: str, product_id: str):
        try:
            cart = await CartRepository.remove_item_from_cart(user_id, product_id)
            serialized = CartRepository.serialize_cart(cart)
            return CartResponse(**serialized)
        except Exception as e:
            raise APIResponses(500, f"Error eliminando producto del carrito: {e}")

    @staticmethod
    async def clear(user_id: str):
        try:
            cart = await CartRepository.clear_cart(user_id)
            serialized = CartRepository.serialize_cart(cart)
            return CartResponse(**serialized)
        except Exception as e:
            raise APIResponses(500, f"Error limpiando carrito: {e}")