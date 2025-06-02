import pandas as pd
from datetime import datetime
from entities.slot import Slot

class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = [None] * self.n_slots
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(self.n_slots):
            self.slots[i] = Slot(id=i, fecha_llegada=None, fecha_despegue=None)

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row: pd.Series) -> pd.Series:
        tipo = row["tipo_vuelo"]
        tiempo_embarque = self.tiempo_embarque_nat if tipo == "NAT" else self.tiempo_embarque_internat
        retraso_str = str(row["retraso"]).strip()
        if retraso_str in ["-", "", "NaT", "nan"]:
            retraso = 0
        else:
            try:
                horas, minutos = map(int, retraso_str.split(":"))
                retraso = horas * 60 + minutos
            except ValueError:
                retraso = 0
        row["fecha_despegue"] = row["fecha_llegada"] + pd.to_timedelta(tiempo_embarque + retraso, unit="m")
        return row

    def encuentra_slot(self, fecha_llegada: datetime, fecha_despegue: datetime) -> int:
        for idx, slot in enumerate(self.slots):
            if slot.slot_esta_libre_fecha_determinada(fecha_llegada, fecha_despegue):
                return idx
        return -1

    def asigna_slot(self, vuelo) -> pd.Series:
        vuelo = self.calcula_fecha_despegue(vuelo)
        intentos = 0
        max_intentos = 10
        while intentos < max_intentos:
            slot_libre = self.encuentra_slot(vuelo["fecha_llegada"], vuelo["fecha_despegue"])
            if slot_libre != -1:
                self.slots[slot_libre].asigna_vuelo(
                    id=vuelo["id"],
                    fecha_llegada=vuelo["fecha_llegada"],
                    fecha_despegue=vuelo["fecha_despegue"]
                )
                vuelo["slot"] = slot_libre
                print(f"Vuelo asignado - Slot: {slot_libre}, Fecha despegue: {vuelo['fecha_despegue']}")
                return vuelo
            else:
                vuelo["fecha_llegada"] += pd.to_timedelta(10, unit="m")
                vuelo = self.calcula_fecha_despegue(vuelo)
                intentos += 1
        print(f"No se pudo asignar slot para vuelo {vuelo['id']} después de {max_intentos} intentos.")
        vuelo["slot"] = None
        return vuelo

    def asigna_slots(self):
        self.df_vuelos.sort_values(by="fecha_llegada", inplace=True)
        self.df_vuelos = self.df_vuelos.apply(self.asigna_slot, axis=1)
        self.df_vuelos.sort_values(by=["slot", "fecha_llegada"], inplace=True)
        self.df_vuelos.reset_index(drop=True, inplace=True)