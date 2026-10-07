from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import ALLOWED_ORIGINS, DEV_MODE
from .database import Base, engine
from .models import *  # noqa: F401,F403
from .routers.cart import router as cart_router
from .routers.notifications import router as notifications_router
from .routers.orders import router as orders_router
from .routers.payments import router as payments_router
from .routers.products import router as products_router
from .routers.users import router as users_router
from .routers.ws import router as websocket_router

app = FastAPI(title='Smart E-Commerce Customer API', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)


@app.on_event('startup')
def startup():
    Base.metadata.create_all(bind=engine)


@app.get('/')
def root():
    return {'message': 'Smart E-Commerce API is running', 'dev_mode': DEV_MODE}


@app.get('/health')
def health():
    return {'status': 'ok'}


app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(notifications_router)
app.include_router(users_router)
app.include_router(websocket_router)
