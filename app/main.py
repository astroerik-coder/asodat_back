from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routers import auth, me, socios, eliminaciones
from .routers import aportes as aportes_router
from .routers import reportes as reportes_router
from .routers import validaciones, health

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

# ------------------ Health Check ------------------
@app.get("/")
async def root():
    return {"message": "ASODAT API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is working correctly"}

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
app.include_router(health.router)

# ------------------ Debug endpoint to see registered routes ------------------
@app.get("/debug/routes")
async def debug_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    
    # Agrupar rutas por categoría
    auth_routes = [r for r in routes if r["path"].startswith("/auth")]
    me_routes = [r for r in routes if r["path"].startswith("/me")]
    socios_routes = [r for r in routes if r["path"].startswith("/socios")]
    aportes_routes = [r for r in routes if r["path"].startswith("/aportes")]
    eliminaciones_routes = [r for r in routes if r["path"].startswith("/eliminaciones")]
    reportes_routes = [r for r in routes if r["path"].startswith("/reportes")]
    validaciones_routes = [r for r in routes if r["path"].startswith("/validaciones")]
    health_routes = [r for r in routes if r["path"].startswith("/health")]
    other_routes = [r for r in routes if not any(r["path"].startswith(prefix) for prefix in ["/auth", "/me", "/socios", "/aportes", "/eliminaciones", "/reportes", "/validaciones", "/health"])]
    
    return {
        "total_routes": len(routes),
        "routes_by_category": {
            "auth": auth_routes,
            "me": me_routes,
            "socios": socios_routes,
            "aportes": aportes_routes,
            "eliminaciones": eliminaciones_routes,
            "reportes": reportes_routes,
            "validaciones": validaciones_routes,
            "health": health_routes,
            "other": other_routes
        },
        "all_routes": routes
    }

# ------------------ Catch-all route for debugging ------------------
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(path: str):
    return {
        "message": f"Route /{path} not found",
        "available_routes": {
            "auth": [
                "/auth/login",
                "/auth/refresh", 
                "/auth/logout",
                "/auth/password/forgot",
                "/auth/password/reset",
                "/auth/password/change"
            ],
            "me": [
                "/me/datos",
                "/me/aportes"
            ],
            "socios": [
                "/socios/",
                "/socios/{cedula}"
            ],
            "aportes": [
                "/aportes/",
                "/aportes/{cedula}"
            ],
            "eliminaciones": [
                "/eliminaciones/",
                "/eliminaciones/{id}"
            ],
            "reportes": [
                "/reportes/socios",
                "/reportes/aportes",
                "/reportes/comprobantes"
            ],
            "validaciones": [
                "/validaciones/cedula/{cedula}"
            ],
            "health": [
                "/health/",
                "/health/test"
            ],
            "docs": [
                "/api/docs",
                "/api/openapi.json"
            ],
            "debug": [
                "/debug/routes"
            ]
        },
        "path": path,
        "tip": "Use /debug/routes to see all available routes"
    }
