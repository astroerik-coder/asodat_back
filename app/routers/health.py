from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    return {"status": "ok", "message": "Backend funcionando correctamente"}

@router.get("/test")
def test_endpoint():
    return {"status": "ok", "message": "Endpoint de prueba funcionando"}
