# app/validator.py

import io
import sys
from typing import Any
from .levels import get_expected_output
from ast import literal_eval

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

def validate_answer(user_code: str, expected_output ,challenge_type: str,) -> dict:
    """
    Valida la respuesta del jugador según el tipo de reto.
    Devuelve un diccionario con 'success' y 'output'.
    """
    try:
        local_vars = {}

        if challenge_type in ["number", "string", "list", "palindrome"]:
            exec(user_code, {}, local_vars)
            key = list(local_vars.keys())[0] if local_vars else None
            output = local_vars.get(key, None)
            
            print(f"Comparando output: '{output}' con esperado: '{expected_output}'")
            #comparación según el tipo de reto
            if challenge_type == "palindrome":
                #Para palidromos, se espera true o false
                success = str(output).lower() == str(expected_output).lower()
            elif challenge_type == "list":
                #Compara lista como objetos, no como cadenas
                try:
                    output_eval = output if isinstance(output, list) else literal_eval(str(output))
                    expected_eval = expected_output if isinstance(expected_output, list) else literal_eval(str(expected_output))
                    success = output_eval == expected_eval
                except Exception:
                    success = False
            else:
                #number o string , convierte a cadena y compara
                success = str(output).strip() == str(expected_output).strip()
            return {
                "success": success,
                "output": output
            }
        else:
            # Para retos tipo "code_output" (comparar output de print)
            stdout_backup = sys.stdout
            sys.stdout = io.StringIO()
            exec(user_code, {}, local_vars)
            result = sys.stdout.getvalue().strip()
            sys.stdout = stdout_backup

            success = result == str(expected_output).strip()

            return {
                "success": success,
                "output": result
            }

    except Exception as e:
        return {
            "success": False,
            "output": f"Error de ejecución: {e}"
        }   
   
 