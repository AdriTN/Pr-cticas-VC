# Práctica 3 de Visión por Computador.

En esta práctica se hace uso de funciones para detectar contornos como **'threshold'** (para obtener una imagen binaria) y **'findContours'** (para detectar contornos en la imagen) con el fin de detectar objetos en una imagen y ser capaces de categorizarlos.

## 3.1. Objetivos

1. Aprender a **extraer información** geométrica de una imagen.
2. **Categorizar** los objetos a partir de dicha información.

## 3.2. Tarea 1: Capturar una o vacias imágenes con monedas no solapadas y visualizarla(s). 

Para realizar esta parte de la primera tarea se ha creado la función **'mostrar_imagenes'** que acepta como parámetros una lista con las rutas a las imágenes que se desean visualizar y otra lista con los títulos que se desea poner en cada imagen (este último parámetro, por defecto, se acepta vacío).

La función mencionada hace uso de un pequeño algoritmo para mostrar todas las imágenes en una sola con el módulo **'matplotlib'**.

Se hace uso de manejo de errores en caso de que el tamaño de las listas pasadas por parámetro no sean del mismo tamaño.

El resultado es algo similar a lo que vemos en la siguiente imagen:

![**Imagen 1.** Visualización de imágenes haciendo uso de la funcion creada.](/P3/assets/img1.png)

### 3.2.1. Identificar de forma interactica una moneda de un valor determinado en la imagen.

Primero se ha creado una función llamada **'detectar_monedas'** que acepta una imagen por parámetro. Dicha función hace lo siguiente:

1. Lee la imagen con **'imread'** de CV2 y la pasa de BGR a RGB.
2. Convierte dicha imagen a escala de grises haciendo uso de **'cvtColor'** con el segundo parámetro **'cv2.COLOR_RGB2GRAY'**.
3. Aplica thresholding para obtener una imagen binaria con **'threshold'** usando como cuarto parámetro **'cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU'**.
4. Obtiene los contornos exteriores con **'findContours'** haciendo uso del parámetro **'RETR_EXTERNAL'** y dibuja los bordes en la imagen original a través de un bucle que aplica un filtro para evitar contornos muy pequeños que no nos interesan.
5. Llama a la función mencionada en 
aplica thresholding para obtener una imagen binaria, obtiene los contornos, dibuja los contornos en la imagen y la muestra con la función mencionada en el **apartado 3.2**.

Se ha creado una clase **Moneda** con el fin de reciclar código para las características de una moneda. Los atributos de la clase son los siguientes:

- **Nombre (str)**: Representa el nombre de la moneda.
- **Valor (int)**: Representa el valor de la moneda.
- **Cantidad (int)**: Cantidad de monedas con las mismas características encontradas.
- **Píxel Mínimo (float)**: Representa el número mínimo de píxeles que tiene una moneda en su diámetro.
- **Píxel Máximo (float)**: Representa el número máximo de píxeles que tiene una moneda en su diámetro.

También se han creado funciones pertenecientes a la clase mencionada con el fin de reciclar código. Las funciones son:

- **resetear_cantidad**: Esta función establece el valor del atributo **'cantidad'** a 0.
- **incrementar_cantidad**: Suma 1 al atributo **'cantidad'** cada vez que se llama.
- **total_valor**: Devuelve el valor total de la moneda en la imagen.
- **mostrar_monedas**: Muestra en forma de tabla toda la información sobre las monedas pasadas por parámetro.
- **calcular_rangos**: Calcula los rángos de píxeles máximo y mínimo que puede tener una moneda.

Cabe recalcar que la clase 'Moneda`está implementada de forma que sea posible usar cualquier tipo de moneda (por este motivo las funciones aceptan un parámetro), sin embargo, para esta práctica haremos uso de la moneda Europea.

EXPLICAR AQUÍ LA PARTE DEL CUADERNO CORRESPONDIENTE A 'Procesar Imagen con Click'. EVITAR LA PARTE EN LA QUE SE ESCRIBE EN LA IMAGEN Y SE IMPRIME EL VALOR TOTAL

### 3.2.2. Mostrar en pantalla el número de monedas y la cantidad de dinero presente en la imagen.

EXPLICAR AQUÍ LA PARTE DONDE SE ESCRIBE EN LA IMAGEN Y SE IMPRIME EL VALOR TOTAL.

### 3.2.3. ¿Qué problemas se han encontrado?

ESTO LO HAGO YO

## 3.2.4. Extras: Considerar que la imagen pueda contener objetos que no son monedas y/o haya solape entre las monedas. Demo en vivo.

EXPLICAR LA FUNCIÓN 'detectar_monedas_mejorado'. DE FORMA DETALLADA.