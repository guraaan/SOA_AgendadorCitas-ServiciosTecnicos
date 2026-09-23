class Servicio:
    def __init__(self, nombre, descripcion, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

    def a_texto(self):
        return f"{self.nombre}|{self.descripcion}|{self.precio}"

    @staticmethod
    def desde_texto(linea):
        partes = linea.strip().split("|")
        return Servicio(partes[0], partes[1], float(partes[2]))


def guardar_servicio(servicio):
    with open("servicios.txt", "a")as archivo:
        archivo.write(servicio.a_texto() + "\n")


def listar_servicios():
    servicios = []
    try:
        with open("servicios.txt", "r")as archivo:
            for linea in archivo:
                servicios.append(Servicio.desde_texto(linea))
    except FileNotFoundError:
        pass
    return servicios


def actualizar_servicio(indice, servicio):
    servicios = listar_servicios()
    servicios[indice] = servicio
    with open("servicios.txt", "w")as archivo:
        for s in servicios:
            archivo.write(s.a_texto() + "\n")


def eliminar_servicio(indice):
    servicios = listar_servicios()
    del servicios[indice]
    with open("servicios.txt", "w")as archivo:
        for s in servicios:
            archivo.write(s.a_texto() + "\n")
