import os
import json
import unittest


class Hotel:
    def __init__(self, nombre, ubicacion, habitaciones_disponibles):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.habitaciones_disponibles = habitaciones_disponibles
        self.reservaciones = []

    def crear_hotel(nombre, ubicacion, habitaciones_disponibles):
        hotel = Hotel(nombre, ubicacion, habitaciones_disponibles)
        hoteles = cargar_datos("hoteles.json")
        hoteles.append(hotel.__dict__)
        guardar_datos("hoteles.json", hoteles)
        return hotel

    def eliminar_hotel(nombre):
        hoteles = cargar_datos("hoteles.json")
        hoteles = [hotel for hotel in hoteles if hotel["nombre"] != nombre]
        guardar_datos("hoteles.json", hoteles)

    def mostrar_informacion_hotel(nombre):
        hoteles = cargar_datos("hoteles.json")
        for hotel in hoteles:
            if hotel["nombre"] == nombre:
                print(f"Nombre: {hotel['nombre']}")
                print(f"Ubicación: {hotel['ubicacion']}")
                print(f"Hab Disponibles: {hotel['habitaciones_disponibles']}")
                print(f"Reservaciones: {hotel['reservaciones']}")

    def modificar_informacion_hotel(
        nombre, nueva_ubicacion=None, nuevas_habitaciones_disponibles=None
    ):
        hoteles = cargar_datos("hoteles.json")
        for hotel in hoteles:
            if hotel["nombre"] == nombre:
                if nueva_ubicacion:
                    hotel["ubicacion"] = nueva_ubicacion
                if nuevas_habitaciones_disponibles:
                    hotel["habitaciones_disponibles"] = nuevas_habitaciones_disponibles
                guardar_datos("hoteles.json", hoteles)

    def reservar_habitacion(hotel_nombre, cliente_nombre):
        hoteles = cargar_datos("hoteles.json")
        for hotel in hoteles:
            if (
                hotel["nombre"] == hotel_nombre
                and hotel["habitaciones_disponibles"] > 0
            ):
                hotel["reservaciones"].append(cliente_nombre)
                hotel["habitaciones_disponibles"] -= 1
                guardar_datos("hoteles.json", hoteles)
                return True
        return False

    def cancelar_reservacion(hotel_nombre, cliente_nombre):
        hoteles = cargar_datos("hoteles.json")
        for hotel in hoteles:
            if (
                hotel["nombre"] == hotel_nombre
                and cliente_nombre in hotel["reservaciones"]
            ):
                hotel["reservaciones"].remove(cliente_nombre)
                hotel["habitaciones_disponibles"] += 1
                guardar_datos("hoteles.json", hoteles)
                return True
        return False


class Cliente:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def crear_cliente(nombre, email):
        cliente = Cliente(nombre, email)
        clientes = cargar_datos("clientes.json")
        clientes.append(cliente.__dict__)
        guardar_datos("clientes.json", clientes)
        return cliente

    def eliminar_cliente(nombre):
        clientes = cargar_datos("clientes.json")
        clientes = [cliente for cliente in clientes if cliente["nombre"] != nombre]
        guardar_datos("clientes.json", clientes)

    def mostrar_informacion_cliente(nombre):
        clientes = cargar_datos("clientes.json")
        for cliente in clientes:
            if cliente["nombre"] == nombre:
                print(f"Nombre: {cliente['nombre']}")
                print(f"Email: {cliente['email']}")

    def modificar_informacion_cliente(nombre, nuevo_email=None):
        clientes = cargar_datos("clientes.json")
        for cliente in clientes:
            if cliente["nombre"] == nombre and nuevo_email:
                cliente["email"] = nuevo_email
                guardar_datos("clientes.json", clientes)


class Reservacion:
    def __init__(self, cliente, hotel):
        self.cliente = cliente
        self.hotel = hotel

    def crear_reservacion(cliente_nombre, hotel_nombre):
        if Hotel.reservar_habitacion(hotel_nombre, cliente_nombre):
            reservacion = Reservacion(cliente_nombre, hotel_nombre)
            reservaciones = cargar_datos("reservaciones.json")
            reservaciones.append(reservacion.__dict__)
            guardar_datos("reservaciones.json", reservaciones)
            return reservacion
        return None

    def cancelar_reservacion(cliente_nombre, hotel_nombre):
        if Hotel.cancelar_reservacion(hotel_nombre, cliente_nombre):
            reservaciones = cargar_datos("reservaciones.json")
            reservaciones = [
                res
                for res in reservaciones
                if not (
                    res["cliente"] == cliente_nombre and res["hotel"] == hotel_nombre
                )
            ]
            guardar_datos("reservaciones.json", reservaciones)


def guardar_datos(nombre_archivo, datos):
    try:
        with open(nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except Exception as e:
        print(f"Error al guardar datos: {e}")


def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r") as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    return []


class TestSistemaHotel(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel.crear_hotel("Hotel Ejemplo", "Ciudad Ejemplo", 10)
        self.cliente = Cliente.crear_cliente("Cliente Ejemplo", "email@ejemplo.com")
        self.reservacion = Reservacion.crear_reservacion(
            "Cliente Ejemplo", "Hotel Ejemplo"
        )

    def test_crear_hotel(self):
        self.assertIsNotNone(self.hotel)

    def test_crear_cliente(self):
        self.assertIsNotNone(self.cliente)

    def test_crear_reservacion(self):
        self.assertIsNotNone(self.reservacion)

    def test_reservar_habitacion(self):
        self.assertTrue(Hotel.reservar_habitacion("Hotel Ejemplo", "Cliente Ejemplo"))

    def test_cancelar_reservacion(self):
        self.assertTrue(Hotel.cancelar_reservacion("Hotel Ejemplo", "Cliente Ejemplo"))


if __name__ == "__main__":
    unittest.main()
    # Ejemplo de uso del sistema
    hotel = Hotel.crear_hotel("Hotel Palacio", "Ciudad de Mexico", 20)
    Hotel.mostrar_informacion_hotel("Hotel Palacio")

    cliente = Cliente.crear_cliente("Sofia Pedroza", "sofia.pedroza@correo.com")
    Cliente.mostrar_informacion_cliente("Sofia Martinez")

    reserva_exitosa = Hotel.reservar_habitacion("Hotel Palacio", "Sofia Pedroza")
    print("Reserva exitosa" if reserva_exitosa else "No se pudo realizar la reserva")

    cancelacion_exitosa = Hotel.cancelar_reservacion("Hotel Palacio", "Sofía Martínez")
    print(
        "Cancelación exitosa"
        if cancelacion_exitosa
        else "No se pudo cancelar la reservación"
    )
