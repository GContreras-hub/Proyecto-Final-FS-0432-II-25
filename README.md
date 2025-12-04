# Dinámica Molecular en Dos Y Tres Dimensiones - Discos Sólidos

Proyecto de investigación para el proyecto final del curso **FS-0432: Física Computacional**.

## Descripción
Este proyecto simula un sistema de partículas esféricas discos sólidos interactuando en un espacio cúbico, bajo colisiones elásticas y rebotes en las paredes. Se estudian patrones de movimiento, distribución espacial y comportamiento colectivo usando simulación molecular básica.

## Objetivos

- Implementar clases y estructuras orientadas a objetos en python para representar partículas.
- Aplicar colisiones elásticas entre partículas y rebotes en paredes.
- Simular dinámicamente el sistema durante un tiempo dado.
- Generar histogramas espaciales y visualización de resultados por medio de matplotlib.
- Aplicar principios de paralelismo, eficiencia computacional y buenas prácticas con Git.

## Tecnicas y recursos utilizados 

- Python 3
- Jupyter Notebook
- NumPy
- Matplotlib
- Organización modular (`src/` con `sim.py`, `colisiones.py`, `simulador.py`)
- Git y GitHub

## Estructura del repositorio

```plaintext
DINAMICA-MOLECULAR/
├── src/
│ ├── sim.py # Clase Partícula y generación del sistema
│ ├── colisiones.py # Lógica de colisiones entre partículas
│ └── simulador.py # Bucle principal de simulación
│
├── notebook/
│ └── proyecto_final.ipynb # Notebook principal con ejecución y visualización
│
├── docs/
│ ├── metodologia.md # Documento explicativo del problema, recursos y enfoque
│ ├── explicacion_notebook.md # Explicación rápida para ejecutar el notebook
│ ├── graficos/ # Gráficos en PNG generados por la simulación
│ | ├── parametros.md # Parámetros y condiciones iniciales del sistema usado en las figuras
│ │ ├── Fig1.jpg
│ │ ├── Fig2.jpg
│ │ └── Fig3.jpg
│ └── Reporte_final.pdf # Reporte del proyecto en formato PDF
│
├── docs_web/ # Página HTML con documentación interactiva
│ └── index.html
│
├── presentación/
│ └── Diapositivas.pdf # Diapositivas utilizadas para la exposición final
│
├── requirements.txt # Dependencias del proyecto
├── .gitignore # Exclusión de archivos temporales o locales
├── LICENSE # Licencia MIT
└── README.md # Documentación principal del repositorio
