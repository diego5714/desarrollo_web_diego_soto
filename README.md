# Diego Soto: Desarrollo de Aplicaciones Web
Repositorio para las tareas del ramo CC5002 Desarrollo de Aplicaciones Web (FCFM UChile)

## Descripción:

- Este repositorio implementa funcionalidades básicas de una aplicación web de adopciones de mascotas, usando el framework SpringBoot y la base de datos MySQL.
- En particular, se implementa lectura de avisos de adopción, y asignación de notas o calificaciones por parte de los usuarios.
- Para correr una versión mas completa implementada con Flask, por favor elegir una branch anterior a Tarea-4

## Ejecución:

- Para ejecutar la aplicación desde una terminal con bash:
    1. Asegurarse de contar con el JDK 25 de Java, y que se encuentre en el PATH del sistema.

    2. Cambiar el directorio de la terminal a ```app_adopciones/```
        ```bash
            cd app_adopciones/
        ```

    3. Asegurarse de que se tiene corriendo el servidor de MySQL y que es posible conectarse a él con las siguientes configuraciones
        - host: 127.0.0.1
        - puerto: 3306
        - username: root
        - password: [Contraseña usada para crear el servidor]

    4. Una vez hecho lo anterior, ejecutar el siguiente comando para entrar en la consola de MySQL:
        ```bash
            mysql -h 127.0.0.1 -u root -p
        ```

    5. Una vez dentro, ejecutar al menos los siguientes scripts en orden desde la carpeta ```database/```:
        ```bash
            source database/tarea2.sql;
            source database/region-comuna.sql;
            source database/tabla-nota.sql;
        ```
        
          Notar que esta branch no ofrece ninguna forma directa a traves de la APP de crear entrada en la base de datos para avisos de adopción. Se recomienda cargar la branch Tarea-3, generar la base de datos según indica ese README.md, poblarla con entradas mediante la app de Flask, y luego cambiar de vuelta a esta branch para ejecutar esta aplicación.
          
          El script que si es importante ejecutar es el siguiente:
          ```bash
            source database/create_java_user.sql;
          ```
          
          Este script crea un usuario "java_app_user" con los permisos suficientes para leer las tablas que requiere la app.

    6. Salir de la consola de MySQL:
        ```bash
            EXIT;
        ```

    7. Finalmente ejecutar la aplicación web con el siguiente comando desde la carpeta ```app_adopciones/```:
        ```bash
            chmod +x mvnw
            ./mvnw spring-boot:run
        ```
        Si se corre Linux o Mac 
        
        ```powershell
            .\mvnw.cmd spring-boot:run
        ```
        Si se corre en Windows con powershell

    - La app estará disponible en: http://127.0.0.1:8080
