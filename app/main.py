from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routers import auth, me, socios, eliminaciones
from .routers import aportes as aportes_router
from .routers import reportes as reportes_router
from .routers import validaciones

app = FastAPI(
    title="ASODAT API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Swagger "Authorize" (JWT Bearer) ------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="API ASODAT",
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    for path in openapi_schema.get("paths", {}).values():
        for op in path.values():
            op.setdefault("security", [{"bearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ------------------ Routers ------------------
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(socios.router)
app.include_router(eliminaciones.router)
app.include_router(aportes_router.router)
app.include_router(reportes_router.router)
app.include_router(validaciones.router)
