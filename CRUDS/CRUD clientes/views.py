from pathlib import Path

from models import Cliente, CAMPOS_CLIENTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# Obtiene la carpeta donde se encuentra este proyecto.
BASE_DIR = Path(__file__).resolve().parent

# Define la ubicación del archivo JSON dentro de la carpeta data.
RUTA_CLIENTES = BASE_DIR / "data" / "clientes.json"

# Crea el gestor para leer y guardar los estudiantes.
gestor = GestorJSON(str(RUTA_CLIENTES))


# Campos que deben tener obligatoriamente todos los clientes.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email")

# Campos que se pueden utilizar para realizar búsquedas.
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """
    Obtiene los emails que ya están registrados.

    Args:
        excepto_id: ID que se debe ignorar al comprobar duplicados.

    Returns:
        Un conjunto (set) con los emails registrados.
    """
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    """
    Calcula el siguiente ID disponible para un nuevo cliente.

    Returns:
        El siguiente número de ID disponible.
    """
    # Obtiene todos los IDs registrados.
    ids = [registro["id"] for registro in gestor.leer()]

    # Si existen clientes, toma el ID mayor y suma 1.
    # Si no existen, comienza desde 1.
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_cliente(datos):
    """
    Crea y guarda un nuevo cliente.

    Args:
        datos: Diccionario con los datos del cliente.

    Returns:
        Una tupla (éxito, mensaje), indicando si la operación fue correcta.
    """
    try:
        # Normaliza los datos y elimina espacios innecesarios.
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_CLIENTE
        }

        # Comprueba que todos los campos obligatorios tengan información.
        faltantes = [
            campo for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # Comprueba que el email tenga un formato válido.
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # Comprueba que el email no esté registrado anteriormente.
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        # Crea el objeto Cliente usando los datos del diccionario.
        cliente = Cliente(siguiente_id(), **valores)

        # Obtiene los registros actuales y agrega el nuevo cliente.
        registros = gestor.leer()
        registros.append(cliente.a_diccionario())

        # Guarda nuevamente la lista en el archivo JSON.
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Cliente {cliente.obtener_nombre_completo()} creado con id {cliente.id}"

    except Exception as error:
        # Captura cualquier error inesperado.
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """
    Obtiene todos los clientes registrados.

    Returns:
        Una lista de objetos Cliente.
    """
    # Convierte cada diccionario almacenado en un objeto Cliente.
    return [
        Cliente.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_cliente):
    """
    Busca un cliente utilizando su ID.

    Args:
        id_cliente: ID del cliente que se desea buscar.

    Returns:
        El objeto Cliente encontrado o None si no existe.
    """
    # Recorre todos los clientes hasta encontrar el ID indicado.
    for cliente in obtener_todos():
        if cliente.id == id_cliente:
            return cliente

    # Si no encuentra coincidencias, devuelve None.
    return None


# ===================== S · SEARCH =====================

def buscar_clientes(termino):
    """
    Busca clientes por diferentes campos.

    Args:
        termino: Texto que se desea buscar.

    Returns:
        Lista de objetos Cliente que coinciden con el término.
    """
    # Convierte el término a minúsculas y elimina espacios.
    termino = termino.strip().lower()

    # Si la búsqueda está vacía, devuelve una lista vacía.
    if not termino:
        return []

    encontrados = []

    # Recorre todos los clientes registrados.
    for registro in gestor.leer():

        # Revisa los campos permitidos para la búsqueda.
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():

                # Agrega el cliente si encuentra una coincidencia.
                encontrados.append(
                    Cliente.desde_diccionario(registro)
                )

                # Pasa al siguiente cliente para evitar duplicados.
                break

    return encontrados


# ===================== U · UPDATE =====================

def actualizar_cliente(id_cliente, cambios):
    """
    Actualiza uno o varios campos de un cliente.

    Args:
        id_cliente: ID del cliente que se desea modificar.
        cambios: Diccionario con los campos que se quieren actualizar.

    Returns:
        Una tupla (éxito, mensaje) indicando el resultado.
    """
    try:
        # Detecta campos enviados que no existen en el modelo.
        desconocidos = set(cambios) - set(CAMPOS_CLIENTE)

        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        # Comprueba que se haya enviado al menos un cambio.
        if not cambios:
            return False, "No se indicó ningún cambio"

        # Si se modifica el email, valida su formato y duplicación.
        if "email" in cambios:

            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"

            if cambios["email"].lower() in emails_registrados(excepto_id=id_cliente):
                return False, "Ese email ya lo usa otro cliente"

        registros = gestor.leer()
        posicion = None

        # Busca la posición del cliente dentro de la lista.
        for indice, registro in enumerate(registros):
            if registro["id"] == id_cliente:
                posicion = indice
                break

        # Si no se encontró el ID, informa del error.
        if posicion is None:
            return False, f"No existe un cliente con id {id_cliente}"

        # Actualiza los campos indicados dentro del diccionario.
        registros[posicion].update(cambios)

        # Guarda los cambios en el archivo JSON.
        gestor.guardar(registros)

        return True, f"Cliente {id_cliente} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        # Captura errores inesperados.
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_cliente(id_cliente):
    """
    Elimina un cliente mediante su ID.

    Args:
        id_cliente: ID del cliente que se desea eliminar.

    Returns:
        Una tupla (éxito, mensaje) indicando el resultado.
    """
    registros = gestor.leer()

    # Crea una nueva lista excluyendo al cliente indicado.
    quedan = [
        registro for registro in registros
        if registro["id"] != id_cliente
    ]

    # Si ambas listas tienen el mismo tamaño, el cliente no existía.
    if len(quedan) == len(registros):
        return False, f"No existe un cliente con id {id_cliente}"

    # Guarda la nueva lista sin el cliente eliminado.
    gestor.guardar(quedan)

    return True, f"Cliente {id_cliente} eliminado"


# ===================== EXTRA: estadísticas con conjuntos =====================

def estadisticas():
    """
    Genera estadísticas generales de los clientes.

    Returns:
        Un diccionario con el total, ciudades, dominios de email
        y clientes que no tienen teléfono.
    """
    registros = gestor.leer()

    # Obtiene las ciudades sin repetir.
    ciudades = {
        r.get("ciudad", "").title()
        for r in registros
        if r.get("ciudad")
    }

    # Obtiene los dominios de los emails sin repetir.
    dominios = {
        r["email"].split("@")[1].lower()
        for r in registros
        if "@" in r["email"]
    }

    # Obtiene los nombres de clientes que no tienen teléfono.
    sin_telefono = [
        r["nombre"]
        for r in registros
        if not r.get("telefono")
    ]

    # Devuelve todas las estadísticas en un diccionario.
    return {
        "total": len(registros),
        "ciudades": sorted(ciudades),
        "dominios": sorted(dominios),
        "sin_telefono": sin_telefono,
    }