from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CartItem, Product
from ..schemas import CartItemPayload
from ..security import get_current_user

router = APIRouter(prefix='/api/cart', tags=['cart'])


@router.get('')
def get_cart(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    rows = db.query(CartItem).filter(CartItem.user_id == current_user['id']).all()
    return {
        'items': [
            {
                'id': row.id,
                'product_id': row.product_id,
                'quantity': row.quantity,
                'product_name': row.product.name,
                'product_price': float(row.product.price),
                'image_url': row.product.image_url,
            }
            for row in rows
        ]
    }


@router.post('/items', status_code=status.HTTP_201_CREATED)
def add_item(payload: CartItemPayload, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    if not product.is_active:
        raise HTTPException(status_code=400, detail='Product is inactive')
    if payload.quantity > product.stock:
        raise HTTPException(status_code=400, detail='Not enough stock available')

    item = db.query(CartItem).filter(CartItem.user_id == current_user['id'], CartItem.product_id == payload.product_id).first()
    if item:
        item.quantity = item.quantity + payload.quantity
        item.updated_at = None
    else:
        item = CartItem(user_id=current_user['id'], product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)

    db.commit()
    return {'message': 'Item added to cart', 'product_id': payload.product_id, 'quantity': payload.quantity}


@router.put('/items/{product_id}')
def update_item(product_id: str, quantity: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if quantity < 1:
        raise HTTPException(status_code=400, detail='Quantity must be at least 1')

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    if quantity > product.stock:
        raise HTTPException(status_code=400, detail='Not enough stock available')

    item = db.query(CartItem).filter(CartItem.user_id == current_user['id'], CartItem.product_id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Cart item not found')

    item.quantity = quantity
    db.commit()
    return {'message': 'Cart item updated', 'product_id': product_id, 'quantity': quantity}


@router.delete('/items/{product_id}')
def remove_item(product_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.user_id == current_user['id'], CartItem.product_id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Cart item not found')
    db.delete(item)
    db.commit()
    return {'message': 'Item removed from cart'}


@router.delete('')
def clear_cart(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db.query(CartItem).filter(CartItem.user_id == current_user['id']).delete()
    db.commit()
    return {'message': 'Cart cleared'}
