import re
from typing import Any
from filetype import filetype  # pyright: ignore[reportMissingTypeStubs]
from flask import Request
from werkzeug.datastructures.file_storage import FileStorage
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database.db import Comuna, SessionLocal

def validar_region_comuna(region: str | None, comuna: str | None) -> bool:
    """
    Valida si la region es valida, y si la comuna pertenece a la region 
    mediante la base de datos

    Args:
        region (str): El ID de la region recibido del formulario.
        comuna (str): El ID de la comuna recibido del formulario.

    Returns:
        bool: True si la combinación es válida, False en caso contrario
    """
    
    session: Session = SessionLocal()

    try:
        # Convertimos los strings a enteros
        region_id: int = int(region)  # pyright: ignore[reportArgumentType]
        comuna_id: int = int(comuna)  # pyright: ignore[reportArgumentType]

        # Hacemos consulta a la base de datos
        resultado: Comuna | None = session.query(Comuna).filter_by(
            id = comuna_id,
            region_id = region_id
        ).first()

        session.close()
        return resultado is not None
    
    except (ValueError, TypeError):
        # Si hubo algun error al convertir los strings a enteros 
        # la validacion falla
        session.close()
        return False

def validar_sector(sector: str | None) -> bool:
    """Valida que el sector, si es que se proporciona, no exceda los 100 caracteres"""
    
    if sector and len(sector.strip()) > 100:
        return False
    
    return True

def validar_nombre(nombre: str | None) -> bool:
    """Valida que el nombre tenga entre 3 y 200 caracteres"""
    
    if not nombre or not (3 <= len(nombre.strip()) <= 200):
        return False
    
    return True

def validar_email(email: str | None) -> bool:
    """Valida que el email tenga un formato y longitud validos"""

    if not email or len(email.strip()) > 100:
        return False

    # Validamos con regex
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(regex, email.strip()):
        return False

    return True

def validar_telefono(telefono: str | None) -> bool:
    """Valida que el telefono, si se proporciona, tenga un formato valido"""

    if not telefono:
        return True

    # Validamos con regex
    regex = r'^\+\d{3}\.\d{8}$'

    if not re.match(regex, telefono.strip()):
        return False

    return True

def validar_tipo(tipo: str | None) -> bool:
    """Valida que el tipo de mascota sea 'Perro' o 'Gato'"""

    if not tipo or tipo not in ['Perro', 'Gato']:
        return False

    return True

def validar_entero_positivo(valor_str: str | None) -> bool:
    """Valida que un string se pueda convertir a un entero mayor que cero"""

    if not valor_str:
        return False

    try:
        # Intentamos convertr a entero
        valor_int: int = int(valor_str)

        if valor_int <= 0:
            return False
        
    except (ValueError, TypeError):
        # Si hubo algun problema al convertir a entero, devolvemos False
        return False

    return True

def validar_unidad(unidad: str | None) -> bool:
    """Valida que la unidad recibida sea 'Meses' o 'Años'"""

    if not unidad or unidad not in ['Meses', 'Años']:
        return False

    return True

def validar_datetime_futuro(datetime_str: str | None) -> bool:
    """Valida que el datetime sea como minimo 3 horas en el futuro, con un margen de 15 minutos"""

    if not datetime_str:
        return False

    try:
        # Intentamos convertir el string a un objeto datetime
        datetime_usuario: datetime = datetime.fromisoformat(datetime_str)

        # Calculamos el limite estricto de fecha y hora
        datetime_minimo_estricto: datetime = datetime.now() + timedelta(hours = 3)

        # Restamos un margen de tolerancia para permitirles a los usuarios demorarse
        # a lo mas 15 minutos al enviar el formulario
        margen_tolerancia: timedelta = timedelta(minutes = 15)
        datetime_minimo_real: datetime = datetime_minimo_estricto - margen_tolerancia

        if datetime_usuario < datetime_minimo_real:
            return False

    except (ValueError, TypeError):
        # Si hubo algun error al convertir a datetime, retornamos False
        return False

    return True

def validar_contactos(contactos: list[str | None]) -> bool:
    """Valida una lista de identificadores de redes sociales, si es que existe"""

    if not contactos:
        return True

    if len(contactos) > 6:
        return False

    for contacto in contactos:
        # Validamos que cada identificador tenga un largo valido
        if contacto:
            if not (4 <= len(contacto.strip()) <= 50):
                return False
    
    return True

def validar_archivos(archivos: list[FileStorage]) -> bool:
    ALLOWED_EXTENSIONS: set[str] = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_MIMETYPES: set[str] = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    
    if not (1 <= len(archivos) <= 5):
        return False

    # Verificamos que no haya archivos vacios
    if len(archivos) == 1 and archivos[0].filename == '':
        return False

    for archivo in archivos:
        # Validamos el tipo de archivo
        ftype_guess = filetype.guess(archivo)  # pyright: ignore[reportUnknownMemberType]

        if ftype_guess.extension not in ALLOWED_EXTENSIONS:    # pyright: ignore[reportOptionalMemberAccess]
            return False

        if ftype_guess.mime not in ALLOWED_MIMETYPES:  # pyright: ignore[reportOptionalMemberAccess]
            return False

    return True

