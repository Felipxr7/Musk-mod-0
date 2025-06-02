import os
import pandas as pd
import logging
from entities.lector import LectorCSV, LectorTXT, LectorJSON
from entities.aeropuerto import Aeropuerto

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def preprocesa_data(df1: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame) -> pd.DataFrame:
    df = pd.concat([df1, df2, df3], ignore_index=True)
    df["fecha_llegada"] = pd.to_datetime(df["fecha_llegada"])
    if "retraso" in df.columns:
        df["retraso"] = df["retraso"].fillna(0)
    return df

class Main:
    def __init__(self):
        self.ejecuta()

    def ejecuta(self):
        logging.info("Iniciando lectura de archivos de vuelos...")

        lector_txt = LectorTXT(os.path.join("data", "vuelos_1.txt"))
        lector_csv = LectorCSV(os.path.join("data", "vuelos_2.csv"))
        lector_json = LectorJSON(os.path.join("data", "vuelos_3.json"))

        df1 = lector_txt.lee_archivo()
        print("df1 (TXT) tipo:", type(df1))
        print(df1 if isinstance(df1, str) else df1.head())
        df1["fecha_llegada"] = pd.to_datetime(df1["fecha_llegada"].str.replace("T", " "), dayfirst=True, errors="coerce")
        df1["fecha_despegue"] = pd.to_datetime(df1["fecha_despegue"].str.replace("T", " "), dayfirst=True, errors="coerce")


        df2 = lector_csv.lee_archivo(datetime_columns=["fecha_llegada"])
        print("df2 (CSV) tipo:", type(df2))
        print(df2.head() if isinstance(df2, pd.DataFrame) else df2)

        df3 = lector_json.lee_archivo()
        print("df3 (JSON) tipo:", type(df3))
        print(df3 if isinstance(df3, str) else df3)
        df3["fecha_llegada"] = pd.to_datetime(df3["fecha_llegada"], dayfirst=True, errors="coerce")
        df3["fecha_despegue"] = pd.to_datetime(df3["fecha_despegue"], dayfirst=True, errors="coerce")


        if not all(isinstance(df, pd.DataFrame) for df in [df1, df2, df3]):
            print("Error en lectura de archivos.")
            logging.error("Error en lectura de archivos.")
            return

        logging.info("Preprocesando datos...")
        df_vuelos = preprocesa_data(df1, df2, df3)

        logging.info("Asignando slots en el aeropuerto...")
        aeropuerto = Aeropuerto(
            vuelos=df_vuelos,
            slots=5,
            t_embarque_nat=30,
            t_embarque_internat=45
        )
        aeropuerto.asigna_slots()

        for _, fila in aeropuerto.df_vuelos.iterrows():
            logging.info(f"Vuelo {fila['id']} llega {fila['fecha_llegada']} y despega {fila['fecha_despegue']} asignado al slot {fila['slot']}")

if __name__ == '__main__':
    Main()
    