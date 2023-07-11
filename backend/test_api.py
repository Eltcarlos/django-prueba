import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
import json

from app import create_document, get_document

@pytest.fixture
async def test_client(aiohttp_client):
    app = web.Application()
    app.router.add_post('/create', create_document)
    app.router.add_get('/document/{codigo}', get_document)
    client = await aiohttp_client(app)
    return client

async def test_create_document(test_client):
    data = {
        'nombre': 'carlos',
        'apellido': 'diaz',
        'edad': '21',
        'telefono': '123456789',
        'correo': 'carlosdiaz@example.com'
    }

    resp = await test_client.post('/create', data=json.dumps(data))

    assert resp.status == 200
    assert resp.content_type == 'application/json'

    result = await resp.json()
    assert result['success'] is True
    assert 'codigo' in result
    assert 'message' in result

async def test_get_document(test_client):
    data = {
        'nombre': 'John',
        'apellido': 'Doe',
        'edad': 30,
        'telefono': '123456789',
        'correo': 'john.doe@example.com'
    }

    # Crear el documento
    resp_create = await test_client.post('/create', data=json.dumps(data))
    assert resp_create.status == 200
    result_create = await resp_create.json()
    assert result_create['success'] is True
    codigo = result_create['codigo']

    # Obtener el documento
    resp_get = await test_client.get(f'/document/{codigo}')
    assert resp_get.status == 200
    assert resp_get.content_type == 'application/json'
    result_get = await resp_get.json()
    assert result_get['success'] is True
    assert 'documento' in result_get

async def test_get_document_not_found(test_client):
    codigo = 'invalid_codigo'

    resp = await test_client.get(f'/document/{codigo}')
    assert resp.status == 200
    assert resp.content_type == 'application/json'
    result = await resp.json()
    assert result['success'] is False
    assert 'message' in result

