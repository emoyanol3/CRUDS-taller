from pathlib import Path

from models import Estudiante, CAMPOS_ESTUDIANTES
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# Obtiene la carpeta donde se encuentra este proyecto.
BASE_DIR = Path(__file__).resolve().parent

# Define la ubicación del archivo JSON dentro de la carpeta data.
RUTA_ESTUDIANTES = BASE_DIR / "data" / "estudiantes.json"

# Crea el gestor para leer y guardar los estudiantes.
gestor = GestorJSON(str(RUTA_ESTUDIANTES))


# Campos que deben tener obligatoriamente todos los estudiantes.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")


# Campos que se pueden utilizar para realizar búsquedas.
CAMPOS_BUSCABLES = (
    "nombre",
    "apellido",
    "email",
    "carnet",
    "materias"
)


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """Obtiene los emails que ya están registrados.
    Args:
        excepto_id: ID que se debe ignorar al comprobar duplicados.
    Returns:
        Un conjunto con los emails registrados.
    """
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    """Calcula el siguiente ID disponible para un nuevo estudiante.
    Returns:
        El siguiente número de ID disponible.
    """
    ids = [registro["id"] for registro in gestor.leer()]

    # Si existen estudiantes, toma el ID mayor y suma 1.
    # Si no existen, comienza desde 1.
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """Crea y guarda un nuevo estudiante.
    Args:
        datos: Diccionario con los datos del estudiante.
    Returns:
        Una tupla (éxito, mensaje).
    """
    try:
        # Normaliza los datos y elimina espacios innecesarios.
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_ESTUDIANTES
        }

        # Comprueba que los campos obligatorios tengan información.
        faltantes = [
            campo for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # Comprueba que el email tenga un formato válido.
        if not es_email_valido(valores["email"]):
            return False, (
                f"El email '{valores['email']}' "
                f"no tiene un formato válido"
            )

        # Comprueba que el email no esté registrado anteriormente.
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        # Crea el objeto Estudiante.
        estudiante = Estudiante(siguiente_id(), **valores)

        # Obtiene los registros actuales y agrega el nuevo estudiante.
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())

        # Guarda la lista actualizada.
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, (
            f"Estudiante {estudiante.obtener_nombre_completo()} "
            f"creado con id {estudiante.id}"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """Obtiene todos los estudiantes registrados.
    Returns:
        Una lista de objetos Estudiante.
    """
    return [
        Estudiante.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_estudiante):
    """Busca un estudiante utilizando su ID.
    Args:
        id_estudiante: ID del estudiante que se desea buscar.
    Returns:
        El objeto Estudiante encontrado o None.
    """
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante

    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    """Busca estudiantes por diferentes campos.
    Args:
        termino: Texto que se desea buscar.
    Returns:
        Lista de estudiantes que coinciden con el término.
    """
    termino = termino.strip().lower()

    if not termino:
        return []

    encontrados = []

    # Recorre todos los estudiantes registrados.
    for registro in gestor.leer():

        # Revisa los campos permitidos para la búsqueda.
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():

                encontrados.append(
                    Estudiante.desde_diccionario(registro)
                )

                # Evita agregar al mismo estudiante dos veces.
                break

    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza uno o varios campos de un estudiante.
    Args:
        id_estudiante: ID del estudiante que se desea modificar.
        cambios: Diccionario con los campos que se quieren actualizar.
    Returns:
        Una tupla (éxito, mensaje).
    """
    try:
        # Detecta campos que no existen en el modelo.
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTES)

        if desconocidos:
            return False, (
                f"Campos no válidos: {', '.join(sorted(desconocidos))}"
            )

        if not cambios:
            return False, "No se indicó ningún cambio"

        # Si se modifica el email, valida su formato y duplicación.
        if "email" in cambios:

            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"

            if cambios["email"].lower() in emails_registrados(
                excepto_id=id_estudiante
            ):
                return False, "Ese email ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None

        # Busca la posición del estudiante.
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, (
                f"No existe un estudiante con id {id_estudiante}"
            )

        # Actualiza los datos indicados.
        registros[posicion].update(cambios)

        # Guarda los cambios.
        if not gestor.guardar(registros):
            return False, "No se pudieron guardar los cambios"

        return True, (
            f"Estudiante {id_estudiante} actualizado "
            f"({len(cambios)} campo/s)"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


def actualizar_nota(id_estudiante, materia, numero_nota, nueva_nota):
    """
    Actualiza una nota existente de un estudiante.

    Args:
        id_estudiante: ID del estudiante.
        materia: Nombre de la materia.
        numero_nota: Posición de la nota que se desea modificar.
        nueva_nota: Nueva calificación.

    Returns:
        Una tupla (éxito, mensaje).
    """
    try:
        # Normaliza el nombre de la materia.
        materia = materia.strip().lower()

        if not materia:
            return False, "La materia no puede estar vacía"

        # Convierte los datos numéricos a sus tipos correspondientes.
        try:
            numero_nota = int(numero_nota)
            nueva_nota = float(nueva_nota)
        except ValueError:
            return False, "El número de nota y la nueva nota deben ser números"

        # Las notas empiezan desde la posición 1 para el usuario.
        if numero_nota < 1:
            return False, "El número de nota debe ser mayor que 0"

        # Comprueba que la nueva nota esté dentro del rango permitido.
        if nueva_nota < 0 or nueva_nota > 10:
            return False, "La nota debe estar entre 0 y 10"

        registros = gestor.leer()

        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                estudiante = Estudiante.desde_diccionario(registro)

                # Comprueba que la materia exista.
                if materia not in estudiante.notas:
                    return False, (
                        f"El estudiante no tiene notas registradas en {materia}"
                    )

                notas = estudiante.notas[materia]

                # Comprueba que exista la nota indicada.
                if numero_nota > len(notas):
                    return False, (
                        f"La materia {materia} solo tiene "
                        f"{len(notas)} nota(s)"
                    )

                # Guarda la nota anterior para mostrarla en el mensaje.
                nota_anterior = notas[numero_nota - 1]

                # Actualiza la nota.
                notas[numero_nota - 1] = nueva_nota

                # Actualiza el registro del estudiante.
                registros[indice] = estudiante.a_diccionario()

                if not gestor.guardar(registros):
                    return False, "No se pudo guardar la nota"

                return True, (
                    f"Nota {numero_nota} de {materia} actualizada: "
                    f"{nota_anterior} → {nueva_nota}"
                )

        return False, (
            f"No existe un estudiante con id {id_estudiante}"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"



# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante mediante su ID.
    Args:
        id_estudiante: ID del estudiante que se desea eliminar.
    Returns:
        Una tupla (éxito, mensaje).
    """
    registros = gestor.leer()

    # Crea una nueva lista excluyendo al estudiante indicado.
    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    # Si ambas listas tienen el mismo tamaño, no existía el estudiante.
    if len(quedan) == len(registros):
        return False, (
            f"No existe un estudiante con id {id_estudiante}"
        )

    # Guarda la lista sin el estudiante eliminado.
    if not gestor.guardar(quedan):
        return False, "No se pudo guardar la eliminación"

    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== MATERIAS =====================

def agregar_materia(id_estudiante, materia):
    """Inscribe un estudiante en una materia.
    Args:
        id_estudiante: ID del estudiante.
        materia: Nombre de la materia.
    Returns:
        Una tupla (éxito, mensaje).
    """
    try:
        # Elimina espacios innecesarios.
        materia = materia.strip().lower()

        if not materia:
            return False, "La materia no puede estar vacía"

        registros = gestor.leer()

        # Busca al estudiante.
        for registro in registros:
            if registro["id"] == id_estudiante:

                # Convierte el registro en un objeto Estudiante.
                estudiante = Estudiante.desde_diccionario(registro)

                # Comprueba si ya está inscrito.
                if materia in estudiante.materias:
                    return False, (
                        f"El estudiante ya está inscrito en {materia}"
                    )

                # Utiliza el método del modelo.
                estudiante.inscribir_materia(materia)

                # Actualiza el registro.
                registros[registros.index(registro)] = (
                    estudiante.a_diccionario()
                )

                # Guarda los cambios.
                if not gestor.guardar(registros):
                    return False, "No se pudo guardar la materia"

                return True, (
                    f"Materia '{materia}' agregada correctamente"
                )

        return False, (
            f"No existe un estudiante con id {id_estudiante}"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== NOTAS =====================

def agregar_nota(id_estudiante, materia, nota):
    """Registra una nota para un estudiante.
    Args:
        id_estudiante: ID del estudiante.
        materia: Nombre de la materia.
        nota: Calificación que se desea registrar.
    Returns:
        Una tupla (éxito, mensaje).
    """
    try:
        materia = materia.strip().lower()

        if not materia:
            return False, "La materia no puede estar vacía"

        # Convierte la nota a número.
        try:
            nota = float(nota)
        except ValueError:
            return False, "La nota debe ser un número"

        # Comprueba que la nota esté dentro de un rango válido.
        if nota < 0 or nota > 10:
            return False, "La nota debe estar entre 0 y 10"

        registros = gestor.leer()

        # Busca al estudiante.
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:

                estudiante = Estudiante.desde_diccionario(registro)

                # Agrega la nota usando el método del modelo.
                estudiante.agregar_nota(materia, nota)

                # Actualiza el registro.
                registros[indice] = estudiante.a_diccionario()

                # Guarda los cambios.
                if not gestor.guardar(registros):
                    return False, "No se pudo guardar la nota"

                return True, (
                    f"Nota {nota} agregada a {materia}"
                )

        return False, (
            f"No existe un estudiante con id {id_estudiante}"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"