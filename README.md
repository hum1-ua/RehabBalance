# Jump Analyzer — Evaluación de simetría de Salto con MediaPipe

Jump Analyzer es una aplicación en Python que mide la altura de salto de cada pierna mediante visión por computador (MediaPipe + OpenCV), permitiendo detectar asimetrías tras lesiones de rodilla (LCA, menisco, etc.).
El objetivo es ofrecer una herramienta sencilla para valorar la fuerza, simetría y riesgo de compensación, claves para un retorno seguro al deporte.
---
## Características principales

- Detección de pose en tiempo real con MediaPipe Tasks.

- Calibración automática de altura base de cada tobillo.

- Medición real de altura de salto con pierna izquierda y derecha.

- Cálculo de asimetría porcentual entre extremidades.

- Evaluación de riesgo de compensación (umbral: 10%).

- Feedback visual inmediato en pantalla.

- Guardado automático de resultados en CSV (una línea por sesión).
---

## Motivación

- Tras cirugías de rodilla es común presentar déficits de fuerza y asimetrías funcionales.

- Las compensaciones durante el salto están asociadas a un mayor riesgo de rerrotura (hasta ~20%).

- La simetría de salto es una métrica muy utilizada en readaptación deportiva.

- Jump Analyzer permite obtener esta información solo con una webcam, de forma rápida y accesible.
---

## Requisitos

- Python 3.10 o superior  
- Webcam conectada  
- Sistema operativo: Windows, Linux o MacOS  

---

## Instalación y ejecución

```bash
git clone https://github.com/hum1-ua/Jump_Analyzer.git
cd Jump_Analyzer

# Crear entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelos (si no están incluidos)
python download_models.py

# Ejecutar la aplicación
python main.py
```
---

## Interpretación de resultados

La app muestra:

- Altura de salto con pierna izquierda

- Altura de salto con pierna derecha

- Diferencia porcentual

Evaluación del riesgo:

Si la diferencia es menor al 10% se considera que no hay un riesgo significativo.
De lo contrario, existe riesgo de compensación y convendría seguir trabajando la pierna débil