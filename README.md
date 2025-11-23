# Jump Analyzer — App de saltos con MediaPipe y OpenCV

Esta aplicación permite medir la altura de los saltos con cada pierna usando la webcam y proporciona feedback visual en tiempo real.
Software destinado a pacientes en proceso de readaptación deportiva tras sufrir cualquier lesión de rodilla, ya que muchos estudios comprobaron que la presencia de asimetrías y descompensaciones de fuerza entre la pierna sana y la lesionada supone un factor de riesgo importante de cara a una posible recaída.
---

## Requisitos

- Python 3.10 o superior  
- Webcam conectada  
- Sistema operativo: Windows, Linux o MacOS  

---

## Instalación y ejecución (Entorno virtual)

1. Crear entorno virtual

```bash
# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Descargar modelos

```bash
python download_models.py
```

4. Ejecutar la aplicación

```bash
python main.py
```
