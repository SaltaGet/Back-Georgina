from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config.logging_config import setup_logging
from src.middleware.timing import TimingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.database.db import db
import logging
from src.routers.user_router import user_router
from src.routers.blog_router import blog_router

# db = DataBase()

setup_logging()

app = FastAPI(title= 'API Fundación Convivir',
            description='API Fundación Convivir',
            version='0.0.1',
            docs_url='/',
            )

app.include_router(router= user_router)
app.include_router(router= blog_router)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TimingMiddleware)

# app.add_middleware(AuthMiddleware)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if db.is_closed():
        try:
            # await db.create_database_if_not_exists()   #QUITAR ESTA LINEA PARA MYSQL
            await db.connect()
        except Exception as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            raise e
    await db.create_tables()
    yield
    if not db.is_closed():
        await db.close()
        logging.info("El servidor se está cerrando.")


app.router.lifespan_context = lifespan
