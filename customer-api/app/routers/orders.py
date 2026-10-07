from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CartItem, Notification, Order, OrderItem, Payment, Product
from ..security import get_current_user
from ..services.notification_manager import manager

router = APIRouter(prefix='/api/orders', tags=['orders'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_order(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user['id']).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail='Cart is empty')

    total_amount = Decimal('0')
    order_items = []
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product or not product.is_active:
            raise HTTPException(status_code=400, detail=f'Product {cart_item.product_id} is not available')
        if cart_item.quantity > product.stock:
            raise HTTPException(status_code=400, detail=f'Not enough stock for {product.name}')

        total_amount += Decimal(str(product.price)) * cart_item.quantity
        order_items.append({
            'product_id': product.id,
            'product_name': product.name,
            'quantity': cart_item.quantity,
            'unit_price': Decimal(str(product.price)),
        })

    order = Order(
        user_id=current_user['id'],
        total_amount=float(total_amount),
        payment_status='PENDING',
        order_status='PENDING',
    )
    db.add(order)
    db.flush()

    for item in order_items:
        db.add(OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'], unit_price=item['unit_price']))

    db.add(Payment(order_id=order.id, amount=float(total_amount), payment_method='stripe', status='PENDING'))

    notification = Notification(
        user_id=current_user['id'],
        type='order',
        message=f'Order {order.id[:8]} created and awaiting payment confirmation.',
    )
    db.add(notification)
    db.query(CartItem).filter(CartItem.user_id == current_user['id']).delete()
    db.commit()
    db.refresh(order)

    await manager.send(current_user['id'], {
        'type': 'order-created',
        'message': notification.message,
        'order_id': order.id,
    })

    return {'message': 'Order created', 'order_id': order.id, 'total_amount': float(total_amount)}


@router.get('')
def list_orders(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user['id']).order_by(Order.created_at.desc()).all()
    return {
        'items': [
            {
                'id': order.id,
                'user_id': order.user_id,
                'total_amount': float(order.total_amount),
                'payment_status': order.payment_status,
                'order_status': order.order_status,
                'created_at': order.created_at,
            }
            for order in orders
        ]
    }


@router.get('/{order_id}')
def get_order(order_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if order.user_id != current_user['id']:
        raise HTTPException(status_code=403, detail='You can only view your own orders')

    return {
        'id': order.id,
        'user_id': order.user_id,
        'total_amount': float(order.total_amount),
        'payment_status': order.payment_status,
        'order_status': order.order_status,
        'created_at': order.created_at,
        'items': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
            }
            for item in order.items
        ],
    }
