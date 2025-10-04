from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    DateTime,
    Enum,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo = False, future = True)
SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

# Modelos #####################################################################

class Region(Base):
    __tablename__ = 'region'

    # Llave primaria
    id = Column(Integer, primary_key = True, autoincrement = True)
    
    # Otras columnas
    nombre = Column(String(200), nullable = False)

    # Relacion inversa entre region y comuna: Una región puede tener asociada multiples comunas
    comunas = relationship("Comuna", back_populates = "region")

    # Metodo para imprimir y debugear
    def __repr__(self):
        return f"<Region(id={self.id}, nombre='{self.nombre}')>"


class Comuna(Base):
    __tablename__ = 'comuna'

    # Llave primaria
    id = Column(Integer, primary_key = True, autoincrement = True)
    
    # Otras columnas
    nombre = Column(String(200), nullable = False)

    # Llave foránea a Region
    region_id = Column(Integer, ForeignKey('region.id'), nullable = False, index = True)

    # Relación entre Comuna y Region: Una comuna se asocia exactamente a una sola region
    region = relationship("Region", back_populates = "comunas")

    # Relación inversa entre Comuna y AvisoAdopcion: Una comuna puede estar asociada a multiples avisos
    avisos = relationship("AvisoAdopcion", back_populates = "comuna")

    # Metodo para imprimir y debugear
    def __repr__(self):
        return f"<Comuna(id={self.id}, nombre='{self.nombre}')>"


class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'

    # Llave primaria
    id = Column(Integer, primary_key = True, autoincrement = True)

    # Otras columnas
    fecha_ingreso = Column(DateTime, nullable = False)
    sector = Column(String(100), nullable = True)
    nombre = Column(String(200), nullable = False)
    email = Column(String(100), nullable = False)
    celular = Column(String(15), nullable = True)
    tipo = Column(Enum('gato', 'perro'), nullable = False)
    cantidad = Column(Integer, nullable = False)
    edad = Column(Integer, nullable = False)
    unidad_medida = Column(Enum('a', 'm'), nullable = False)
    fecha_entrega = Column(DateTime, nullable = False)
    descripcion = Column(Text, nullable = True)

    # Llave foránea a Comuna
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable = False, index = True)

    # Relación entre AvisoAdopcion y Comuna: Un aviso de adopcion esta asociado exactamente a una comuna
    comuna = relationship("Comuna", back_populates = "avisos")

    # Relación inversa entre AvisoAdopcion y Foto: Un aviso puede estar asociado a multiples fotos
    fotos = relationship("Foto", back_populates = "aviso")

    # Relación inversa entre AvisoAdopcion y ContactarPor: Un aviso puede estar asociado a multiples contactos
    contactos = relationship("ContactarPor", back_populates = "aviso")

    # Método para imprimir y debugear
    def __repr__(self):
        return f"<AvisoAdopcion(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}')>"


class Foto(Base):
    __tablename__ = 'foto'

    # Llave primaria
    # (aviso_id es tambien llave foránea a AvisoAdopcion)
    id = Column(Integer, primary_key = True, autoincrement = True)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key = True, index = True)

    # Otras columnas
    ruta_archivo = Column(String(300), nullable = False)
    nombre_archivo = Column(String(300), nullable = False)

    # Relación entre Foto y AvisoAdopcion: Una foto esta asociada exactamente a un aviso
    aviso = relationship("AvisoAdopcion", back_populates = "fotos")

    # Método para imprimir y debugear
    def __repr__(self):
        return f"<Foto(id={self.id}, nombre_archivo='{self.nombre_archivo}')>"


class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    # Llave primaria
    # (aviso_id es tambien llave foránea a AvisoAdopcion)
    id = Column(Integer, primary_key = True, autoincrement = True)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key = True, index = True)

    # Otras columnas
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable = False)
    identificador = Column(String(150), nullable = False)

    # Relación entre ContactarPor y AvisoAdopcion: Un contacto esta asociado exactamente a un aviso
    aviso = relationship("AvisoAdopcion", back_populates = "contactos")

    # Método para imprimir y debugear
    def __repr__(self):
        return f"<ContactarPor(id={self.id}, nombre='{self.nombre}', identificador='{self.identificador}')>"


# Funciones de la base de datos ##########################################################################################

def obtener_avisos(page_size):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).limit(page_size).all()
    session.close()

    return avisos