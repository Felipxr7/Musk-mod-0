import pandas as pd
import json 
import os

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension):
        _, ext = os.path.splitext(self.path)
        if ext.lower() != f".{extension.lower()}":
            raise ValueError(f"Error: Se esperaba un archivo con extensión .{extension}, pero se recibió {ext}")

    def lee_archivo(self):
        raise NotImplementedError

    @staticmethod
    def convierte_dict_a_csv(data: dict, output_file: str):
        df = pd.DataFrame.from_dict(data)
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"Archivo csv '{output_file}' generado exitosamente")

class LectorCSV(Lector):
    def __init__(self, path):
        super().__init__(path)
        self._comprueba_extension("csv")
    def lee_archivo(self, datetime_columns=None):
        if datetime_columns is None:
            datetime_columns = []
        try:
            df = pd.read_csv(self.path, parse_dates=datetime_columns, encoding="utf-8")
            return df
        except FileNotFoundError:
            return "Error: el archivo no existe"

class LectorJSON(Lector):
    def __init__(self, path):
        super().__init__(path)
        self._comprueba_extension("json")
    def lee_archivo(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
            df = pd.DataFrame(data)
            return df
        except FileNotFoundError:
            return "Error: el archivo no existe"

class LectorTXT(Lector):
    def __init__(self, path):
        super().__init__(path)
        self._comprueba_extension("txt")
    def lee_archivo(self):
        try:
            df = pd.read_csv(self.path, delimiter=",", skipinitialspace=True)
            return df
        except FileNotFoundError:
            return "Error: el archivo no existe"
        except pd.errors.ParserError:
            return "Error: formato del archivo TXT no es adecuado"