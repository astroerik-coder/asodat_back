"""
Middleware personalizado para la aplicación ASODAT
"""
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

logger = logging.getLogger(__name__)

class CORSMiddlewareCustom(BaseHTTPMiddleware):
    """
    Middleware personalizado para manejar CORS de manera restrictiva
    Solo permite el dominio específico de ASODAT
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.allowed_origin = "https://asodat-l88n.vercel.app"
    
    async def dispatch(self, request: Request, call_next):
        # Log de la petición para debugging
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Origin: {request.headers.get('origin', 'No origin')}")
        
        # Verificar si el origen está permitido
        origin = request.headers.get("origin")
        if origin and origin != self.allowed_origin:
            logger.warning(f"Origen no permitido: {origin}")
            return JSONResponse(
                content={"error": "Origin not allowed"},
                status_code=403
            )
        
        # Manejar preflight OPTIONS
        if request.method == "OPTIONS":
            response = JSONResponse(
                content={"message": "OK"},
                status_code=200
            )
            
            # Headers CORS solo para el dominio permitido
            response.headers["Access-Control-Allow-Origin"] = self.allowed_origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Origin, Accept"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Max-Age"] = "86400"
            
            return response
        
        # Continuar con la petición normal
        response = await call_next(request)
        
        # Agregar headers CORS solo para el dominio permitido
        if origin == self.allowed_origin:
            response.headers["Access-Control-Allow-Origin"] = self.allowed_origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Origin, Accept"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response
