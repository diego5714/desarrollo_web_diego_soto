from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename
from database.db import AvisoAdopcion, Foto, ContactarPor, SessionLocal, obtener_aviso_por_id, obtener_avisos, obtener_avisos_por_pagina, obtener_foto_por_ids
from utils import validate
from datetime import datetime
import hashlib
import math
import os
import uuid
import filetype  # pyright: ignore[reportMissingTypeStubs]

UPLOAD_FOLDER = 'static/uploads'

app: Flask = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Rutas de la aplicación ###################################################
@app.route('/')
def index() -> str:
    # Obtenemos los ultimos 5 avisos por fecha de publicacion
    avisos: list[AvisoAdopcion] = obtener_avisos(5)
    
    return render_template('index.html', avisos=avisos)

@app.route('/form', methods=["GET", "POST"])
def publication_form() -> str:
    if request.method == "POST":
        # Request POST

        validacion, errores, datos = validate.validar_formulario(request)

        if not validacion:
            # Hubo un error al validar la informacion del formulario
            # Mostramos mensajes de error en la plantilla

            return render_template('form.html', errores=errores, form_data=request.form)

        session: Session = SessionLocal()

        # La validacion fue exitosa, procedemos a crear instancias en base de datos
        try:
            nuevo_aviso: AvisoAdopcion = AvisoAdopcion(
                fecha_ingreso = datetime.now(),
                sector = datos["sector"],
                nombre = datos["nombre"],
                email = datos["email"],
                celular = datos["telefono"],
                tipo = datos["tipo_mascota"],
                cantidad = datos["cantidad"],
                edad = datos["edad"],
                unidad_medida = datos["unidad_edad"],
                fecha_entrega = datos["fecha_entrega"],
                descripcion = datos["descripcion"],
                comuna_id = datos["comuna_id"]
            )

            # Creamos instancias de Foto()
            for foto_storage in datos["fotos_subidas"]:  # pyright: ignore[reportAny]
                _filename = hashlib.sha256(
                    secure_filename(foto_storage.filename).encode("utf-8")  # pyright: ignore[reportAny]
                ).hexdigest()

                _extension = filetype.guess(foto_storage).extension  # pyright: ignore[reportUnknownMemberType, reportAny, reportOptionalMemberAccess]

                img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

                # Guardamos la imagen como archivo
                ruta_guardado: str = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)  # pyright: ignore[reportUnknownArgumentType]
                ruta_relativa: str = os.path.join('uploads', img_filename)
                foto_storage.save(ruta_guardado)    # pyright: ignore[reportAny]
                
                # Creamos instancia de Foto() y la agregamos al aviso
                nueva_foto = Foto(
                    ruta_archivo = ruta_relativa, 
                    nombre_archivo = img_filename
                )
                
                nuevo_aviso.fotos.append(nueva_foto)  # pyright: ignore[reportAny]
            
            # Procesamos y creamos las instancias de ContactarPor()
            
            contactos_info = {
                'whatsapp': datos.get('whatsapp_id'),
                'telegram': datos.get('telegram_id'),
                'twitter': datos.get('twitter_id'),
                'instagram': datos.get('instagram_id'),
                'tiktok': datos.get('tiktok_id'),
                'otra': datos.get('otro_id')
            }

            for nombre_red, identificador in contactos_info.items():
                if identificador:
                    nuevo_contacto: ContactarPor = ContactarPor(
                        nombre = nombre_red,
                        identificador = identificador
                    )
                    
                    nuevo_aviso.contactos.append(nuevo_contacto)  # pyright: ignore[reportAny]

            session.add(nuevo_aviso)
            session.commit()

            #flash("Aviso creado exitosamente", "success")
            return redirect(url_for('index'))  # pyright: ignore[reportReturnType]
        
        except Exception as e:
            # Algo fallo, deshacemos cualquier cambio que se haya hecho
            session.rollback()
            #flash(f"Ocurrió un error al crear el aviso: {e}", "error")
            
            return render_template('form.html', form_data = request.form)

        finally:
            session.close()
        
    
    # Request GET
    return render_template('form.html')


@app.route('/publications')
def publication_list() -> str:
    # Obtenemos el numero de pagina desde la url, si no se especifica 
    # es por defecto 1
    pagina: int = request.args.get('page', 1, type = int)
    avisos_por_pagina = 5

    avisos, items_totales = obtener_avisos_por_pagina(pagina, avisos_por_pagina)

    # Calculamos el total de paginas
    paginas_totales: int = math.ceil(items_totales / avisos_por_pagina)

    return render_template('publication_list.html', avisos = avisos, pagina = pagina, paginas_totales = paginas_totales)

@app.route('/publication/<int:id>')
def publication(id: int) -> str:
    # Obtenemos el aviso asociado al id

    aviso: AvisoAdopcion = obtener_aviso_por_id(id)
    
    return render_template('publication.html', aviso = aviso)

@app.route('/image/<int:aviso_id>/<int:foto_id>')
def image(aviso_id: int, foto_id: int) -> str:
    # Obtenemos la foto en base al id de aviso y de foto

    foto: Foto = obtener_foto_por_ids(aviso_id, foto_id)
    
    return render_template('image.html', foto = foto)

@app.route('/statistics')
def statistics() -> str:
    return render_template('statistics.html')