def validar_formulario(request: Request) -> tuple[bool, list[str], dict[Any, Any]]:  # pyright: ignore[reportExplicitAny]
    """
    Valida la informacion recibida en el formulario del request

    Args: 
        request (Request): El objeto request recibido en la ruta de flask

    Returns:
        bool: True si la validacion fue exitosa, False en caso contrario

    """

    # Obtenemos los datos del formulario

    # Ubicacion
    region: str | None = request.form.get('region')
    comuna: str | None = request.form.get('comuna')
    sector: str | None = request.form.get('sector')
    
    # Contacto
    nombre: str | None = request.form.get('nombre')
    email: str | None = request.form.get('email')
    telefono: str | None = request.form.get('telefono')

    # Redes sociales
    whatsapp_id: str | None = request.form.get('whatsapp-input')
    telegram_id: str | None = request.form.get('telegram-input')
    twitter_id: str | None = request.form.get('twitter-input')
    instagram_id: str | None = request.form.get('instagram-input')
    tiktok_id: str | None = request.form.get('tiktok-input')
    otro_id: str | None = request.form.get('other-input')

    contactos: list[str | None] = []

    contactos.append(whatsapp_id)
    contactos.append(telegram_id)
    contactos.append(twitter_id)
    contactos.append(instagram_id)
    contactos.append(tiktok_id)
    contactos.append(otro_id)

    # Datos mascota
    tipo_mascota: str | None = request.form.get('tipo')
    cantidad: str | None = request.form.get('cantidad')
    edad: str | None = request.form.get('edad')
    unidad_edad: str | None = request.form.get('unidad')
    fecha_entrega: str | None = request.form.get('fecha')    # String con la fecha, ej: '2025-10-04T21:30'
    descripcion: str | None = request.form.get('descripcion') 

    fotos_subidas: list[FileStorage] = request.files.getlist('fotos')

    # Hacemos validacion de datos

    msg: list[str] = []
    valido: bool = True

    if not validar_region_comuna(region, comuna):
        msg.append("La region o la comuna son inválidas")
        valido = False

    if not validar_sector(sector):
        msg.append("El sector ingresado no es válido")
        valido = False

    if not validar_nombre(nombre):
        msg.append("El nombre ingresado no es válido")
        valido = False

    if not validar_email(email):
        msg.append("El correo ingresado no es válido")
        valido = False

    if not validar_telefono(telefono):
        msg.append("El teléfono ingresado no es válido")
        valido = False

    if not validar_contactos(contactos):
        msg.append("Los contactos de redes sociales no son válidos")
        valido = False

    if not validar_tipo(tipo_mascota):
        msg.append("El tipo de mascota ingresado no es válido")
        valido = False

    if not validar_entero_positivo(cantidad):
        msg.append("La cantidad de mascotas ingresada no es válida")
        valido = False

    if not validar_entero_positivo(edad):
        msg.append("La edad ingresada no es válida")
        valido = False
    
    if not validar_unidad(unidad_edad):
        msg.append("La unidad de la edad no es válida")
        valido = False

    if not validar_datetime_futuro(fecha_entrega):
        msg.append("La fecha de entrega no es válida, debe ser al menos 3 horas en el futuro")
        valido = False

    if not validar_archivos(fotos_subidas):
        msg.append("Las fotos subidas o su cantidad no son válidas")
        valido = False

    # Almacenamos los datos convertidos en un diccionario
    datos: dict[Any, Any] = {}  # pyright: ignore[reportExplicitAny]

    if valido:
        datos["region_id"] = int(region)  # pyright: ignore[reportArgumentType]
        datos["comuna_id"] = int(comuna)  # pyright: ignore[reportArgumentType]
        datos["sector"] = str(sector).strip() or None
        datos["nombre"] = str(nombre).strip()
        datos["email"] = str(email).strip()
        datos["telefono"] = str(telefono).strip() or None
        datos["whatsapp_id"] = str(whatsapp_id).strip() or None
        datos["telegram_id"] = str(telegram_id).strip() or None
        datos["twitter_id"] = str(twitter_id).strip() or None
        datos["instagram_id"] = str(instagram_id).strip() or None
        datos["tiktok_id"] = str(tiktok_id).strip() or None
        datos["otro_id"] = str(otro_id).strip() or None
        datos["tipo_mascota"] = str(tipo_mascota).lower()
        datos["cantidad"] = int(cantidad)  # pyright: ignore[reportArgumentType]
        datos["edad"] = int(edad)   # pyright: ignore[reportArgumentType]
        datos["unidad_edad"] = 'm' if unidad_edad == 'Meses' else 'a'
        datos["fecha_entrega"] = datetime.fromisoformat(fecha_entrega)  # pyright: ignore[reportArgumentType]
        datos["descripcion"] = str(descripcion).strip() or None
        datos["fotos_subidas"] = fotos_subidas

    return (valido, msg, datos)
