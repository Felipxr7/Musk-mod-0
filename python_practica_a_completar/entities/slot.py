from datetime import datetime

class Slot:
    def __init__(self, id, fecha_llegada=None, fecha_despegue=None):
        self.id = id
        self.fecha_inicial = fecha_llegada
        self.fecha_final = fecha_despegue

    def asigna_vuelo(self, id, fecha_llegada: datetime, fecha_despegue: datetime):
        if fecha_llegada > fecha_despegue:
            print("Error: la fecha de llegada no puede ser posterior a la de despegue.")
            return
        self.id = id
        self.fecha_inicial = fecha_llegada
        self.fecha_final = fecha_despegue

    def slot_esta_libre_fecha_determinada(self, llegada: datetime, despegue: datetime) -> bool:
        if self.fecha_inicial is None or self.fecha_final is None:
            return True
        return despegue <= self.fecha_inicial or llegada >= self.fecha_final
