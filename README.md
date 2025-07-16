# HackerMaster: Videojuego de Retos de Programación Interactivos

## Descripción

**HackerMaster** es un juego web interactivo que desafía a los jugadores a resolver retos de programación y lógica en Python. Inspirado en el ambiente de un "terminal hacker", el jugador avanza nivel por nivel superando desafíos de dificultad creciente. El objetivo es mejorar habilidades de programación, lógica y pensamiento crítico de forma divertida y gamificada.

El juego está pensado para ambientes educativos, ferias de tecnología y formación de futuros ingenieros.

---

## Características

- **Retos dinámicos:** Preguntas de programación (listas, strings, binario, lógica, etc.), que requieren resolver un mini-problema escribiendo código Python.
- **Sistema de niveles:** El juego tiene tres niveles de dificultad (fácil, medio, difícil) y cada uno contiene una serie de retos.
- **Validación automática:** El sistema ejecuta y valida el código o la respuesta del usuario contra un output esperado.
- **Puntuación y métricas:** Lleva el control de intentos, aciertos, errores, avance por nivel, etc.
- **Interfaz tipo terminal hacker:** Visual atractivo inspirado en entornos de hacking y matrix.
- **Transiciones animadas:** Animaciones para pase de nivel, loading y Game Over.
- **Pantallas de victoria y game over:** Mensajes interactivos y métricas de desempeño al terminar el juego.
- **Backend escalable:** El backend permite definir nuevos retos y tipos de desafíos fácilmente desde archivos JSON.
- **Métricas en tiempo real:** Pantalla exclusiva para ver estadísticas y desempeño de todos los jugadores.

---

## Tecnologías y Librerías Utilizadas

- **Backend:** Python 3.9+, Flask, json, os, ast.
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API), FontAwesome.
- **Estilos especiales:** Fondo tipo Matrix animado, overlays CSS para transiciones.
- **Ejecución segura:** El backend evalúa el código del usuario en un entorno controlado.
- **Persistencia:** Los datos de jugadores y métricas se guardan en archivos JSON.

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/HackerMaster.git
cd HackerMaster
pip install -r requirements.txt
python run.py
