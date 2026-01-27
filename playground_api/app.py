from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from playground_api.routes import calculations_route, responses_route
from playground_api.settings import Settings

settings = Settings()

app = FastAPI(version=settings.VERSION)


@app.get('/', include_in_schema=False)
def redirect_to_home():
    return RedirectResponse(
        url='/docs', status_code=HTTPStatus.TEMPORARY_REDIRECT
    )


@app.get(
    '/version',
    status_code=HTTPStatus.OK,
)
def version():
    return {'version': settings.VERSION}


app.include_router(responses_route.router)
app.include_router(calculations_route.router)
