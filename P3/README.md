# Práctica 3 de Visión por Computador.

En esta práctica se hace uso de funciones para detectar contornos como 'threshold' (para obtener una imagen binaria) y 'findContours' (para detectar contornos en la imagen) con el fin de detectar objetos en una imagen y ser capaces de categorizarlos.

## 3.1. Objetivos

1. Aprender a extraer información geométrica de una imagen.
2. Categorizar los objetos a partir de dicha información.

## 3.2. Tarea 1: Capturar una o vacias imágenes con monedas no solapadas y visualizarla(s). 

Para realizar esta parte de la primera tarea se ha creado la función 'mostrar_imagenes' que acepta como parámetros una lista con las rutas a las imágenes que se desean visualizar y otra lista con los títulos que se desea poner en cada imagen (este último parámetro, por defecto, se acepta vacío).

La función mencionada hace uso de un pequeño algoritmo para mostrar todas las imágenes en una sola con el módulo 'matplotlib'.

Se hace uso de manejo de errores en caso de que el tamaño de las listas pasadas por parámetro no sean del mismo tamaño.

El resultado es algo similar a lo que vemos en la siguiente imagen:

![**Imagen 1.** Visualización de imágenes haciendo uso de la funcion creada.](/P3/assets/img1.png)

### 3.2.1. Identificar de forma interactica una monedar de un valor determinado en la imagen. 

### 3.2.2. Mostrar en pantalla el número de monedas y la cantidad de dinero presente en la imagen. 

### 3.2.3. ¿Qué problemas se han encontrado?

## Extras: Considerar que la imagen pueda contener objetos que no son monedas y/o haya solape entre las monedas. Demo en vivo.