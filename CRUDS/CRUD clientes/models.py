import json  # Permite trabajar con datos en formato JSON.

# Campos que pertenecen a un cliente y se utilizan en otras partes del sistema.
CAMPOS_CLIENTE = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")

from shared.herramientas import limpiar_pantalla  # Importa una función de utilidad.


# MODELO: representa los datos y acciones relacionadas con un cliente.
class Cliente:
    """Representa a un cliente."""

    def __init__(self, id_cliente, nombre, apellido, email, telefono, ciudad, direccion):
        """Crea un nuevo objeto Cliente."""
        self.id = id_cliente  # Identificador único del cliente.
        self.nombre = nombre  # Nombre del cliente.
        self.apellido = apellido  # Apellido del cliente.
        self.email = email  # Correo electrónico.
        self.telefono = telefono  # Número de teléfono.
        self.ciudad = ciudad  # Ciudad donde vive.
        self.direccion = direccion  # Dirección del cliente.

    def obtener_nombre_completo(self):
        """ Obtiene el nombre completo del cliente.
        Returns:
            El nombre y apellido unidos en un solo texto.
        """
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        """Convierte el cliente en un diccionario.
        Returns:
            Un diccionario con todos los datos del cliente."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un Cliente a partir de un diccionario.
        Args:
            datos: Diccionario que contiene los datos del cliente.
        Returns:
            Un nuevo objeto Cliente."""
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["telefono"],
            datos.get("ciudad", ""),      # Usa "" si el campo no existe.
            datos.get("direccion", ""),
        )

    def a_json(self):
        """Convierte los datos del cliente a formato JSON.
        Returns:
            Los datos del cliente como texto JSON."""
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    def __str__(self):
        """Define cómo se muestra el cliente al usar print().
        Returns:
            Una cadena con el ID, nombre completo y email.
        """
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"


