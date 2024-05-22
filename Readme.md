# El Problema de la Ubicación de Instalaciones de Capacidad Acotada (PUICA)
## Proyecto 2 Análisis y Diseño de Algoritmos II

Este repositorio contiene el código para solucionar el problema de ubicar instalaciones de capacidad acotada, el cual fue abordado utilizando MiniZinc y Python. Se incluyen el modelo utilizado y el programa para visualizar entradas y salidas de forma gráfica.

### Integrantes
- Javier E. Díaz Posso - 1740763
- Daniel A. Mora Muñoz - 1841563
- Daniel F. Rosero Zemanate - 1929347
- Miguel A. Velasco Escobar - 1843152

### Contenido de la entrega
En el repositorio se entrega, el modelo llamado ```PUICA.mzn```, y un archivo de datos utilizado para escribir la información que se lee en los archivos de prueba y los ingresados en la interfaz, llamado ```DatosPUICA.mzn```, este ultimo varía durante la ejecución del programa.

En la carpeta PUICAGUIFuentes se encuentra el archivo ```PUICAGUI.py```, el cual contiene la interfaz del programa y el archivo ```requirements.txt``` que contiene los requerimientos que se deben instalar para ejecutar el programa.

En la carpeta DatosPUICA se incluyen los archivos de la bateria de pruebas, con los que fue probado el modelo.

En la carpeta MisInstancias se incluyen 5 archivos de prueba utilizados en el modelo (diferentes de los archivos dados), propuestos para retar los modelos de los compañeros.

# ```Instrucciones de uso```
- Clonar el repositorio
```
git clone https://github.com/Ironwolf1212/Proyecto2ADAII.git
```

Una vez clonado este repositorio, nos dirigimos a la carpeta donde se encuentran los archivos.
### Creación de un ambiente virtual de Python (opcional)

##### En Windows
```
python -m venv .venv
./.venv/Scripts/activate
```
##### En Linux
```
python3 -m venv .venv
./.venv/bin/activate
```

### Instalación de requerimientos

##### En Windows
```
pip install -r PUICAGUIFuentes/requirements.txt
```
##### En Linux
```
pip3 install -r PUICAGUIFuentes/requirements.txt
```

### Ejecución del programa
Finalmente ejecutamos el programa ```PUICAGUI.py``` que se encuentra en el directiorio _PUICAGUIFuentes_.
##### En Windows
```
python PUICAGUIFuentes/PUICAGUI.py
```
##### En Linux
```
python3 PUICAGUIFuentes/PUICAGUI.py
```
