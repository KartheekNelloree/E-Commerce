from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Notification
from ..security import get_current_user

router = APIRouter(prefix='/api/notifications', tags=['notifications'])


@router.get('')
def list_notifications(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    rows = db.query(Notification).filter(Notification.user_id == current_user['id']).order_by(Notification.created_at.desc()).all()
    return {'items': [
        {
            'id': row.id,
            'user_id': row.user_id,
            'type': row.type,
            'message': row.message,
            'is_read': row.is_read,
            'created_at': row.created_at,
        }
        for row in rows
    ]}


@router.put('/{notification_id}/read')
def mark_as_read(notification_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    row = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user['id']).first()
    if not row:
        raise HTTPException(status_code=404, detail='Notification not found')
    row.is_read = True
    db.commit()
    return {'message': 'Notification marked as read'}
