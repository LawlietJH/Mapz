# Mapz

## En Python: 3.5.0
## Versión Actual: 1.6.4
## Dependencias: Pygame.
## Compatibilidad: Windows y Linux.

- - -

### Instalando Pygame con Pip (Administrador de Paquetes de Python):

__Comando desde Consola:__

```bat
python -m pip install pygame
```
- - -

### Para Linux: Dependencia para Tkinter.

```bash
sudo apt-get install python3-tk
```

## Interacciones: (Pueden Utilizarse Completamente Clics con el Mouse)

__Permite Presionar Las Teclas:__

* __Al Comienzo:__

  * ___Letra 'C':_ Presiona El Botón 'Cargar' que permite Cargar Un Mapa.__
  * ___Letra 'M':_ Presiona El Botón 'Mute' del Tipo ON/OFF Para Silencia o No La Música de Fondo.__
  * ___Letra 'O':_ Presiona El Botón 'Ocultar' del Tipo ON/OFF Para Enmascarar o No el Mapa al Iniciar El Juego.__

* __Una vez Cargado El Mapa: (Selección De Terrenos, Personaje, Costos y Puntos Inicio y Detino)__

  * ___ENTER:_ Presiona El Botón 'Comenzar' que permite Comenzar La Partida (Requiere Haber Seleccionado Un Personaje Primero, Luego Haber Seleccionado Todos Los Terrenos Necesarios para El Mapa y después, haber seleccionado Un Terreno (Con Costo) Para El Punto Inicio y otro para el Punto Destino).__
  * ___Flecha Izquierda:_ Cambia a Página Anterior en Seleccion de Terrenos.__
  * ___Flecha Derecha:_ Cambia a Página Siguiente en Seleccion de Terrenos.__
  * ___Clic Izquierdo (Mouse):_ Seleccion de Punto Inicio y Posteriormente Punto Destino, Dar otro Clic en otro Terreno, Reinicia el Punto Inicio y Destino.__
  * ___Clic Derecho (Mouse):_ Da La Información del Terreno Seleccionado en el Mapa.__
  
* __Una vez Iniciado El Juego: (Interacción Con El Mapa)__

  * ___Tecla 'V':_ Presiona El Botón 'Ver Árbol' del Tipo ON/OFF Para Mostrar o No el Árbol Generado Con El Mapa al Avanzar En El Juego.__
  * ___Tecla 'R':_ Presiona El Botón 'Reniciar' Para Volver a Comenzar La Partida Sin Alterar Nada.__
  * ___Tecla 'P':_ Presiona El Botón 'Seleccionar Personaje' Para Permitir Seleccionar Otro Personaje o Solo Modificar Costos o Modificar Los Puntos Inicio y Destino, asi tambien como poder Cambiar Los Terrenos o El Mapa.__
  * ___Flecha Izquierda y Tecla 'A':_ Avanzan El Personaje A Terreno a la Izquierda (Siempre y Cuando Tenga Costo ese Terreno).__
  * ___Flecha Arriba y Tecla 'W':_ Avanzan El Personaje A Terreno Arriba (Siempre y Cuando Tenga Costo ese Terreno).__
  * ___Flecha Derecha y Tecla 'D':_ Avanzan El Personaje A Terreno a la Derecha (Siempre y Cuando Tenga Costo ese Terreno).__
  * ___Flecha Abajo y Tecla 'S':_ Avanzan El Personaje A Terreno Abajo (Siempre y Cuando Tenga Costo ese Terreno).__
  
* __Una vez Mostrado EL Árbol: (Tiene Estructura de Carpetas)__

  * ___Flecha Izquierda y Tecla 'A':_ Desplaza a la Izquierda.__
  * ___Flecha Arriba y Tecla 'W':_ Desplaza a Arriba.__
  * ___Flecha Derecha y Tecla 'D':_ Desplaza a la Derecha.__
  * ___Flecha Abajo y Tecla 'S':_ Desplaza a Abajo.__
  
  
## Fechas:

