from fastapi import APIRouter, Depends, HTTPException
from src.controllers.cart import CartController
from src.schemas.cart import AddItemRequest, CartResponse
from src.helpers.jwt import get_current_user  # si tienes auth

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartResponse)
async def get_my_cart(current_user=Depends(get_current_user)):
    cart = await CartController.get_cart(current_user.id)
    return cart

@router.post("/add", response_model=CartResponse)
async def add_item_to_cart(
    data: AddItemRequest,
    current_user=Depends(get_current_user)
):
    cart = await CartController.add_item(current_user.id, data.product_id, data.quantity)
    return cart

@router.delete("/remove/{product_id}", response_model=CartResponse)
async def remove_item_from_cart(product_id: str, current_user=Depends(get_current_user)):
    cart = await CartController.remove_item(current_user.id, product_id)
    return cart

@router.delete("/clear", response_model=CartResponse)
async def clear_cart(current_user=Depends(get_current_user)):
    cart = await CartController.clear(current_user.id)
    return cart