#!/usr/bin/env python3
"""
Script para probar el endpoint de autenticación
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_auth_components():
    """Prueba los componentes de autenticación"""
    try:
        print("🔍 Probando componentes de autenticación...")
        
        # Importar componentes
        from app.core.config import settings
        print(f"✅ Configuración cargada: JWT_SECRET = {'*' * len(settings.jwt_secret) if settings.jwt_secret else 'NO CONFIGURADO'}")
        
        from app.core.security import create_access_token, create_refresh_token
        print("✅ Funciones de seguridad importadas")
        
        from app.db.models.iniciosesion import InicioSesion
        from app.db.models.socio import Socio
        print("✅ Modelos importados")
        
        from app.schemas.auth import LoginIn
        print("✅ Schemas importados")
        
        # Probar creación de tokens
        test_token = create_access_token("1234567890", "socio")
        print(f"✅ Token de acceso creado: {test_token[:20]}...")
        
        refresh_token, jti = create_refresh_token("1234567890", "socio")
        print(f"✅ Token de refresh creado: {refresh_token[:20]}...")
        
        print("\n🎉 Todos los componentes funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Test de componentes de autenticación ASODAT")
    print("=" * 55)
    
    success = test_auth_components()
    
    if success:
        print("\n✅ Los componentes de autenticación están funcionando")
        sys.exit(0)
    else:
        print("\n❌ Hay problemas con los componentes de autenticación")
        sys.exit(1)
