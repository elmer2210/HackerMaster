# ============================================
# Archivo: storage.py
# Propósito: Leer y guardar los datos desde archivos JSON.
# Este archivo contiene:
#   - Función `load_players()` → lee jugadores.json y retorna lista
#   - Función `save_players(jugadores)` → guarda lista en jugadores.json
#   - Opcional:
#       - `export_to_csv()` → para exportar métricas a resultados.csv
# Este archivo se encarga de la persistencia de datos.
# ============================================

from app.players import get_all_players, serialize_players, load_players_from_data
import json
import os
import csv

# Ruta del archivo JSON donde se guardan los jugadores
DATA_FILE = os.path.join("data", "players.json")
CSV_FILE = os.path.join("data", "results.csv")

#Guardamos los jugadores en el archivo JSON
def save_players_to_json():
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(serialize_players(), file, indent=4, ensure_ascii=False)
    print(f"Jugadores guardados en {DATA_FILE}")

# Cargamos los jugadores desde el archivo JSON
def load_players_from_json():
    if not os.path.exists(DATA_FILE):
        print(f"Archivo {DATA_FILE} no encontrado. Cargando jugadores vacíos.")
        return
    
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            load_players_from_data(data)
            print(f"Jugadores cargados desde {DATA_FILE}")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON en {DATA_FILE}. Cargando jugadores vacíos.")
            
# Exporta los resultados a un archivo CSV (opcional)
def export_to_csv():

    players = get_all_players()

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        # Definimos los nombres de las columnas del CSV
        # Asegúrate de que los nombres coincidan con los atributos de Player
        fieldnames = ['name', 'current_level', 'score_per_level', 'attempts', 
                      'correct_attempts', 'incorrect_attempts']
        # Creamos el escritor de CSV con los nombres de las columnas
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in players:
            writer.writerow({
                'name': player.name,
                'current_level': player.current_level,
                'score_per_level': player.score_per_level,
                'attempts': player.attempts,
                'correct_attempts': player.correct_attempts,
                'incorrect_attempts': player.incorrect_attempts
            })
    print(f"Resultados exportados a {CSV_FILE}")