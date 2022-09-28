<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a>
    <img src="imagenes/buho.jpg" alt="Logo" width="248" height="139">
  </a>

  <h3 align="center">Lenguaje buho</h3>

  <p align="center">
    Un lenguaje inclusivo diseñado especificamente para aquellas personas no videntes que aman programar!
    <br />
    <a href="https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion"><strong>Explora la documentacion »</strong></a>
    <br />
    <br />
    <a href="https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion/Entregable%201%20-%20Gramatica">Explorar gramatica</a>
    ·
    <a href="https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion/Entregable%202%20-%20Explorador">Explorar explorador</a>
    ·
    <a href="https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion/Entregable%202%20-%20Analizador">Explorar analizador</a>
    ·
    <a href="https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion/Entregable%202%20-%20Verificador">Explorar verificador</a>
    ·
    <a href="https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion/Entregable%202%20-%20Generador">Explorar generador</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Acerca del proyecto">Acerca del proyecto</a>
      <ul>
        <li><a href="#Estructura del repositorio">Estructura del repositorio</a></li>
      </ul>
    </li>
    <li>
      <a href="#Empezar a utilizar el proyecto">Empezar a utilizar el proyecto</a>
      <ul>
        <li><a href="#Prerequisitos">Prerequisitos</a></li>
        <li><a href="#Instalacion">Instalacion</a></li>
      </ul>
    </li>
    <li><a href="#Uso">Uso</a></li>
    <li><a href="#Tareas">Tareas</a></li>
    <li><a href="#Licencia">Licencia</a></li>
    <li><a href="#Contactos">Contactos</a></li>
    <li><a href="#Reconocimientos">Reconocimientos</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## Acerca del proyecto

<a>
  <img src="images/screenshot producto.png" alt="Logo" width="746" height="402">
</a>

Hay muchos lenguajes para programar, sin embargo, pocos se centran en facilitar la programacion a las personas con discapacidades y tienen dificultades a la hora de escribir o entener el lenguaje

Estas son las ventajas del lenguaje buho:

-   Se centra en la abolición del uso de signos, nuestro lenguaje se hace fácil de leer por los “lectores de pantalla” que utilizan generalmente nuestra población objetivo.
-   Es más fácil de entender para alguien que está empezando a programar por su sencillez y ser de alto nivel.
-   La estructura del lenguaje permite una fácil comprensión por parte de personas ajenas a la programación, debido a que intenta seguir la estructuras de las oraciones de español.
-   Nuestra mascota es la más adorable :owl:

Nuestro lenguaje esta en desarrollo y se centra en la implementacion de un compilador de 4 pasadas. Esta diseñado para el curso compiladores e interpretes, por lo que sus funcionalidades no seran muy avanzadas por el momento

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Estructura del repositorio

Esta seccion enlista las carpetas y archivos usados dentro del proyecto, asi como la mencion de aquellas librerias utilizadas en el proyecto. Para las carpetas y archivos:

-   .idea es la carpeta con los archivos necesarios para el uso del ide pycharm, por lo que no tienen gran importancia
-   analizador contiene todos los archivos fuente para el funcionamiento del analizador
-   documentacion contiene las carpetas relacionadas con los entregables del proyecto, lo cual incluye:
    ** Entregable 1 - Gramatica contiene el documento tecnico de la gramatica y codigo de ejemplo del lenguaje, asi como el archivo para el reconocimiento del lenguaje por editores de texto
    ** Entregable 2 - Documento tecnico del analizador
-   explorador contiene todos los archivos fuente para el funcionamiento del explorador
-   generador contiene todos los archivos fuente para el funcionamiento del generador
-   imagenes contiene los archivos multimedia utilizados por el proyecto (principalmente la documentacion)
-   utils contiene los archivos de clase utilizados por alguno de las partes del compilador
-   verificador contiene todos los archivos fuente para el funcionamiento del verificador

En la lista de librerias se encuentra:

-   [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Empezar a utilizar el proyecto

Esta es la seccion de instrucciones y comandos utilizados para el funcionamiento del compilador

### Prerequisitos

El prerequisito inicial es tener python instalado en el equipo

-   npm
    ```sh
    sudo apt install python3.8
    ```

### Instalacion

1. Clonar el repositorio
    ```sh
    git clone https://gitlab.com/AndreyKdo/proyectocompiladores
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Uso

Para la ejecución unicamente del explorador

```sh
python3 buho.py [direccion_del_archivo] -e
```

Para la ejecución del analizador y sus componentes previos

```sh
python3 buho.py [direccion_del_archivo] -a
```

Para la ejecución verificador y sus componentes previos

```sh
python3 buho.py [direccion_del_archivo] -verificar
```

Para la ejecución generador y sus componentes previos

```sh
python3 buho.py [dirreccion_del_archivo] -g
```

En caso de buscar otras opciones del compilador, utilizar el siguiente comando

```sh
python3 buho.py -h
```

_Para más ejemplos revisar la [Documentation](https://gitlab.com/AndreyKdo/proyectocompiladores/-/tree/main/documentacion)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Tareas

-   [x] Gramatica del lenguaje
    -   [x] Archivo para el reconocimiento del lenguaje en editores de texto
-   [x] Explorador del compilador
    -   [x] Video promocional del lenguaje
    -   [x] Actualizacion del readme en el proyecto
-   [ ] Analizador del compilador
-   [ ] Verificador del compilador
-   [ ] Generador del lenguaje

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## Licencia

Distribuido por la licensia GPL v3. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contactos

Desarrolladores del proyecto

-   Sánchez Sánchez Miguel David - 2019061555 - miguelsanchez712000@gmail.com
-   Sánchez Vargas Kaled - 2019160584 - kaledsv@gmail.com
-   Lumbi Murillo Kimberly Verónica - 2020146765 - kilumur@gmail.com
-   Vargas Fletes Juan José - 2020035292 - juanvfletes@estudiantec.cr
-   Picado Arias Andrey Fabián- 2020135773 - andreypcd@gmail.com

Project Link: [https://gitlab.com/AndreyKdo/proyectocompiladores](https://gitlab.com/AndreyKdo/proyectocompiladores)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Reconocimientos

Paginas y proyectos utilizados como referencia para el proyecto

-   [licensia GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt)
-   [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
-   [Ciruelas](https://gitlab.com/cursos-itcr/ciruelas)
-   [Best Readme Template](https://github.com/othneildrew/Best-README-Template/blob/master/README.md)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
