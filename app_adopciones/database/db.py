from sqlalchemy import (
    Engine,
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    Text,
    ForeignKey,
    desc,
    func,
)

from sqlalchemy.orm import (
    Session,
    joinedload,
    sessionmaker,
    declarative_base,
    relationship,
)

from datetime import datetime
from typing import override

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL: str = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine: Engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)

Base = declarative_base()  # pyright: ignore[reportAny]

# Modelos ################################################################################################################


class Region(Base):  # pyright: ignore[reportAny]
    __tablename__: str = "region"

    # Llave primaria
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Otras columnas
    nombre: Column[str] = Column(String(200), nullable=False)

    # Relación inversa entre region y comuna: Una región puede tener asociada multiples comunas
    comunas = relationship("Comuna", back_populates="region")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Método para imprimir y hacer debug
    @override
    def __repr__(self) -> str:
        return f"<Region(id={self.id}, nombre='{self.nombre}')>"


class Comuna(Base):  # pyright: ignore[reportAny]
    __tablename__: str = "comuna"

    # Llave primaria
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Otras columnas
    nombre: Column[str] = Column(String(200), nullable=False)

    # Llave foránea a Region
    region_id: Column[int] = Column(
        Integer, ForeignKey("region.id"), nullable=False, index=True
    )

    # Relación entre Comuna y Region: Una comuna se asocia exactamente a una sola region
    region = relationship("Region", back_populates="comunas")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Relación inversa entre Comuna y AvisoAdopcion: Una comuna puede estar asociada a multiples avisos
    avisos = relationship("AvisoAdopcion", back_populates="comuna")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Método para imprimir y hacer debug.
    @override
    def __repr__(self):
        return f"<Comuna(id={self.id}, nombre='{self.nombre}')>"


class AvisoAdopcion(Base):  # pyright: ignore[reportAny]
    __tablename__: str = "aviso_adopcion"

    # Llave primaria
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Otras columnas
    fecha_ingreso: Column[datetime] = Column(DateTime, nullable=False)
    sector: Column[str] = Column(String(100), nullable=True)
    nombre: Column[str] = Column(String(200), nullable=False)
    email: Column[str] = Column(String(100), nullable=False)
    celular: Column[str] = Column(String(15), nullable=True)
    tipo: Column[str] = Column(Enum("gato", "perro"), nullable=False)
    cantidad: Column[int] = Column(Integer, nullable=False)
    edad: Column[int] = Column(Integer, nullable=False)
    unidad_medida: Column[str] = Column(Enum("a", "m"), nullable=False)
    fecha_entrega: Column[datetime] = Column(DateTime, nullable=False)
    descripcion: Column[str] = Column(Text, nullable=True)

    # Llave foránea a Comuna
    comuna_id: Column[int] = Column(
        Integer, ForeignKey("comuna.id"), nullable=False, index=True
    )

    # Relación entre AvisoAdopcion y Comuna: Un aviso de adopción está asociado exactamente a una comuna
    comuna = relationship("Comuna", back_populates="avisos")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Relación inversa entre AvisoAdopcion y Foto: Un aviso puede estar asociado a multiples fotos
    fotos = relationship("Foto", back_populates="aviso")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Relación inversa entre AvisoAdopcion y ContactarPor: Un aviso puede estar asociado a multiples contactos
    contactos = relationship("ContactarPor", back_populates="aviso")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Relación inversa entre AvisoAdopcion y Comentario: Un aviso puede estar asociado a multiples comentarios
    comentarios = relationship("Comentario", back_populates="aviso")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Método para imprimir y hacer debug.
    @override
    def __repr__(self) -> str:
        return (
            f"<AvisoAdopcion(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}')>"
        )


class Foto(Base):  # pyright: ignore[reportAny]
    __tablename__: str = "foto"

    # Llave primaria
    # (aviso_id es también llave foránea a AvisoAdopcion)
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    aviso_id: Column[int] = Column(
        Integer, ForeignKey("aviso_adopcion.id"), primary_key=True, index=True
    )

    # Otras columnas
    ruta_archivo: Column[str] = Column(String(300), nullable=False)
    nombre_archivo: Column[str] = Column(String(300), nullable=False)

    # Relación entre Foto y AvisoAdopcion: Una foto está asociada exactamente a un aviso
    aviso = relationship("AvisoAdopcion", back_populates="fotos")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Método para imprimir y hacer debug.
    @override
    def __repr__(self) -> str:
        return f"<Foto(id={self.id}, nombre_archivo='{self.nombre_archivo}')>"


