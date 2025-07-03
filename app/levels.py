# app/levels.py

TOTAL_LEVELS = 6

# Diccionario con los retos del juego
RETO_POR_NIVEL = {
    1: {
        "enunciado": "¿Cuál es el resultado de 3 + 5 * 2?",
        "entrada": None,
        "salida": "13",
        "pista": "Primero las multiplicaciones… el orden importa."
    },
    2: {
        "enunciado": "Invierte la palabra: 'anagrama'",
        "entrada": "anagrama",
        "salida": "amargana",
        "pista": "Lee desde el final hasta el principio."
    },
    3: {
        "enunciado": "Convierte el número binario 1011 a decimal.",
        "entrada": "1011",
        "salida": "11",
        "pista": "Potencias de 2: 1x8 + 0x4 + 1x2 + 1x1"
    },
    4: {
        "enunciado": "¿Cuántas letras tiene la palabra 'inteligencia'?",
        "entrada": "inteligencia",
        "salida": "12",
        "pista": "Cuenta cuidadosamente, no te comas ninguna letra."
    },
    5: {
        "enunciado": "Evalúa: (4**2 - 6) / 2",
        "entrada": None,
        "salida": "5.0",
        "pista": "Potencias antes que la resta. ¿Paréntesis incluidos?"
    },
    6: {
        "enunciado": "Codifica 'hola' en ASCII (suma los valores de cada letra)",
        "entrada": "hola",
        "salida": "421",
        "pista": "h=104, o=111, l=108, a=98. Súmalos todos."
    }
}

def get_challenge(level: int) -> str:
    """Devuelve el enunciado del reto para el nivel dado."""
    return RETO_POR_NIVEL.get(level, {}).get("enunciado", "Nivel no disponible.")

def get_expected_output(level: int) -> str:
    """Devuelve la respuesta correcta para el nivel dado."""
    return RETO_POR_NIVEL.get(level, {}).get("salida", "")

def get_hint(level: int) -> str:
    """Devuelve una pista críptica para el nivel dado."""
    return RETO_POR_NIVEL.get(level, {}).get("pista", "Sin pista. Usa tu lógica.")
