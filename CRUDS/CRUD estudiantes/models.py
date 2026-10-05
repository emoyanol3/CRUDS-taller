import json  # Permite trabajar con datos en formato JSON.


# Campos básicos que pertenecen a un estudiante.
CAMPOS_ESTUDIANTES = ("nombre", "apellido", "email", "carnet")


# MODELO: representa los datos y acciones relacionadas con un estudiante.
class Estudiante:
    
    def __init__(
        self,
        id_estudiante,
        nombre,
        apellido,
        email,
        carnet,
        notas=None,
        materias=None
    ):
        """Crea un nuevo objeto Estudiante."""
        self.id = id_estudiante  # Identificador del estudiante.
        self.nombre = nombre  # Nombre del estudiante.
        self.apellido = apellido  # Apellido del estudiante.
        self.email = email  # Correo electrónico.
        self.carnet = carnet  # Código o carnet del estudiante.

        # Guarda las notas agrupadas por materia.
        self.notas = notas if notas else {}

        # Guarda las materias sin permitir repetidas.
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        """Obtiene el nombre completo del estudiante.

        Returns:
            El nombre y apellido unidos en un solo texto.
        """
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        """Inscribe al estudiante en una materia.

        Args:
            materia: Nombre de la materia que se desea agregar.

        Returns:
            None. Solo modifica las materias del estudiante.
        """
        # Los conjuntos no permiten elementos repetidos.
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        """Agrega una nota a una materia.

        Args:
            materia: Nombre de la materia.
            nota: Calificación que se desea registrar.

        Returns:
            None. La nota se agrega al estudiante.
        """
        # Inscribe la materia automáticamente si no existe.
        self.inscribir_materia(materia)

        # Agrega la nota a la lista de esa materia.
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        """Calcula el promedio de todas las notas del estudiante.

        Returns:
            El promedio de las notas redondeado a dos decimales.
        """
        todas = []

        # Recorre las notas de cada materia.
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)

        # Si no existen notas, devuelve 0.
        if not todas:
            return 0

        # Calcula el promedio y lo redondea a dos decimales.
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        """Busca las materias que comparten dos estudiantes.

        Args:
            otro_estudiante: Segundo estudiante con quien se hará la comparación.

        Returns:
            Un conjunto con las materias que tienen en común.
        """
        # El operador & obtiene la intersección de dos conjuntos.
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        """Convierte el estudiante en un diccionario.

        Returns:
            Un diccionario con todos los datos del estudiante.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,

            # JSON no permite guardar conjuntos, por eso se convierte a lista.
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un Estudiante a partir de un diccionario.

        Args:
            datos: Diccionario con los datos del estudiante.

        Returns:
            Un nuevo objeto Estudiante.
        """
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),

            # Convierte nuevamente la lista de materias en un conjunto.
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        """Define cómo se muestra el estudiante al usar print().

        Returns:
            Una cadena con el carnet, nombre completo y promedio.
        """
        return (
            f"[{self.carnet}] "
            f"{self.obtener_nombre_completo()} - "
            f"Promedio: {self.obtener_promedio()}"
        )