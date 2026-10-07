import json
import os

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Notification, Order, Payment, Product
from ..security import get_current_user
from ..services.notification_manager import manager
from ..services.payment_service import create_checkout_session

router = APIRouter(prefix='/api/payments', tags=['payments'])


@router.post('/create-checkout-session')
def create_checkout_session_route(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user['id']).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    session = create_checkout_session(order.id, float(order.total_amount), current_user['email'])
    payment = db.query(Payment).filter(Payment.order_id == order.id).first()
    if payment:
        payment.payment_method = 'stripe'
        payment.amount = order.total_amount
    else:
        payment = Payment(order_id=order.id, amount=order.total_amount, payment_method='stripe', status='PENDING')
        db.add(payment)

    db.commit()
    return {'order_id': order.id, 'checkout_url': session.get('checkout_url'), 'session_id': session.get('session_id')}


@router.post('/webhook')
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    event = None
    signature = request.headers.get('stripe-signature')
    secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    if secret and signature:
        try:
            event = stripe.Webhook.construct_event(payload, signature, secret)
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid Stripe signature')
    else:
        event = json.loads(payload.decode())

    event_type = event.get('type')
    order_data = event.get('data', {}).get('object', {})
    order_id = order_data.get('metadata', {}).get('order_id')
    if not order_id and order_data.get('id'):
        order_id = order_data.get('id')

    if not order_id:
        return {'status': 'ignored', 'message': 'No order id in Stripe event'}

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    payment = db.query(Payment).filter(Payment.order_id == order.id).first()
    if event_type in {'checkout.session.completed', 'payment_intent.succeeded'}:
        order.payment_status = 'PAID'
        order.order_status = 'CONFIRMED'
        if payment:
            payment.status = 'PAID'
            payment.stripe_payment_id = order_data.get('payment_intent') or order_data.get('id')
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock = max(0, product.stock - item.quantity)
        notification = Notification(user_id=order.user_id, type='payment', message='Payment succeeded and order confirmed.', is_read=False)
        db.add(notification)
        await manager.send(order.user_id, {'type': 'payment-success', 'message': notification.message, 'order_id': order.id})
    elif event_type in {'checkout.session.expired', 'payment_intent.payment_failed'}:
        order.payment_status = 'FAILED'
        order.order_status = 'CANCELLED'
        if payment:
            payment.status = 'FAILED'
        notification = Notification(user_id=order.user_id, type='payment', message='Payment failed or was cancelled.', is_read=False)
        db.add(notification)
        await manager.send(order.user_id, {'type': 'payment-failed', 'message': notification.message, 'order_id': order.id})

    db.commit()
    return {'status': 'ok'}


@router.get('/{order_id}')
def payment_details(order_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user['id']).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    payment = db.query(Payment).filter(Payment.order_id == order.id).first()
    return {
        'order_id': order.id,
        'amount': float(order.total_amount),
        'status': order.payment_status,
        'payment_status': order.payment_status,
        'payment': {
            'id': payment.id if payment else None,
            'status': payment.status if payment else 'UNKNOWN',
            'stripe_payment_id': payment.stripe_payment_id if payment else None,
            'created_at': payment.created_at if payment else None,
        },
    }
