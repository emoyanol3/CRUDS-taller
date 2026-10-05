import os
# "os" es un módulo estándar de Python que permite interactuar
# con el sistema operativo, por ejemplo, limpiar la pantalla.

# DICCIONARIO: relaciona cada nombre de color con su código de consola.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}
# TUPLA: contiene las respuestas que se consideran afirmativas.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")

def limpiar_pantalla():
    """Limpia la pantalla de la consola.
    Returns:
        None: solo realiza una acción en la consola.
"""
    # Usa "clear" en Linux/Mac y "cls" en Windows.
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    """Imprime un texto utilizando un color de consola.
    Args:
        texto: Mensaje que se desea mostrar.
        color: Nombre del color definido en COLORES.
    Returns:
        None: muestra el texto en pantalla.
    """
    # Obtiene el código del color o usa blanco si no existe.
    codigo = COLORES.get(color, COLORES["BLANCO"])

    # Imprime el texto con el color y luego restablece el formato.
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    """Muestra un título para una sección del programa.
    Args:
        texto: Título que se desea mostrar.
    Returns:
        None: solo muestra información en pantalla.
    """
    # Limpia la pantalla antes de mostrar el nuevo título.
    limpiar_pantalla()

    # Muestra una línea superior de separación.
    imprimir_color("=" * 60, "AZUL")

    # Centra el título dentro del espacio disponible.
    print(f"  {texto}".center(60))

    # Muestra una línea inferior de separación.
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    """Muestra un mensaje indicando que una operación fue exitosa.
    Args:
        mensaje: Texto que se mostrará al usuario.
    Returns:
        None: muestra el mensaje en pantalla.
    """
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    """Muestra un mensaje indicando que ocurrió un error.
    Args:
        mensaje: Texto que explica el error.
    Returns:
        None: muestra el mensaje en pantalla.
    """
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    """Muestra un mensaje informativo al usuario.
    Args:
        mensaje: Información que se desea mostrar.
    Returns:
        None: muestra el mensaje en pantalla.
    """
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    """Solicita al usuario una confirmación.
    Args:
        pregunta: Pregunta que se mostrará al usuario.
    Returns:
        True si la respuesta es afirmativa; False en caso contrario.
    """
    # Solicita la respuesta y la convierte a minúsculas.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()

    # Comprueba si la respuesta está dentro de RESPUESTAS_SI.
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    """Comprueba si un correo tiene un formato básico válido.
    Args:
        texto: Correo electrónico que se desea validar.
    Returns:
        True si el correo cumple las condiciones básicas; False si no.
    """
    # Elimina espacios al inicio y al final.
    texto = texto.strip()

    # Debe existir exactamente un símbolo @.
    if texto.count("@") != 1:
        return False

    # Separa el correo en usuario y dominio.
    usuario, dominio = texto.split("@")

    # Comprueba que exista usuario, un punto en el dominio
    # y que el dominio no termine en punto.
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")