### Revisiónes de Proyecto: (Las Penalizaciones y Observaciones se Deben Corregir Aún Después de las Entregas.)
 
* __Parte 1: _05/03/2018 y 07/03/2018_.__
  * ___Calificación:_ 100/100.__
  * ___Penalizaciones:___
    * __No Se Debe Tener Que Cargar De Nuevo El Mapa Para Seleccionar Otro Personaje. -5 Puntos. _(Corregido el 07/03/2018 en v1.4.8)___
  * ___Observaciones:___
    * __En El Terreno Pared Debe Poder Modificar su Costo. _(Corregido el 05/03/2018 en v1.4.5)___
    * __Costos Con Máximo 2 Decimales. _(Corregido el 06/03/2018 en v1.4.6)___
    * __Mostrar Información de Terrenos al Clic derecho de Forma Constante Aún Antes De Comenzar El Juego. _(Corregido el 21/03/2018 en v1.4.9)___
* __Parte 2: _23/04/2018 y 25/04/2018_.__
  * ___Calificación:_ 100/100.__
  * ___Penalizaciones:___
  * ___Observaciones:___
* __Parte 3: _16/05/2018 y 21/05/2018_.__

- - -

### <span style="color:green;">Proyecto Parte 1: Finalizada.</span>
 * <span style="color:blue;">__Versión 1.0:__</span>
   * __v1.0.0: _16/02/2018_, v1.0.2: _16/02/2018_, v1.0.4: _16/02/2018_, v1.0.6: _16/02/2018_, v1.0.8: _17/02/2018___

 * __Versión 1.1:__
   * __v1.1.0: _17/02/2018_, v1.1.2: _18/02/2018_, v1.1.4: _19/02/2018_, v1.1.6: _19/02/2018_, v1.1.8: _19/02/2018___
   
 * __Versión 1.2:__
   * __v1.2.0: _20/02/2018_, v1.2.1: _20/02/2018_, v1.2.2: _20/02/2018_, v1.2.3: _20/02/2018_, v1.2.4: _20/02/2018___
   * __v1.2.5: _20/02/2018_, v1.2.6: _21/02/2018_, v1.2.7: _21/02/2018_, v1.2.8: _21/02/2018_, v1.2.9: _21/02/2018___
   
 * __Versión 1.3:__
   * __v1.3.0: _21/02/2018_, v1.3.1: _23/02/2018_, v1.3.2: _24/02/2018_, v1.3.3: _24/02/2018_, v1.3.4: _24/02/2018___
   * __v1.3.5: _24/02/2018_, v1.3.6: _26/02/2018_, v1.3.7: _27/02/2018_, v1.3.8: _01/03/2018_, v1.3.9: _01/03/2018___
   
 * __Versión 1.4:__
   * __v1.4.0: _02/03/2018_, v1.4.1: _03/03/2018_, v1.4.2: _04/03/2018_, v1.4.3: _04/03/2018_, v1.4.4: _04/03/2018___
   * __v1.4.5: _05/03/2018_, v1.4.6: _06/03/2018_, v1.4.7: _07/03/2018_, v1.4.8: _07/03/2018_, v1.4.9: _21/03/2018_.__

### Proyecto Parte 2: Finalizada.

 * __Versión 1.5:__
   
   * __v1.5.0: _28/03/2018_, v1.5.1: _29/03/2018_, v1.5.2: _15/04/2018_, v1.5.3: _15/04/2018_, v1.5.4: _15/04/2018___
   * __v1.5.5: _16/04/2018_, v1.5.6: _18/04/2018_, v1.5.7: _20/04/2018_, v1.5.8: _20/04/2018_, v1.5.9: _21/04/2018___
   
 * __Versión 1.6:__
   
   * __v1.6.0: _24/04/2018_, v1.6.1: _24/04/2018_.__

### Proyecto Parte 3: Comenzada.

 * __Versión 1.6:__
   
   * __v1.6.2: _04/05/2018_, v1.6.3: _04/05/2018_, v1.6.4: _04/05/2018_.__
