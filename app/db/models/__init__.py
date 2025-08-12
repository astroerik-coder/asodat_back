# Importaciones de todos los modelos para facilitar el acceso
from .socio import Socio, TipoUsuario
from .aportes import Aportes, AportesSocios
from .comprobante import ComprobantePago
from .cupo import CupoSocio
from .historial_aportes import HistorialAportes
from .historial_carga_aportes import HistorialCargaAportes
from .historial_eliminaciones import HistorialEliminaciones
from .noticia import Noticia
from .refresh_token import RefreshToken
from .password_reset import PasswordResetToken
from .iniciosesion import InicioSesion
from .usuario import Usuario

# Lista de todos los modelos para facilitar operaciones masivas
__all__ = [
    "Socio",
    "TipoUsuario", 
    "Aportes",
    "AportesSocios",
    "ComprobantePago",
    "CupoSocio",
    "HistorialAportes",
    "HistorialCargaAportes",
    "HistorialEliminaciones",
    "Noticia",
    "RefreshToken",
    "PasswordResetToken",
    "InicioSesion",
    "Usuario"
]
