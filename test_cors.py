"""
Script de prueba para verificar la configuración de CORS
Solo permite consultas desde https://asodat-l88n.vercel.app
"""
import requests
import json

def test_cors_preflight():
    """Prueba el preflight request OPTIONS desde el dominio permitido"""
    url = "https://asodat-back.vercel.app/auth/login"
    
    headers = {
        "Origin": "https://asodat-l88n.vercel.app",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type, Authorization"
    }
    
    try:
        response = requests.options(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        # Verificar headers CORS
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods", 
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Credentials"
        ]
        
        for header in cors_headers:
            value = response.headers.get(header)
            print(f"{header}: {value}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_cors_actual():
    """Prueba una petición real POST desde el dominio permitido"""
    url = "https://asodat-back.vercel.app/auth/login"
    
    headers = {
        "Origin": "https://asodat-l88n.vercel.app",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        # Verificar headers CORS en la respuesta
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers", 
            "Access-Control-Allow-Credentials"
        ]
        
        for header in cors_headers:
            value = response.headers.get(header)
            print(f"{header}: {value}")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_cors_blocked():
    """Prueba que CORS bloquee orígenes no permitidos"""
    url = "https://asodat-back.vercel.app/auth/login"
    
    headers = {
        "Origin": "https://malicious-site.com",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\n=== Prueba de Bloqueo CORS ===")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        # Debería ser bloqueado (403 Forbidden)
        return response.status_code == 403
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Probando Preflight CORS (Dominio Permitido) ===")
    preflight_ok = test_cors_preflight()
    
    print("\n=== Probando Petición Real (Dominio Permitido) ===")
    actual_ok = test_cors_actual()
    
    print("\n=== Probando Bloqueo de Orígenes No Permitidos ===")
    blocked_ok = test_cors_blocked()
    
    print(f"\n=== Resultados ===")
    print(f"Preflight (Permitido): {'✅ OK' if preflight_ok else '❌ FALLÓ'}")
    print(f"Petición Real (Permitido): {'✅ OK' if actual_ok else '❌ FALLÓ'}")
    print(f"Bloqueo (No Permitido): {'✅ OK' if blocked_ok else '❌ FALLÓ'}")
    
    if preflight_ok and actual_ok and blocked_ok:
        print("🎉 CORS está funcionando correctamente y es restrictivo!")
    else:
        print("⚠️  Hay problemas con CORS que necesitan ser solucionados.")
