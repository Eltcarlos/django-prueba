from aiohttp import web
import aiohttp_cors
import base64
import random
import string
from io import BytesIO
from reportlab.pdfgen import canvas
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://eltcarlosfn:GVC1L8IXf0czgQSn@cluster0.airfnju.mongodb.net/python')
db = client['documentos']

async def create_document(request):
    try:
        data = await request.json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        edad = data.get('edad')
        telefono = data.get('telefono')
        correo = data.get('correo')

        # Generar código único de 10 dígitos
        characters = string.ascii_letters + string.digits
        codigo = ''.join(random.choices(characters, k=10))

        # Editar la plantilla PDF con los datos proporcionados
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(100, 750, 'Chelita Software Full Stack Test')
        c.setFont('Helvetica', 12)

        c.drawString(100, 700, f"Nombre: {nombre}")
        c.drawString(100, 680, f"Apellido: {apellido}")
        c.drawString(100, 660, f"Edad: {edad}")
        c.drawString(100, 640, f"Teléfono: {telefono}")
        c.drawString(100, 620, f"Correo: {correo}")
        c.save()

        # Obtener el contenido del PDF en base64
        pdf_content = pdf_buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Guardar el documento en la base de datos
        documento = {
            'codigo': codigo,
            'contenido': pdf_base64
        }
        await db.documentos.insert_one(documento)

        return web.json_response({'success': True, 'codigo': codigo, 'message': 'Se ha creado correctamente'})
    except Exception as e:
        return web.json_response({'success': False, 'message': 'Ha ocurrido un error al crear el documento'})

async def get_document(request):
    codigo = request.match_info.get('codigo')

    documento = await db.documentos.find_one({'codigo': codigo})

    if documento:
        return web.json_response({'success': True, 'documento': documento['contenido']})
    else:
        return web.json_response({'success': False, 'message': 'No se ha encontrado el documento'})



app = web.Application()

# Configurar CORS
cors = aiohttp_cors.setup(app)
create_document_route = app.router.add_post('/create', create_document)
get_document_route = app.router.add_get('/document/{codigo}', get_document)
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

web.run_app(app)