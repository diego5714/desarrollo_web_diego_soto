CREATE USER 'java_app_user'@'127.0.0.1' IDENTIFIED BY 'programacionweb';
GRANT SELECT ON tarea2.aviso_adopcion TO 'java_app_user'@'localhost';
GRANT SELECT ON tarea2.comuna TO 'java_app_user'@'localhost';
GRANT SELECT ON tarea2.region TO 'java_app_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON tarea2.nota TO 'java_app_user'@'localhost';
