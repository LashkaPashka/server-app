from fastapi import UploadFile, APIRouter
import shutil



router = APIRouter(
    prefix='/loading_file',
    tags=['Загрузка файлов']
)


@router.post('/')
async def loading_images(name: int, file: UploadFile):
    with open(f'app/static/images/{name}.jpg', 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)

