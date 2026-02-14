# Mario-Bros-TOAD
# 🍄 Super Mario Arcade Project

¡Bienvenido al proyecto de recreación de Super Mario Bros version SNES! Este es un desarrollo colaborativo para la universidad, integrado en un sistema de Arcade SDK.

## 🚀 Estado Actual del Proyecto
El juego cuenta actualmente con un menú principal funcional y una transición fluida hacia el primer nivel de plataformas.

### 🎮 Características del Menú
* **Diseño Retro:** Fondo y títulos inspirados en la estética clásica de SNES.
* **Botón Dinámico:** Sistema de parpadeo (blinking) para el botón "Press to Play" que se detiene al pasar el mouse (efecto Hover).
* **Sistema de Audio:** * Música de fondo (Intro SNES) con bucle infinito.
    * Efecto de sonido "p-ping" al interactuar con el botón.
    * Transición de audio suave mediante *fade-out* al iniciar el juego.
* **Área de Interacción Optimizada:** Rectángulo de colisión ajustado manualmente para una respuesta precisa al clic del mouse.

## 🛠️ Tecnologías Utilizadas
* **Python 3.x**
* **Pygame:** Para el motor de juego y manejo de assets.
* **Arcade Machine SDK:** Para la integración en el sistema de la facultad.
* **Pathlib:** Para la gestión de rutas de archivos multiplataforma.

## 📂 Estructura de Archivos (Menú)
```text
project/
│
├── assets/
│   ├── menu/        # Imágenes (Fondo, Título, Botones)
│   ├── music/       # Música de fondo (.mp3)
│   └── sounds/      # Efectos de sonido (.mp3 / .wav)
│
├── src/
│   └── states/
│       ├── menu.py  # Lógica del estado del menú
│       └── nivel1.py # Nivel de plataformas
│
└── mario_game.py    # Corazón del juego (Controlador de estados)