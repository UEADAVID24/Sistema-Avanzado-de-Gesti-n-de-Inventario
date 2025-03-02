import json

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        """Convierte el producto en un diccionario para almacenamiento."""
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos = self.cargar_inventario()

    def agregar_producto(self, producto):
        """Añadir un nuevo producto al inventario."""
        if producto.id_producto in self.productos:
            print("Error: ID de producto ya existente.")
        else:
            self.productos[producto.id_producto] = producto
            self.guardar_inventario()
            print("Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        """Eliminar un producto por su ID."""
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()
            print("Producto eliminado correctamente.")
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualizar cantidad o precio de un producto."""
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].cantidad = cantidad
            if precio is not None:
                self.productos[id_producto].precio = precio
            self.guardar_inventario()
            print("Producto actualizado correctamente.")
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        """Buscar productos por nombre."""
        encontrados = [p.to_dict() for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            for producto in encontrados:
                print(producto)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_productos(self):
        """Mostrar todos los productos del inventario."""
        if self.productos:
            for producto in self.productos.values():
                print(producto.to_dict())
        else:
            print("El inventario está vacío.")

    def guardar_inventario(self):
        """Guardar inventario en un archivo JSON."""
        with open(self.archivo, "w") as file:
            json.dump({k: v.to_dict() for k, v in self.productos.items()}, file, indent=4)

    def cargar_inventario(self):
        """Cargar el inventario desde un archivo JSON."""
        try:
            with open(self.archivo, "r") as file:
                datos = json.load(file)
                return {k: Producto(**v) for k, v in datos.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

# Interfaz de usuario
if __name__ == "__main__":
    inventario = Inventario()
    while True:
        print("\n1. Agregar Producto")
        print("2. Eliminar Producto")
        print("3. Actualizar Producto")
        print("4. Buscar Producto")
        print("5. Mostrar Inventario")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("ID del producto: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            inventario.agregar_producto(Producto(id_producto, nombre, cantidad, precio))
        elif opcion == "2":
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)
        elif opcion == "3":
            id_producto = input("ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (dejar vacío si no cambia): ")
            precio = input("Nuevo precio (dejar vacío si no cambia): ")
            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None
            inventario.actualizar_producto(id_producto, cantidad, precio)
        elif opcion == "4":
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)
        elif opcion == "5":
            inventario.mostrar_productos()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
