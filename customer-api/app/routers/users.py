from fastapi import APIRouter, Depends

from ..security import get_current_user

router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/me')
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user
