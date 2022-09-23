from logger import bcolors, log_error

version_lenguaje = "0.1.0"

"""
    Imprime la ayuda del lenguaje
"""
def help(archivo : str = ""):
    print(f"{bcolors.WARNING}Ayuda: {bcolors.HEADER}buho.py {bcolors.ENDC}[ruta_archivo] [opcion]")
    print(f"""{bcolors.WARNING}
    /╲ ︵ ╱\\
    l (◉) (◉)
    \ ︶ V︶ /
    /↺↺↺↺\\
    ↺↺↺↺↺
    \↺↺↺↺/
    ¯¯/\¯/\¯
    {bcolors.HEADER}
    {bcolors.UNDERLINE}Buho "{version_lenguaje}"{bcolors.ENDC}
    """)
    print("Opciones:")
    print("  -h, -help\t\tMuestra esta ayuda")
    print("  -v, -version\t\tMuestra la versión del lenguaje")
    print("  -e, -explorar\t\tSolo usa el explorador del lenguaje y muestra los componentes léxicos")

"""
    Imprime la versión del lenguaje
"""
def version(archivo : str = ""):
    print(f"buho {version_lenguaje}")