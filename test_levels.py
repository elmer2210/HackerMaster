from app import players, storage

def main():
    # Cargar jugadores si ya existen
    storage.load_players_from_json()

    # Crear un nuevo jugador solo si no existe
    if not players.get_player("Neo"):
        p = players.create_player("Neo")
        players.update_player(p, True, 10)
        players.update_player(p, False, 5)

    # Guardar los jugadores
    storage.save_players_to_json()

    # Exportar CSV
    storage.export_to_csv()

if __name__ == "__main__":
    main()
