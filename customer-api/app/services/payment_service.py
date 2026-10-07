import os

import stripe


stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')


def create_checkout_session(order_id: str, total_amount: float, customer_email: str):
    if not stripe.api_key:
        return {
            'checkout_url': 'https://example.com/mock-checkout',
            'mode': 'test',
            'order_id': order_id,
            'amount': total_amount,
            'customer_email': customer_email,
        }

    try:
        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[{'price_data': {'currency': 'usd', 'unit_amount': int(total_amount * 100), 'product_data': {'name': f'Order {order_id}'}}, 'quantity': 1}],
            customer_email=customer_email,
            success_url='http://localhost:5173/checkout?status=success',
            cancel_url='http://localhost:5173/checkout?status=cancelled',
            metadata={'order_id': order_id},
        )
        return {'checkout_url': session.url, 'session_id': session.id, 'order_id': order_id}
    except Exception:
        return {'checkout_url': 'https://example.com/mock-checkout', 'mode': 'fallback', 'order_id': order_id}
