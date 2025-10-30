from typing import Optional
from src.models.cart import Cart, CartItem
from src.models.products import Products
from src.helpers.api_responses import DBError
from bson import ObjectId
from beanie import PydanticObjectId

class CartRepository:
    @staticmethod
    def serialize_cart(cart: Cart):
        if not cart:
            return None

        return {
            "_id": str(cart.id),
            "user_id": str(cart.user_id) if cart.user_id else None,
            "items": [
                {
                    "product_id": str(i.product_id) if isinstance(i.product_id, (ObjectId, PydanticObjectId)) else i.product_id,
                    "quantity": i.quantity
                }
                for i in cart.items
            ]
        }

    @staticmethod
    async def get_cart_by_user_id(user_id: str) -> Optional[Cart]:
        try:
            cart = await Cart.find_one(Cart.user_id == ObjectId(user_id))
            if not cart:
                return None

        # 🔹 Forzar rehidratación desde Mongo (vuelve a cargar el doc completo)
            cart = await Cart.get(cart.id)

        # 🔹 Asegurar que los items son instancias de CartItem
            cart.items = [
                i if isinstance(i, CartItem) else CartItem(**i)
                for i in cart.items
            ]

            return cart
        except Exception as e:
            raise DBError(f"Error fetching cart by user_id: {e}")

    @staticmethod
    async def create_cart(user_id: str) -> Cart:
        cart = Cart(user_id=ObjectId(user_id))
        await cart.insert()
        return cart

    @staticmethod
    async def add_item_to_cart(user_id: str, product_id: str, quantity: int):
        try:
        # 🔹 Obtener carrito (o crear uno nuevo)
            cart = await CartRepository.get_cart_by_user_id(user_id)
            if not cart:
                cart = await CartRepository.create_cart(user_id)

        # 🔹 Asegurar que tenemos la versión más reciente del documento
            cart = await Cart.get(cart.id)

            found = False
            for item in cart.items:
                if str(item.product_id) == str(product_id):
                    item.quantity += quantity
                    found = True
                    break

            if not found:
                cart.items.append(
                    CartItem(product_id=ObjectId(product_id), quantity=quantity)
                )

        # 🔹 Guardar correctamente (actualiza el documento completo)
            await cart.save()

        # 🔹 Vuelve a obtener desde la BD para devolverlo actualizado
            updated_cart = await Cart.get(cart.id)
            return updated_cart

        except Exception as e:
            raise DBError(f"Error adding item to cart: {e}")

    @staticmethod
    async def remove_item_from_cart(user_id: str, product_id: str):
        try:
            cart = await CartRepository.get_cart_by_user_id(user_id)
            if not cart:
                return None

        # ✅ Compara como strings
            cart.items = [
                item for item in cart.items
                if str(item.product_id) != str(product_id)
            ]

            await cart.save()

        # ✅ Rehidratar para devolver la versión actualizada
            updated_cart = await Cart.get(cart.id)
            return updated_cart
        except Exception as e:
            raise DBError(f"Error removing item from cart: {e}")

    @staticmethod
    async def clear_cart(user_id: str):
        try:
            cart = await CartRepository.get_cart_by_user_id(user_id)
            if not cart:
                return None

            cart.items = []
            await cart.save()
            return cart
        except Exception as e:
            raise DBError(f"Error clearing cart: {e}")