import json
import os


class GestorJSON:
    """Gestiona la lectura y escritura de datos en un archivo JSON."""

    def __init__(self, ruta):
        self.ruta = ruta  # Guarda la ubicación del archivo JSON.

        carpeta = os.path.dirname(ruta)  # Obtiene la carpeta donde estará el archivo.

        # Crea la carpeta si todavía no existe.
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        # Si el archivo no existe, devuelve una lista vacía.
        if not os.path.exists(self.ruta):
            return []

        try:
            # Abre el archivo y carga su contenido como datos de Python.
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            # Verifica que los datos sean una lista antes de devolverlos.
            return datos if isinstance(datos, list) else []

        except (json.JSONDecodeError, OSError):
            # Si ocurre un error al leer, devuelve una lista vacía.
            return []

    def guardar(self, datos):
        try:
            # Abre el archivo en modo escritura y guarda los datos en JSON.
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)

            return True  # Indica que los datos se guardaron correctamente.

        except (TypeError, OSError):
            # Si los datos no son compatibles o hay un error de archivo, devuelve False.
            return False