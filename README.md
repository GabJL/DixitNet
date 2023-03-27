# DixitNet
Pequeño juego de preguntas y respuestas usado en RySD (Software) - UMA

## Código

Hay dos pequeños scripts:
* Uno que genera el pdf con los términos (basado en un fichero json con los datos para los términos)
* Uno para gestión el juego y llevar la puntuación. Requiere el fichero de alumnos (para saber nombres y DNIs) y una plantilla para rellenar con las puntuaciones.

## Instrucciones del juego (las originales, aunque algunas cosas no se respetaron):

### ¿Qué grupo soy?
*	Hay dos grupos: el 0 y el 1 (eh, que somos informáticos).
*	El grupo donde estás es el resto de tu DNI/NIE al ser dividido entre 2 (si tu identificador es par eres grupo 0, y si es impar eres grupo 1). 

### ¿Qué roles hay?
*	Hay dos roles: representante (2 por grupo) y participante (todo el resto).
*	Los representantes serán voluntarios si los hay o aleatorios si no hay voluntarios.

### ¿Qué grupo empieza a preguntar?
*	El grupo que tenga al representante más joven.

### ¿Cómo va cada turno?
*	Mediante una ruleta se elige el tema de la siguiente pregunta.
*	Preparación de la pregunta (Representantes):
* *	Eligen un término al azar de los que hay de ese tema.
  *	Cada término viene con una descripción.
  *	Los representantes deben elegir hasta 8 palabras para que el resto de alumno intenten acertar el término (en 1 minuto).
  *	Para elegir las palabras no pueden hablar, pero pueden comunicarse por escrito. 
  *	Al final las 8 palabras deben aparecer apuntadas en la ficha pasada.
  *	Entre las palabras elegidas no pueden aparecer las del término, y solo puede aparecer a lo sumo dos palabras de la descripción (y que no aparezcan en el término).
  *	Palabras derivadas o en otros idiomas se consideran que son la misma palabra.
*	Realización de la pregunta (Todos):
*  *	Los representantes leen 2 de las palabras elegidas (las que quieran que no se hayan dicho).
  *	Si alguien quiere participar levanta la mano y se le da oportunidad al más rápido.
  *	Si acierta se reparten puntos y acaba el turno.
  *	Si falla, el jugador ya no puede responder más para ese término y se da la oportunidad a si alguien del otro grupo quiere intentarlo (si falla también se “elimina” para ese término).
  *	El proceso se repite hasta acabar las palabras o acertar.
*	Tras acabar un turno, pasa a otro turno con el equipo contrario.

### Puntos del juego:
*	La cantidad de puntos depende de cómo de rápido se acertó.
*	Para los representantes que han hecho la pregunta: 2 puntos si se acertó con 4 palabras o menos, 1 se si acertó con más de 4 palabras y 0 si no se acertó.
*	Para el acertante: 4 si acertó con 2 palabras, 3 si acertó con 4 palabras, 2 si acertó con 6 palabras y 1 si acertó con 8 palabras.
*	Para el grupo del acertante: 4 si acertó con 2 palabras, 3 si acertó con 4 palabras, 2 si acertó con 6 palabras y 1 si acertó con 8 palabras.

###Puntos de participación (los que valen en la asignatura):
*	Los puntos que recibe el alumno se calculan como:
*  *	Puntos de grupo ponderados: 10*puntos del grupo / (puntos del grupo 0 + puntos del grupo 1)
  *	Puntos de participación: mínimo (10, puntos de grupo ponderado + puntos de alumno)
