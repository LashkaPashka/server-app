from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.hotels.router import get_data



router = APIRouter(
    prefix='/templates',
    tags=['Фронтенд']
)

jinja2 = Jinja2Templates(directory='app/pages/templates')


@router.get('/')
async def send_template(request: Request, hotels=Depends(get_data)):
    context = {'request': request, 'hotels': hotels}
    return jinja2.TemplateResponse(name='hotel.html', context=context)








