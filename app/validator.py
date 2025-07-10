# app/validator.py

import ast
import io
import sys
from typing import Any

def normalize_answer(value: str) -> Any:
    """
    Convierte la cadena en su tipo de dato correspondiente si es posible.
    """
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value.strip().lower()

def is_palindrome(text: str) -> bool:
    clean = ''.join(c.lower() for c in text if c.isalnum())
    return clean == clean[::-1]

def safe_exec(code: str) -> str:
    """
    Ejecuta código en un entorno seguro y captura el resultado de print().
    """
    buffer = io.StringIO()
    try:
        original_stdout = sys.stdout
        sys.stdout = buffer
        exec(code, {})
        return buffer.getvalue().strip()
    except Exception:
        return ""
    finally:
        sys.stdout = original_stdout

def validate_answer(challenge_type: str, challenge: str, user_code: str) -> dict:
    """
    Valida la respuesta del jugador según el tipo de reto.
    Devuelve un diccionario con 'success' y 'output'.
    """
    print(f"Validando reto: {challenge}")
    expected_output = challenge['expected_output']
    challenge_type = challenge['type']

    try:
        # Ambiente seguro para evaluar la respuesta
        local_vars = {}

        if challenge_type in ["number", "string", "list", "palindrome"]:
            exec(user_code, {}, local_vars)

            # Extrae la variable principal según el tipo
            key = list(local_vars.keys())[0] if local_vars else None
            output = local_vars.get(key, None)
            print(f"Salida del código ejecutado: {output} y salida esperada: {expected_output}")

            if challenge_type == "palindrome":
                success = str(output) == str(expected_output)
            elif challenge_type == "list":
                success = str(output) == expected_output
            else:
                success = str(output).strip() == str(expected_output).strip()

            return {
                "success": success,
                "output": output
            }

        else:
            # Por defecto: comparar código ejecutado con salida esperada
            import io
            import sys

            # Capturar la salida estándar
            stdout_backup = sys.stdout
            sys.stdout = io.StringIO()

            exec(user_code, {}, local_vars)

            result = sys.stdout.getvalue().strip()
            sys.stdout = stdout_backup

            success = result == expected_output.expected_output.strip()
            return {
                "success": success,
                "output": result
            }

    except Exception as e:
        return {
            "success": False,
            "output": f"Error de ejecución: {e}"
        }