from aiohttp import web
import aiohttp_cors
from controllers import create_document, get_document


def setup_routes(app, cors):
    # Agregar rutas y configurar CORS
    create_document_route = app.router.add_post('/create', create_document)
    get_document_route = app.router.add_get('/document/{codigo}',  get_document)
    cors.add(create_document_route, {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
    })
    cors.add(get_document_route, {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
    })