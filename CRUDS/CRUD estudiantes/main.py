from models import CAMPOS_ESTUDIANTES

from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_materia,
    agregar_nota,
    actualizar_nota
)


def pausa():
    """Pausa el programa hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    """
    Muestra una lista de estudiantes en forma de tabla.

    Args:
        estudiantes: Lista de objetos Estudiante.

    Returns:
        None. Solo muestra la información en pantalla.
    """
    print(
        f"{'ID':<5}"
        f"{'NOMBRE':<25}"
        f"{'EMAIL':<30}"
        f"{'CARNET':<15}"
        f"{'PROMEDIO':<10}"
        f"{'MATERIAS':<10}"
    )

    print("-" * 95)

    for estudiante in estudiantes:
        materias = len(estudiante.materias)

        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<30}"
            f"{estudiante.carnet:<15}"
            f"{estudiante.obtener_promedio():<10}"
            f"{materias:<10}"
        )

    print("-" * 95)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ===================== CREAR =====================

def opcion_crear():
    """Solicita los datos y crea un nuevo estudiante."""
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")

    datos = {}

    for campo in CAMPOS_ESTUDIANTES:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ===================== VER TODOS =====================

def opcion_ver_todos():
    """Muestra todos los estudiantes registrados."""
    imprimir_titulo("LISTA DE ESTUDIANTES")

    estudiantes = obtener_todos()

    if not estudiantes:
        imprimir_info(
            "Todavía no hay estudiantes. "
            "Use la opción 1 para crear el primero."
        )
    else:
        mostrar_tabla(estudiantes)

    pausa()


# ===================== BUSCAR =====================

def opcion_buscar():
    """Busca estudiantes utilizando diferentes datos."""
    imprimir_titulo("BUSCAR ESTUDIANTE")

    termino = input(
        "Nombre, apellido, email, carnet o materia: "
    )

    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(
            f"Ningún estudiante coincide con '{termino}'."
        )
    else:
        mostrar_tabla(encontrados)

    pausa()


# ===================== VER POR ID =====================

def opcion_ver_por_id():
    """Muestra todos los datos de un estudiante mediante su ID."""
    imprimir_titulo("VER ESTUDIANTE POR ID")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    print(f"\nID          : {estudiante.id}")
    print(f"Nombre      : {estudiante.nombre}")
    print(f"Apellido    : {estudiante.apellido}")
    print(f"Email       : {estudiante.email}")
    print(f"Carnet      : {estudiante.carnet}")

    # Muestra las materias separadas por coma.
    materias = ", ".join(sorted(estudiante.materias))
    print(f"Materias    : {materias or 'Ninguna'}")

    # Muestra las notas agrupadas por materia.
    print("Notas       :")

    if estudiante.notas:
        for materia, notas in estudiante.notas.items():
            print(f"  - {materia}: {notas}")
    else:
        print("  Ninguna")

    print(f"Promedio    : {estudiante.obtener_promedio()}")

    pausa()


# ===================== ACTUALIZAR =====================

def opcion_actualizar():
    """Permite modificar los datos básicos de un estudiante."""
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    imprimir_info(
        f"Editando a {estudiante.obtener_nombre_completo()}"
    )

    print("Deje en blanco el campo que no quiera cambiar.\n")

    cambios = {}

    for campo in CAMPOS_ESTUDIANTES:
        actual = getattr(estudiante, campo)
        nuevo = input(
            f"{campo.capitalize()} [{actual}]: "
        ).strip()

        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(
        id_estudiante,
        cambios
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ===================== ELIMINAR =====================

def opcion_eliminar():
    """Elimina un estudiante después de confirmar la operación."""
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    imprimir_info(
        f"Se eliminará: {estudiante}"
    )

    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")

    pausa()


# ===================== MATERIAS =====================

def opcion_agregar_materia():
    """Inscribe un estudiante en una materia."""
    imprimir_titulo("INSCRIBIR MATERIA")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Nombre de la materia: ")

    exito, mensaje = agregar_materia(
        id_estudiante,
        materia
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ===================== NOTAS =====================

def opcion_agregar_nota():
    """Registra una nota para un estudiante."""
    imprimir_titulo("REGISTRAR NOTA")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Nombre de la materia: ")
    nota = input("Nota (0 - 10): ")

    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()

def opcion_actualizar_nota():
    """Permite modificar una nota existente."""
    imprimir_titulo("ACTUALIZAR NOTA")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        return pausa()

    if not estudiante.notas:
        imprimir_info("El estudiante todavía no tiene notas registradas.")
        return pausa()

    # Muestra las materias que tienen notas.
    print("\nMaterias con notas:")

    for materia, notas in estudiante.notas.items():
        print(f"  - {materia}: {notas}")

    materia = input("\nMateria: ")

    try:
        numero_nota = int(
            input("Número de nota que desea actualizar: ")
        )
    except ValueError:
        imprimir_error("El número de nota debe ser un entero")
        return pausa()

    nueva_nota = input("Nueva nota (0 - 10): ")

    exito, mensaje = actualizar_nota(
        id_estudiante,
        materia,
        numero_nota,
        nueva_nota
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ===================== SALIR =====================

def salir():
    """Finaliza el programa."""
    imprimir_info("¡Hasta luego!")
    return "salir"


# ===================== MENÚ =====================

OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Inscribir materia", opcion_agregar_materia),
    "8": ("Registrar nota", opcion_agregar_nota),
    "9": ("Actualizar nota", opcion_actualizar_nota),
    "0": ("Salir", salir),
}


def mostrar_menu():
    """Muestra las opciones disponibles del sistema."""
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")

    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")

    print()


def main():
    """Ejecuta el menú principal del sistema."""
    while True:
        mostrar_menu()

        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]

        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")

