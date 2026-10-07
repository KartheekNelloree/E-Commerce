from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product

router = APIRouter(prefix='/api/products', tags=['products'])


@router.get('')
def list_products(
    search: Optional[str] = Query(default=None),
    category: Optional[str] = None,
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    sort: Optional[str] = 'newest',
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.is_active.is_(True))

    if search:
        like = f'%{search.lower()}%'
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%'),
            )
        )

    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    sort_map = {
        'popularity': Product.popularity_score.desc(),
        'price_asc': Product.price.asc(),
        'price_desc': Product.price.desc(),
        'newest': Product.created_at.desc(),
    }
    query = query.order_by(sort_map.get(sort, Product.created_at.desc()))

    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    return {'items': [
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'stock': item.stock,
            'category': item.category,
            'image_url': item.image_url,
            'popularity_score': item.popularity_score,
            'is_active': item.is_active,
            'created_at': item.created_at,
            'updated_at': item.updated_at,
        }
        for item in items
    ], 'total': total, 'page': page, 'limit': limit}


@router.get('/{product_id}')
def get_product(product_id: str, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Product not found')
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': float(item.price),
        'stock': item.stock,
        'category': item.category,
        'image_url': item.image_url,
        'popularity_score': item.popularity_score,
        'is_active': item.is_active,
        'created_at': item.created_at,
        'updated_at': item.updated_at,
    }