class ContactarPor(Base):  # pyright: ignore[reportAny]
    __tablename__: str = "contactar_por"

    # Llave primaria
    # (aviso_id es también llave foránea a AvisoAdopcion)
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    aviso_id: Column[int] = Column(
        Integer, ForeignKey("aviso_adopcion.id"), primary_key=True, index=True
    )

    # Otras columnas
    nombre: Column[str] = Column(
        Enum("whatsapp", "telegram", "X", "instagram", "tiktok", "otra"), nullable=False
    )

    identificador: Column[str] = Column(String(150), nullable=False)

    # Relación entre ContactarPor y AvisoAdopcion: Un contacto está asociado exactamente a un aviso
    aviso = relationship("AvisoAdopcion", back_populates="contactos")  # pyright: ignore[reportUnannotatedClassAttribute]

    # Método para imprimir y hacer debug.
    @override
    def __repr__(self) -> str:
        return f"<ContactarPor(id={self.id}, nombre='{self.nombre}', identificador='{self.identificador}')>"


class Comentario(Base):
    __tablename__ = "comentario"

    # Llave primaria
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Llave foránea
    aviso_id: Column[int] = Column(
        Integer, ForeignKey("aviso_adopcion.id"), nullable=False, index=True
    )

    # Otras columnas
    nombre: Column[str] = Column(
        String(80),
        nullable=False,
    )

    texto: Column[str] = Column(String(300), nullable=False)
    fecha: Column[datetime] = Column(DateTime, nullable=False)

    # Relación entre Comentario y AvisoAdopcion: Un comentario está asociado exactamente a un aviso
    aviso = relationship("AvisoAdopcion", back_populates="comentarios")  # pyright: ignore[reportUnannotatedClassAttribute]

    @override
    def __repr__(self) -> str:
        return f"<Comentario(id={self.id}, aviso_id='{self.aviso_id}', nombre='{self.nombre}', texto='{self.texto}', fecha='{self.fecha}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "aviso_id": self.aviso_id,
            "nombre": self.nombre,
            "texto": self.texto,
            "fecha": self.fecha.isoformat(),
        }


# Funciones de la base de datos ##########################################################################################


def obtener_avisos(page_size: int) -> list[AvisoAdopcion]:
    with SessionLocal() as session:
        avisos: list[AvisoAdopcion] = (
            session.query(AvisoAdopcion)
            .options(
                joinedload(AvisoAdopcion.fotos),
                joinedload(AvisoAdopcion.contactos),
                joinedload(AvisoAdopcion.comuna),
            )
            .order_by(desc(AvisoAdopcion.fecha_ingreso))
            .limit(page_size)
            .all()
        )

    return avisos


def obtener_aviso_por_id(id: int) -> AvisoAdopcion | None:
    with SessionLocal() as session:
        aviso: AvisoAdopcion = (
            session.query(AvisoAdopcion)
            .options(
                joinedload(AvisoAdopcion.fotos),
                joinedload(AvisoAdopcion.contactos),
                joinedload(AvisoAdopcion.comuna),
                joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region),
            )
            .filter_by(id=id)
            .first()
        )

    return aviso


def obtener_avisos_por_pagina(
    pagina_idx: int, avisos_por_pagina: int
) -> tuple[list[AvisoAdopcion], int]:
    """Obtiene una lista paginada de avisos y el total de avisos obtenidos en dicha página"""

    with SessionLocal() as session:
        # Calculamos offset
        offset = (pagina_idx - 1) * avisos_por_pagina

        query = (
            session.query(AvisoAdopcion)
            .options(joinedload(AvisoAdopcion.comuna), joinedload(AvisoAdopcion.fotos))
            .order_by(desc(AvisoAdopcion.fecha_ingreso))
        )

        # Obtenemos el total de avisos antes de paginar
        items_totales = session.query(func.count(AvisoAdopcion.id)).scalar()  # pyright: ignore[reportAny]

        # Se aplica límite y offset para obtener solo página actual
        avisos_paginados: list[AvisoAdopcion] = (
            query.limit(avisos_por_pagina).offset(offset).all()
        )

        return avisos_paginados, items_totales


def obtener_foto_por_ids(aviso_id: int, foto_id: int) -> Foto:
    with SessionLocal() as session:
        foto: Foto = (
            session.query(Foto)
            .options(joinedload(Foto.aviso))
            .filter_by(id=foto_id, aviso_id=aviso_id)
            .first()
        )

    return foto


def obtener_comentarios_por_aviso(aviso_id: int) -> list[Comentario]:
    with SessionLocal() as session:
        comentarios: list[Comentario] = (
            session.query(Comentario)
            .options(joinedload(Comentario.aviso))
            .filter_by(aviso_id=aviso_id)
            .order_by(Comentario.fecha.desc())
            .all()
        )

    return comentarios
