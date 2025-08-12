"""
Configuración de CORS para la aplicación ASODAT
"""
import os
from typing import List

def get_cors_origins() -> List[str]:
    """
    Obtiene la lista de orígenes permitidos para CORS
    Solo permite el dominio específico de ASODAT
    """
    raw_origins = os.getenv("CORS_ORIGINS", "https://asodat-l88n.vercel.app")
    
    # Si se especifica "*", usar solo el dominio de ASODAT
    if raw_origins.strip() == "*":
        return ["https://asodat-l88n.vercel.app"]
    
    # Si se especifican orígenes específicos, dividirlos por comas
    origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
    
    # Asegurar que el dominio de ASODAT esté siempre incluido
    asodat_domain = "https://asodat-l88n.vercel.app"
    if asodat_domain not in origins:
        origins.append(asodat_domain)
    
    return origins

def get_cors_headers() -> List[str]:
    """
    Obtiene la lista de headers permitidos para CORS
    """
    return [
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Cache-Control",
        "Pragma"
    ]

def get_cors_methods() -> List[str]:
    """
    Obtiene la lista de métodos HTTP permitidos para CORS
    """
    return [
        "GET",
        "POST", 
        "PUT",
        "DELETE",
        "OPTIONS",
        "PATCH"
    ]
