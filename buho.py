import sys

from logger import bcolors, log_error
from ayuda import help, version
from explorador.explorador import invocar_explorador
from analizador.analizador import invocar_analizador
from verificador.verificador import invocar_verificador
from generador.generador import invocar_generador

"""
    Opciones de ejecución para el lenguaje buho
"""
opciones = {
    "-h": help,
    "-help": help,
    "-ayuda": help,
    "-version": version,
    "-ver": version,
    "-e": invocar_explorador,
    "-a": invocar_analizador,
    "-v": invocar_verificador,
    "-g": invocar_generador,
    "-explorar": invocar_explorador,
    "-analizar": invocar_analizador,
    "-verificar": invocar_verificador,
    "-generar": invocar_generador
}

"""
    Lee un archivo y retorna su contenido
"""
def leer_archivo(ruta):
    try:
        archivo = open(ruta, "r")
        return archivo.read()
    except FileNotFoundError:
        log_error(f"No se encontró el archivo '{ruta}'")
        help()
        sys.exit(1)

"""
    Punto de entrada del programa
"""
def main():
    cantidad_argumentos = len(sys.argv)

    """
        Verificamos si el usuario no ha ingresado ningún argumento
    """
    if cantidad_argumentos <= 1:
        log_error("No se ha ingresado ningún argumento")
        help()
        sys.exit(1)

    ruta_archivo = sys.argv[1]

    archivo = leer_archivo(ruta_archivo)

    """
        Verificamos si el usuario ha ingresado una opción
    """
    if cantidad_argumentos > 2:
        opcion = sys.argv[2]

        if opcion in opciones:
            opciones[opcion](archivo)
        else:
            log_error(f"La opción {opcion} no es válida")
            help()
            sys.exit(1)

if __name__ == "__main__":
    main()
