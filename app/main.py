import time

from app.importer.router import router as router_importer
import sentry_sdk
from fastapi import FastAPI, Depends
from typing import Optional
from httpx import Request
from fastapi_versioning import VersionedFastAPI
from pydantic import BaseModel
from datetime import date
from CORS.router import router as router_check
from app.admin.auth import authentication_backend
from app.logger import logger
from app.users.models import Users
from app.bookings.router import router as router_booking
from app.users.router import router as router_register
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_templates
from fastapi.staticfiles import StaticFiles
from app.image.images import router as router_images
from app.database import engine
from sqladmin import Admin
from app.admin.admin import UserAdmin, BookingsAdmin, RoomAdmin, HotelsAdmin




app = FastAPI()


app.include_router(router_booking)
app.include_router(router_register)
app.include_router(router_hotels)
app.include_router(router_templates)
app.include_router(router_images)
app.include_router(router_check)
app.include_router(router_importer)



app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')
app.mount('/static', StaticFiles(directory='app/static'), 'static')


sentry_sdk.init(
    dsn="https://5d5f8e59493f56f01110cceb62dd9922@o4505895321403392.ingest.sentry.io/4505895322648576",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)



class Sargs:
    def __init__(
            self,
            name: str,
            data_to: date,
            data_from: date,
            stars: str
    ):
        self.name = name
        self.data_to = data_to
        self.data_from = data_from
        self.stars = stars


class SHoutel(BaseModel):
    name: str
    data_to: date
    data_from: date
    star: Optional[bool] = False


@app.get('/')
def hotel(srgs: SHoutel = Depends()) -> list[SHoutel]:

    hotel = [
        {
         'name': 'Plaza',
         'data_to': '2020-05-25',
         'data_from': '2020-06-04',
        }
    ]

    return hotel


class Sbooking(BaseModel):
    role_id: int
    date_from: date
    date_to: date


@app.post('/')
def add_hotel(booking: Sbooking):
    return f'Status 200 | Response {booking}'





admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(BookingsAdmin)
admin.add_view(UserAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelsAdmin)




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info('process_time', extra={
        'process_time': round(process_time, 4)
    })
    return response


