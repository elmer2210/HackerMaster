from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# ============================================
# Archivo: run.py
# Propósito: Punto de entrada para ejecutar el servidor.
# Este archivo:
#   - Importa la función `create_app()` desde __init__.py
#   - Ejecuta la aplicación Flask
# Comando:
#   python run.py
# ============================================
