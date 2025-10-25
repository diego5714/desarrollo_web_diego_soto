from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from werkzeug import Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures.file_storage import FileStorage

from database.db import (
    AvisoAdopcion,
    Comentario,
    Foto,
    ContactarPor,
    SessionLocal,
    obtener_aviso_por_id,
    obtener_avisos,
    obtener_avisos_por_pagina,
    obtener_foto_por_ids,
    obtener_comentarios_por_aviso,
)

from utils import validate
from datetime import datetime
import hashlib
import math
import os
import uuid
import filetype  # pyright: ignore[reportMissingTypeStubs]

UPLOAD_FOLDER = "static/uploads"

app: Flask = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Rutas de la aplicación ###################################################
@app.route("/")
def index() -> str:
    # Obtenemos los últimos 5 avisos por fecha de publicación
    avisos: list[AvisoAdopcion] = obtener_avisos(5)

    return render_template("index.html", avisos=avisos)


@app.route("/form", methods=["GET", "POST"])
def publication_form() -> str | Response:
    if request.method == "POST":
        # Request POST

        validacion, errores, datos_str, datos_int, fotos, fecha = (
            validate.validar_formulario_publicacion(request)
        )

        if not validacion:
            # Hubo un error al validar la información del formulario
            # Mostramos mensajes de error en la plantilla

            print("Error de validacion")
            print(errores)
            return render_template("form.html", errores=errores, form_data=request.form)

        session: Session = SessionLocal()

        # La validacion fue exitosa, procedemos a crear instancias en base de datos
        try:
            nuevo_aviso: AvisoAdopcion = AvisoAdopcion(
                fecha_ingreso=datetime.now(),
                sector=datos_str["sector"],
                nombre=datos_str["nombre"],
                email=datos_str["email"],
                celular=datos_str["telefono"],
                tipo=datos_str["tipo_mascota"],
                cantidad=datos_int["cantidad"],
                edad=datos_int["edad"],
                unidad_medida=datos_str["unidad_edad"],
                fecha_entrega=fecha,
                descripcion=datos_str["descripcion"],
                comuna_id=datos_int["comuna_id"],
            )

            # Creamos instancias de Foto()
            for foto_storage in fotos:
                _filename = hashlib.sha256(
                    secure_filename(foto_storage.filename).encode("utf-8")
                ).hexdigest()

                _extension = filetype.guess(foto_storage).extension

                img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

                # Guardamos la imagen como archivo
                ruta_guardado: str = os.path.join(
                    app.config["UPLOAD_FOLDER"], img_filename
                )

                ruta_relativa: str = os.path.join("uploads", img_filename)
                foto_storage.save(ruta_guardado)

                # Creamos instancia de Foto() y la agregamos al aviso
                nueva_foto = Foto(
                    ruta_archivo=ruta_relativa, nombre_archivo=img_filename
                )

                nuevo_aviso.fotos.append(nueva_foto)  # pyright: ignore[reportAny]

            # Procesamos y creamos las instancias de ContactarPor()

            contactos_info = {
                "whatsapp": datos_str.get("whatsapp_id"),
                "telegram": datos_str.get("telegram_id"),
                "X": datos_str.get("twitter_id"),
                "instagram": datos_str.get("instagram_id"),
                "tiktok": datos_str.get("tiktok_id"),
                "otra": datos_str.get("otro_id"),
            }

            for nombre_red, identificador in contactos_info.items():
                if identificador:
                    nuevo_contacto: ContactarPor = ContactarPor(
                        nombre=nombre_red, identificador=identificador
                    )

                    nuevo_aviso.contactos.append(nuevo_contacto)  # pyright: ignore[reportAny]

            session.add(nuevo_aviso)
            session.commit()

            # flash("Aviso creado exitosamente", "success")
            return redirect(url_for("index"))

        except Exception as e:
            # Algo fallo, deshacemos cualquier cambio que se haya hecho
            session.rollback()
            # flash(f"Ocurrió un error al crear el aviso: {e}", "error")

            print(f"ERROR DURANTE LA INSERCIÓN: {e}")

            return render_template("form.html", form_data=request.form)

        finally:
            session.close()

    # Request GET
    return render_template("form.html")


@app.route("/publications")
def publication_list() -> str:
    # Obtenemos el número de página desde la url, si no se especifica
    # es por defecto 1
    pagina: int = request.args.get("pagina", 1, type=int)
    avisos_por_pagina = 5

    avisos, items_totales = obtener_avisos_por_pagina(pagina, avisos_por_pagina)

    # Calculamos el total de páginas
    paginas_totales: int = math.ceil(items_totales / avisos_por_pagina)

    return render_template(
        "publication_list.html",
        avisos=avisos,
        pagina=pagina,
        paginas_totales=paginas_totales,
    )


@app.route("/publication/<int:id>", methods=["GET", "POST"])
def publication(id: int) -> str | Response:
    # Obtenemos el aviso asociado al ID
    aviso: AvisoAdopcion = obtener_aviso_por_id(id)

    if request.method == "POST":
        # Procesar la solicitud POST para agregar el comentario
        validacion, errores, datos = validate.validar_formulario_comentario(request)

        if not validacion:
            # Hubo un error al validar la información del formulario
            # Mostramos mensajes de error en la plantilla

            print("Error de validacion")
            print(errores)
            return render_template(
                "publication.html", aviso=aviso, errores=errores, form_data=request.form
            )

        print("El comentario fue validado correctamente")

        session: Session = SessionLocal()

        # La validacion fue exitosa, procedemos a crear instancias en base de datos
        try:
            if aviso is None:
                raise ValueError("El aviso no existe")

            nuevo_comentario: Comentario = Comentario(
                aviso_id=aviso.id,
                nombre=datos["nombre"],
                texto=datos["comentario"],
                fecha=datetime.now(),
                aviso=aviso,
            )

            session.add(nuevo_comentario)
            session.commit()

            # flash("Aviso creado exitosamente", "success")
            return render_template("publication.html", aviso=aviso, exito=True)

        except Exception as e:
            # Algo falló, deshacemos cualquier cambio que se haya hecho
            session.rollback()
            # flash(f"Ocurrió un error al crear el aviso: {e}", "error")

            print(f"ERROR DURANTE LA INSERCIÓN: {e}")

            errores: list[str] = []
            errores.append(f"Ocurrió un error inesperado al crear el comentario: {e}")

            return render_template("publication.html", aviso=aviso, errores=errores)

        finally:
            session.close()

    return render_template("publication.html", aviso=aviso)


@app.route("/image/<int:aviso_id>/<int:foto_id>")
def image(aviso_id: int, foto_id: int) -> str:
    # Obtenemos la foto basándonos en el ID del aviso y de la foto

    foto: Foto = obtener_foto_por_ids(aviso_id, foto_id)

    return render_template("image.html", foto=foto)


@app.route("/statistics")
def statistics() -> str:
    return render_template("statistics.html")


