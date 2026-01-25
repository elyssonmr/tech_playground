from http import HTTPStatus

from fastapi import FastAPI

from playground_api.settings import Settings

settings = Settings()

app = FastAPI(version=settings.VERSION)


@app.get(
    '/version',
    status_code=HTTPStatus.OK,
)
def version():
    return {'version': settings.VERSION}
