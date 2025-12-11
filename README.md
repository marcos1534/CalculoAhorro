# 🚀 Finanzas Pro & Arcade Zone

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

**Una plataforma híbrida única: Planificación Financiera Avanzada (FIRE) adaptada a la fiscalidad española + Sala Recreativa Retro competitiva.**

---

## 📋 Descripción

Este proyecto nació con el objetivo de resolver un problema común para el inversor español: **¿Cuánto dinero real me queda después de Hacienda?**

La aplicación combina simulaciones financieras rigurosas (ajustadas a los tramos del IRPF 2024/2025) con un entorno de entretenimiento desarrollado en JavaScript/HTML5 incrustado.

### 🌟 Funcionalidades Principales

#### 📊 Módulo Financiero
* **Simulador FIRE:** Proyección de interés compuesto con aportaciones mensuales y cálculo de impuestos (IRPF del Ahorro) automático.
* **Monitor de Mercado:** Precios en tiempo real de los principales ETFs (S&P 500, MSCI World) y Criptomonedas usando la API de Yahoo Finance (`yfinance`).
* **Máquina del Tiempo:** Herramienta de *backtesting* para ver la rentabilidad histórica de activos.
* **Fiscalidad Española:** Algoritmo propio que aplica los tramos progresivos (19% - 28%) sobre los beneficios.

#### 🕹️ Zona Arcade (Ranking Global)
Una colección de minijuegos clásicos recreados en Canvas/JS sin dependencias externas:
* 🟡 **Pac-Man Style**
* 🧱 **Tetris**
* 👾 **Space Invaders**
* 🦍 **Donkey Kong**
* **Sistema de Récords:** Base de datos SQLite para guardar las mejores puntuaciones (Top 5).

#### 🔐 Gestión de Usuarios
* Sistema de Login y Registro seguro (hashing de contraseñas).
* **Panel de Administrador:** Gestión de usuarios y reseteo de tablas de puntuación.

---

## 🛠️ Instalación y Uso Local

Sigue estos pasos para ejecutar el proyecto en tu ordenador:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com//marcos1534/CalculoAhorro.git)
    cd CalculoAhorro
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

---

## 📂 Estructura del Proyecto

```text
├── app.py                # Entrada principal (Login y Router)
├── database.py           # Gestión de SQLite (Usuarios y Scores)
├── requirements.txt      # Librerías necesarias
├── utils/
│   └── games_data.py     # Lógica de los juegos (HTML/JS Strings)
└── pages/
    ├── 01_📈_Mercado.py
    ├── 02_🧮_Simulador.py
    ├── 03_🔮_Time_Machine.py
    └── 04_🕹️_Arcade.py
