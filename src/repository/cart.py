from typing import Optional
from src.models.cart import Cart, CartItem
from src.models.products import Products
from src.helpers.api_responses import DBError
from bson import ObjectId

class CartRepository:
    @staticmethod
    def serialize_cart(cart):
        data = cart.dict()
        data["_id"] = str(cart.id)
        data["user_id"] = str(cart.user_id)
        data.pop("id", None)
        return data

    @staticmethod
    async def get_cart_by_user_id(user_id: str) -> Optional[Cart]:
        return await Cart.find_one(Cart.user_id ==  ObjectId(user_id))

    @staticmethod
    async def create_cart(user_id: str) -> Cart:
        cart = Cart(user_id=user_id)
        await cart.insert()
        return cart

    @staticmethod
    async def add_item_to_cart(user_id: str, product_id: str, quantity: int):
        try:
            cart = await CartRepository.get_cart_by_user_id(user_id)
            if not cart:
                cart = await CartRepository.create_cart(user_id)

            # Buscar si el producto ya está en el carrito
            for item in cart.items:
                if item.product_id == product_id:
                    item.quantity += quantity
                    break
            else:
                cart.items.append(CartItem(product_id=product_id, quantity=quantity))

            await cart.save()
            return cart
        except Exception as e:
            raise DBError(f"Error adding item to cart: {e}")

    @staticmethod
    async def remove_item_from_cart(user_id: str, product_id: str):
        try:
            cart = await CartRepository.get_cart_by_user_id(user_id)
            if not cart:
                return None

            cart.items = [item for item in cart.items if item.product_id != product_id]
            await cart.save()
            return cart
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