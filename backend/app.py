from aiohttp import web
import aiohttp_cors
from dotenv import load_dotenv
import motor.motor_asyncio
import os

from routes import setup_routes

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de MongoDB desde las variables de entorno
mongodb_url = os.getenv("MONGODB_URL")

#Conexion a la DB
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
db = client['documentos']


# Configuración y ejecución de la aplicación web
app = web.Application()

# poner en contexto de la aplicacion la base de datos
app['db'] = db

# Configurar CORS
cors = aiohttp_cors.setup(app)
setup_routes(app, cors)

web.run_app(app)