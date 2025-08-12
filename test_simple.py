#!/usr/bin/env python3
"""
Script simple para test de conexión directa a Supabase PostgreSQL
"""

import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def test_direct_connection():
    """Test de conexión directa usando psycopg2"""
    try:
        print("🔍 Probando conexión directa a Supabase...")
        
        # Obtener la URL de la base de datos
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ Variable DATABASE_URL no encontrada")
            return False
        
        print(f"📡 Conectando a: {database_url.split('@')[1] if '@' in database_url else 'URL oculta'}")
        
        # Conectar directamente
        conn = psycopg2.connect(database_url)
        
        # Crear cursor
        cur = conn.cursor()
        
        # Consulta de prueba
        cur.execute("SELECT 1 as test")
        test_value = cur.fetchone()[0]
        print(f"✅ Consulta de prueba: {test_value}")
        
        # Información de la base de datos
        cur.execute("SELECT current_database()")
        db_name = cur.fetchone()[0]
        print(f"🗄️ Base de datos: {db_name}")
        
        cur.execute("SELECT current_user")
        user = cur.fetchone()[0]
        print(f"👤 Usuario: {user}")
        
        # Verificar tablas existentes
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"📋 Tablas disponibles: {', '.join(tables)}")
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        print("\n🎉 Test de conexión exitoso!")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\nVerifica:")
        print("1. Que el archivo .env esté configurado con DATABASE_URL")
        print("2. Que las credenciales de Supabase sean correctas")
        print("3. Que la base de datos esté accesible")
        return False

if __name__ == "__main__":
    print("🚀 Test de conexión simple ASODAT - Supabase")
    print("=" * 55)
    
    success = test_direct_connection()
    
    if success:
        print("\n✅ La conexión a Supabase está funcionando correctamente")
        exit(0)
    else:
        print("\n❌ Hay problemas con la conexión a Supabase")
        exit(1)
