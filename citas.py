import requests


class Cita:
    def __init__(self, servicio, cliente, fecha):
        self.servicio = servicio
        self.cliente = cliente
        self.fecha = fecha

    def a_texto(self):
        return f"{self.servicio}|{self.cliente}|{self.fecha}"

    @staticmethod
    def desde_texto(linea):
        partes = linea.strip().split("|")
        return Cita(partes[0], partes[1], partes[2])


def es_feriado(fecha):
    """Consulta la API de Nager.Date y devuelve el nombre del feriado o False."""
    anio = fecha[:4]
    try:
        respuesta = requests.get(
            f"https://date.nager.at/api/v3/PublicHolidays/{anio}/MX", timeout=5
        )
        feriados = respuesta.json()
        for f in feriados:

            if f["date"] == fecha:
                return f["localName"]
    except Exception:
        return None
    return False


def guardar_cita(cita):
    with open("citas.txt", "a")as archivo:
        archivo.write(cita.a_texto() + "\n")


def listar_citas():
    citas = []
    try:
        with open("citas.txt", "r")as archivo:
            for linea in archivo:
                citas.append(Cita.desde_texto(linea))
    except FileNotFoundError:
        pass
    return citas


def eliminar_cita(indice):
    citas = listar_citas()
    del citas[indice]
    with open("citas.txt", "w")as archivo:
        for c in citas:
            archivo.write(c.a_texto() + "\n")
