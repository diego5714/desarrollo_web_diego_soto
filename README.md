# desarrollo_web_diego_soto
Repositorio para las tareas del ramo CC5002 Desarrollo de Aplicaciones Web (FCFM UChile)

## Descripción:

- Este repositorio implementa una simple aplicación web de adopciones de mascotas, usando el framework Flask y la base de datos MySQL

## Ejecución:

- Para ejecutar la aplicación desde una terminal con bash:
    1. Crear un entorno virtual de Python:
        ```bash
            python -m venv venv
        ```

    2. Activar el entorno
        ```bash
            source venv/bin/activate
        ```

    3. Cambiar el directorio de la terminal a ```app_adopciones/```
        ```bash
            cd app_adopciones/
        ```

    4. Instalar los paquetes requeridos de Python
        ```bash
            pip install -r requirements.txt
        ```

    5. Asegurarse de que se tiene corriendo el servidor de MySQL y que es posible conectarse a él con las siguientes configuraciones
        - host: localhost
        - puerto: 3306 
        - username: root 
        - password: [Contraseña usada para crear el servidor]

    6. Una vez hecho lo anterior, ejecutar el siguiente comando para entrar en la consola de MySQL:
        ```bash
            mysql -u root -p
        ```

    7. Una vez dentro, ejecutar los siguientes scripts en orden desde la carpeta ```database/```:
        ```bash
            source database/create_user.sql;
            source database/tarea2.sql;
            source database/region_comuna.sql;
            source database/grant_user_permissions.sql
        ``` 

    8. Salir de la consola de MySQL:
        ```bash
            EXIT;
        ```

    9. Finalmente ejecutar la aplicación web con el siguiente comando desde la carpeta ```app_adopciones/```:
        ```bash
            flask run
        ```
    
    - La app estará disponible en: http://127.0.0.1:5000