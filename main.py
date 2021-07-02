from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    documented_routes = []
    for r in app.routes:
        if not r.path == "/":
            documented_routes.append(r)
    openapi_schema = get_openapi(
        title="SAP RFC Bridge",
        version="1.0.0",
        description="Provides a bridge to communicate with SAP ECC",
        routes=documented_routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def read_root():
    return RedirectResponse("/docs")


from routers.call import router as call_router

app.include_router(call_router)