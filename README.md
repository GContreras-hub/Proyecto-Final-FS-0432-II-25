# Proyecto Física Computacional: Dinámica molecular en dos dimensiones basado en el paper: “Traffic jams without bottlenecks-experimental evidence for the physical mechanism of the formation of a jam”

Proyecto de investigación para el proyecto final del curso **FS-0432: Física Computacional**.

## Descripción
Simulación de la Transición de Fase en el Tráfico Vehicular. Este proyecto de física computacional se dedica a simular y analizar la formación espontánea de atascos de tráfico, buscando demostrar que la congestión es una manifestación de una transición de fase colectiva, más que el simple resultado de un obstáculo físico.

El proyecto se basa en un paper japonés de 2008 publicado por New Journal of Physics nombrado ''Traffic jams without bottlenecks-experimental evidence for the physical mechanism of the formation of a jam'' \cite{helbing2002traffic}. El experimento se desarrolla en un entorno simulado de una carretera circular de 230 metros de circunferencia, con 22 vehículos. En este caso se modelan los vehiculos como partículas. La condición inicial es un movimiento homogéneo con velocidad uniforme, ajustando la densidad promedio de vehículos a un valor crítico que configura el inicio de la inestabilidad.

## Objetivos

- Implementar la solución en Python
- Inicializar el sistema a partir de posiciones conocidas y una distribución de velocidades aleatoria.
- Elaborar subrutinas que evalúan si los discos chocan o cambian de velocidad. Calcular las nuevas velocidades y posiciones del sistema y como afecta el flujo de las moléculas.
- Visualizar por medio de matplotlib la posición de cada uno de las partículas dentro de los carriles y guardar el correspondiente archivo para realizar una película al final del cálculo.
- Aumentar el número de particulas presentes.
- Elaborar un histograma de las posiciones de los centros de los discos a lo largo del eje-x.
- Determinar cuantas partículas llegan a congestionar o colapsar un numero n de carriles.
- Visualizar el efecto de presa fantasma en una carretera circular.
- Visualizar/simular el flujo correcto de las partículas.
- Crear documentación.

## Tecnicas y recursos utilizados 

- Python 3
- Jupyter Notebook
- NumPy
- Matplotlib
- Organización modular
- Git y GitHub

## Estructura del repositorio

```plaintext
https://github.com/GContreras-hub/Proyecto-Final-FS-0432-II-25/tree/main
Proyecto-Final-FS-0432-II-25/
│
├── notebook/
│ └── proyecto_final.ipynb 
│
├──Proyecto/
│   ├──mkdocs.yml
│   ├── Mkdocs.png
│   ├── Mkdocs2.png
│   ├──simulacionPoo.py
│    └── docs/
│          ├── index.md
│          ├── Mkdocs.png
│          ├── Mkdocs2.png
│          ├──simulacionPoo.py 
│           └── api/
│                └── simulacion.md
│
├── presentación/
│ └── Diapositivas.pdf # Diapositivas utilizadas para la exposición final
│
├── LICENSE # Licencia MIT
└── README.md # Documentación principal del repositorio
