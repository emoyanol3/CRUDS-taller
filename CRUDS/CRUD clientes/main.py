from models import CAMPOS_CLIENTE

# Importa las funciones que muestran mensajes y piden confirmaciones.
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar)

# Importa las funciones que realizan las operaciones del CRUD.
from views import (
    crear_cliente, obtener_todos, obtener_por_id, buscar_clientes,
    actualizar_cliente, eliminar_cliente, estadisticas)

# Pausa el programa hasta que el usuario presione Enter.
def pausa():
    input("\nPresione Enter para continuar...")

# Muestra una lista de clientes en forma de tabla.
def mostrar_tabla(clientes):
    # Define los encabezados de las columnas.
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}{'TELÉFONO':<12}")
    print("-" * 85)

    # Recorre cada cliente y muestra sus datos.
    for cliente in clientes:
        print(f"{cliente.id:<5}{cliente.obtener_nombre_completo():<25}"
              f"{cliente.email:<28}{cliente.ciudad:<15}{cliente.telefono:<12}")

    print("-" * 85)

    # Muestra la cantidad total de clientes.
    imprimir_info(f"Total: {len(clientes)} cliente(s)")

# ---------- C · CREAR ----------

def opcion_crear():
    imprimir_titulo("CREAR NUEVO CLIENTE")

    # Crea un diccionario con los datos ingresados por el usuario.
    datos = {}

    # Recorre los campos definidos en CAMPOS_CLIENTE.
    for campo in CAMPOS_CLIENTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    # Envía los datos al CRUD y recibe el resultado de la operación.
    exito, mensaje = crear_cliente(datos)

    # Muestra un mensaje dependiendo de si la operación tuvo éxito.
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()
# ---------- R · LEER TODOS ----------

def opcion_ver_todos():
    imprimir_titulo("LISTA DE CLIENTES")

    # Obtiene todos los clientes registrados.
    clientes = obtener_todos()

    if not clientes:
        # Informa si todavía no existen clientes.
        imprimir_info("Todavía no hay clientes. Use la opción 1 para crear el primero.")
    else:
        # Si existen clientes, los muestra en una tabla.
        mostrar_tabla(clientes)

    pausa()
# ---------- S · BUSCAR ----------

def opcion_buscar():
    imprimir_titulo("BUSCAR CLIENTE")

    # Solicita el texto que se desea buscar.
    termino = input("Nombre, email, teléfono o ciudad: ")

    # Realiza la búsqueda de clientes.
    encontrados = buscar_clientes(termino)

    if not encontrados:
        # Informa si no hubo coincidencias.
        imprimir_info(f"Ningún cliente coincide con '{termino}'.")
    else:
        # Muestra los clientes encontrados.
        mostrar_tabla(encontrados)

    pausa()
# ---------- R · LEER UNO ----------

def opcion_ver_por_id():
    imprimir_titulo("VER CLIENTE POR ID")

    try:
        # Convierte el ID ingresado a un número entero.
        id_cliente = int(input("Id del cliente: "))

    except ValueError:
        # Evita que el programa se detenga si se escribe texto.
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Busca el cliente utilizando su ID.
    cliente = obtener_por_id(id_cliente)

    if not cliente:
        # Informa si el cliente no existe.
        imprimir_error(f"No existe un cliente con id {id_cliente}")

    else:
        # Convierte el cliente en diccionario y muestra sus datos.
        for clave, valor in cliente.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")

    pausa()
# ---------- U · ACTUALIZAR ----------

def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR CLIENTE")

    try:
        # Solicita y convierte el ID a entero.
        id_cliente = int(input("Id del cliente: "))

    except ValueError:
        # Controla el error si el usuario escribe algo que no sea un número.
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Busca el cliente que se desea modificar.
    cliente = obtener_por_id(id_cliente)

    if not cliente:
        # Informa si no existe el cliente.
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        return pausa()

    imprimir_info(f"Editando a {cliente.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Diccionario que almacenará únicamente los campos modificados.
    cambios = {}

    # Recorre todos los campos del cliente.
    for campo in CAMPOS_CLIENTE:

        # Obtiene el valor actual del campo.
        actual = getattr(cliente, campo)

        # Solicita el nuevo valor.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        # Solo agrega el campo si el usuario escribió un nuevo valor.
        if nuevo:
            cambios[campo] = nuevo

    # Envía los cambios al CRUD.
    exito, mensaje = actualizar_cliente(id_cliente, cambios)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()
# ---------- D · ELIMINAR ----------

def opcion_eliminar():
    imprimir_titulo("ELIMINAR CLIENTE")

    try:
        # Solicita el ID del cliente que se quiere eliminar.
        id_cliente = int(input("Id del cliente: "))

    except ValueError:
        # Controla un ID que no sea numérico.
        imprimir_error("El id debe ser un número entero")
        return pausa()

    # Busca el cliente antes de eliminarlo.
    cliente = obtener_por_id(id_cliente)

    if not cliente:
        # Informa si el cliente no existe.
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        return pausa()

    # Muestra qué cliente será eliminado.
    imprimir_info(f"Se eliminará: {cliente}")

    # Solicita confirmación antes de eliminar.
    if confirmar("¿Confirma la eliminación?"):

        # Ejecuta la eliminación.
        exito, mensaje = eliminar_cliente(id_cliente)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    else:
        # Si el usuario cancela, no se elimina nada.
        imprimir_info("Operación cancelada")

    pausa()
# ---------- EXTRA · ESTADÍSTICAS ----------

def opcion_estadisticas():
    imprimir_titulo("ESTADÍSTICAS")

    # Obtiene las estadísticas generadas por el CRUD.
    datos = estadisticas()

    # Muestra la información obtenida.
    print(f"  Clientes registrados : {datos['total']}")
    print(f"  Ciudades distintas   : {len(datos['ciudades'])} -> {', '.join(datos['ciudades'])}")
    print(f"  Dominios de email    : {', '.join(datos['dominios'])}")
    print(f"  Sin teléfono         : {len(datos['sin_telefono'])}")

    pausa()

# Finaliza el programa.
def salir():
    imprimir_info("¡Hasta luego!")
    return "salir"

# Diccionario que relaciona cada tecla con una opción y su función.
OPCIONES = {
    "1": ("Crear cliente", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Estadísticas", opcion_estadisticas),
    "0": ("Salir", salir),
}

# Muestra las opciones disponibles del menú.
def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE CLIENTES")

    # Recorre el diccionario y muestra cada opción.
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")

    print()

# Función principal que controla el funcionamiento del programa.
def main():

    # Mantiene el menú funcionando hasta que el usuario decida salir.
    while True:
        mostrar_menu()

        # Solicita al usuario que seleccione una opción.
        tecla = input("Seleccione una opción: ").strip()

        # Comprueba si la opción existe en el diccionario.
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        # Obtiene la función asociada a la opción seleccionada.
        _texto, funcion = OPCIONES[tecla]

        # Ejecuta la función correspondiente.
        if funcion() == "salir":
            break

# Comprueba que este archivo sea el programa principal.
if __name__ == "__main__":

    try:
        # Inicia el sistema.
        main()

    except KeyboardInterrupt:
        # Permite cerrar el programa con Ctrl + C sin mostrar un error.
        print("\nPrograma interrumpido por el usuario.")