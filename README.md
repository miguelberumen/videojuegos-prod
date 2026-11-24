# U3 - A3: Pruebas Unitarias en Mini-Proyecto Flask

En esta actividad realicé pruebas unitarias utilizando el módulo `unittest` de Python para comprobar que funcionaran correctamente los modelos, las rutas y la API de mi aplicación de videojuegos desarrollada con Flask.

También utilicé `setUp()` y `tearDown()` para preparar y limpiar el entorno antes y después de cada prueba, evitando que los resultados de una prueba afectaran a las demás.

## Cobertura de las pruebas

Las pruebas se encuentran dentro de la carpeta `tests/`. En total realicé **23 pruebas**, que se pueden ejecutar desde la carpeta principal del proyecto con el siguiente comando:

```bash
python -m unittest discover -v tests
```

- **Modelos (`test_models.py`) – 5 pruebas:**
  - Comprobé la creación y consulta de videojuegos.
  - Probé la actualización del nombre y precio.
  - Verifiqué el registro de usuarios.
  - Comprobé que las contraseñas se guardaran correctamente y pudieran validarse.
  - Verifiqué que no se pudiera acceder directamente a la contraseña.

- **Rutas (`test_routes.py`) – 10 pruebas:**
  - Comprobé el acceso al inicio de sesión y al registro.
  - Verifiqué que las páginas protegidas solicitaran iniciar sesión.
  - Probé el registro y acceso de usuarios.
  - Comprobé el comportamiento cuando los datos de acceso son incorrectos.
  - Probé el registro de videojuegos y el cierre de sesión.

- **API (`test_api.py`) – 8 pruebas:**
  - Comprobé la consulta de todos los videojuegos y de uno en particular.
  - Probé el registro de nuevos videojuegos.
  - Verifiqué la actualización y eliminación de registros.
  - Comprobé las respuestas cuando se envían datos incorrectos o se busca un videojuego que no existe.

## Retos encontrados y soluciones

Durante la realización de las pruebas encontré algunos problemas que tuve que solucionar:

1. **Error al ejecutar la aplicación:** Al principio apareció un error porque no estaba activo el entorno virtual. Lo solucioné activándolo e instalando las dependencias necesarias.

2. **Preparación de la aplicación para las pruebas:** Tuve que organizar `main.py` para poder iniciar la aplicación en modo de pruebas sin afectar su funcionamiento normal.

3. **Base de datos para las pruebas:** Creé una base de datos separada llamada `juegos_test` para evitar modificar o eliminar los datos de mi base de datos principal.

4. **Problema con el inicio de sesión:** Al realizar las pruebas del formulario apareció un problema con la validación CSRF. Lo solucioné desactivando esta validación únicamente en el entorno de pruebas.

5. **Guardado de resultados:** Tuve un problema al guardar los resultados de las pruebas en `results.txt`. Lo solucioné utilizando el comando `2>&1` para guardar también los mensajes de error de la terminal.