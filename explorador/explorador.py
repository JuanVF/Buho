# Explorador para el lenguaje Buho

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import bcolors

from enum import Enum, auto

import re

"""
Clase que se encarga de manejar los posibles errores encontrados durante el proceso de exploración
Se setea el número de línea desde el explorador de lienas. Tiene que llamar setlineaStr(numlinea) desde la funcion que lleva el contador de linea del codigo
Recibe: lista de ComponenteLéxico "componentes".
Si encuentra un tipo de componente "ERROR", imprime el error.
"""
class ManejadorErrores:
    def __init__(self):
        self.lineaStr = "En la línea número "
        self.columnaStr = "En la columna "
        self.componenteStr = "En el componente " 
        self.error : str
        self.msjAdicional : str


    # recibe el numero de linea que se debe analizar
    def setlineaStr(self,numlinea):
        self.lineaStr = self.lineaStr + str(numlinea) + ". "

    # recibe el indice de la linea donde empieza el error
    def setcolumnaStr(self,numcolumna):
        self.columnaStr = self.columnaStr + str(numcolumna) + ". "
    
    # recibe el string que no coincide con un regex del lenguaje
    def setcomponenteStr(self,numcomponente):
        self.componenteStr = self.componenteStr + str(numcomponente) + ". "

    # retorna el string con el mensaje de error si se encuentra
    def getMensajeError(self):
        msj = self.error + f"""
        ******************************************** {bcolors.FAIL}Error encontrado{bcolors.ENDC} ****************************************************** 
        {bcolors.WARNING}\tUbicado en : """ + self.lineaStr + self.columnaStr + self.componenteStr + """\n\t\t...""" + self.msjAdicional + "..." + f"""{bcolors.ENDC}        
        ********************************************************************************************************************
        """
        return msj

    # imprime el error para la revision del usuario
    def imprimir_error_Str(self,componente):
        self.error = "...Error de escritura de componente detectado:"
        self.msjAdicional = str(componente) + " mal escrito."

        print(self.getMensajeError())
    
#son solo errores de saber si esta bien o mal escrito
    def manejar_errores(self,componentes):
        for componente in componentes:
            if (componente.tipo == TipoComponente.ERROR):
                self.setcolumnaStr(componente.columna)
                self.setcomponenteStr(componente.texto)
                self.imprimir_error_Str(componente)


class TipoComponente(Enum):
    """
    Enum con los tipos de componentes lexicos del lenguaje
    """
    COMENTARIO = auto()
    PALABRA_CLAVE = auto()
    TIPO = auto()
    IDENTIFICADOR = auto()
    OPERADORES_ARITMETICOS = auto()
    OPERADORES_LOGICOS = auto()
    NUMERO = auto()
    FLOTANTE = auto()
    TEXTO = auto()
    BOOLEANO = auto()
    ESCRITURA = auto()
    RECIBIMIENTO = auto()
    CONDICIONAL = auto()
    REPETICION = auto()
    ESPERA = auto()
    VALOR_ABSOLUTO = auto()
    ALEATORIO = auto()
    DECLARACION = auto()
    OPERADOR_ARITMETICO = auto()
    OPERADOR_LOGICO = auto()
    PUNTUACION = auto()
    BLANCOS = auto()
    ERROR = auto()


class ComponenteLéxico:
    """
    Clase que almacena la información de un componente léxico
    Alamacena el tipo del componente, el string que corresponde y la columna/index de donde se encuentra dentro del documento
    """

    tipo    : TipoComponente
    texto   : str
    columna : int
    fila    : int

    def __init__(self, tipo_nuevo: TipoComponente, texto_nuevo: str, columna_nueva: int, fila_nueva: int):
        self.tipo = tipo_nuevo
        self.texto = texto_nuevo
        self.columna = columna_nueva
        self.fila = fila_nueva

    def __str__(self):
        """
        Retorna una representación de texto con los atributos del componente lexico, con respecto al formato de python
        """

        resultado = f'{bcolors.OKCYAN}{self.tipo:30} {bcolors.OKGREEN}<{self.texto}> en {bcolors.WARNING}{self.fila}:{self.columna}{bcolors.ENDC}'
        return resultado

class Explorador:
    """
    Clase que lleva el proceso principal de exploración y crea la lista de 
    componentes léxicos que se utilizaran en el analizador, mediante el uso 
    descriptores de componente.

    Un descriptor de componente es una tupla con dos elementos:
        - El tipo de componente
        - Un string de regex que describe los textos que son generados para
          ese componente

    La instancia de manejadorErrores se utiliza para presentar los posibles errores al usuario
    """
    manejadorErrores = ManejadorErrores()

    regex_componentes=[ (TipoComponente.COMENTARIO, r'^//.*'),
                        (TipoComponente.PALABRA_CLAVE, r'^(funcion|inicio_funcion|final_funcion|recibe|devuelve)$'),
                        (TipoComponente.ESCRITURA, r'^(escribir)$'),
                        (TipoComponente.RECIBIMIENTO, r'^(recibir_entrada|guardar_en|con_comentario|sin_comentario|guardar_en)$'),
                        (TipoComponente.CONDICIONAL, r'^(si|inicio_si|final_si|sino|final_sino)$'),
                        (TipoComponente.REPETICION, r'^(mientras|inicia_mientras|final_mientas|desde|hasta|inicia_desde|final_desde)$'),
                        (TipoComponente.ESPERA, r'^(dormir)$'),
                        (TipoComponente.VALOR_ABSOLUTO, r'^(valor_absoluto)$'),
                        (TipoComponente.ALEATORIO, r'^(numerico_aletorio|de|a)$'),
                        (TipoComponente.TIPO, r'^(numerico|flotante|texto|bool)$'),
                        (TipoComponente.DECLARACION, r'^(tiene)$'),
                        (TipoComponente.OPERADOR_ARITMETICO, r'^(mas|menos|por|entre|residuo|elevado|modulo)$'),
                        (TipoComponente.OPERADOR_LOGICO, r'^(menor|mayor|menor_igual|mayor_igual|diferente|igual|y|o)$'),
                        (TipoComponente.TEXTO, r'^(".?[^~]*)"$'),
                        (TipoComponente.IDENTIFICADOR, r'^([a-z]([a-zA-z0-9])*)$'),
                        (TipoComponente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)$'),
                        (TipoComponente.NUMERO, r'^(-?[0-9]+)$'),
                        (TipoComponente.BOOLEANO, r'^(verdadero|falso)$'),
                        (TipoComponente.PUNTUACION, r'^(\n)'),
                        (TipoComponente.BLANCOS, r'^(\s)+')]



    def __init__(self, texto):
        self.texto = texto
        self.componentes = []

    
    def explorar(self):
        """
        Itera sobre cada una de las líneas y las va procesando de forma que
        se generan los componentes lexicos necesarios en la etapa de
        análisis

        Se manda el numero de linea y componentes lexicos que se generaron al 
        manejador de errores, por si se encontro un error para comunicarselo
        al usuario
        """

        lineas = self.texto.split("\n") 
        index = 1
        
        for linea in lineas:
            resultado = self.procesar_linea(linea, index)
            self.componentes = self.componentes + resultado

            self.manejadorErrores.setlineaStr(index)
            self.manejadorErrores.manejar_errores(resultado)

            index += 1


    def imprimir_componentes(self):
        """
        Imprime en pantalla en formato amigable al usuario los componentes
        léxicos creados a partir del archivo de entrada
        """

        for componente in self.componentes:
            print(componente)



    def procesar_linea(self, linea, index):
        """
        Se encarga de obtener cada componente lexico de una linea del codigo
        """
        componentes = []

        linea_original = linea

        while linea != "":
            valido = True
            for tipo, patron in self.regex_componentes:
                coincidencia = re.match(patron, linea)

                """ 
                Si el primer string encontrado concuerda con algun regex 
                y no es un componente irrelevante (un comentario o espacio en BLANCOS)
                entonces se guarda en la lista de componentes
                """
                if coincidencia is not None:
                    if not self.es_ignorable(tipo):
                        token = coincidencia.group(0)
                        num_columna = len(linea_original)-len(linea)+len(token)
                        """ 
                        algunos componentes (como los operadores logicos) requieren un espacio 
                        para que identificadores con esas palabras (funcion mayorDeDosNumeros) no sean confundidos por el regex
                        pero este espacio es innecesario dentro del componente lexico
                        """
                        nuevo_componente = ComponenteLéxico(tipo, token, num_columna, index)

                        if token[-1] == " ":
                            nuevo_componente = ComponenteLéxico(tipo, token[:-1], num_columna, index)

                        componentes.append(nuevo_componente)
                    
                    valido = False
                    linea = linea[coincidencia.end():]
                    break
            """
                Si el string termino la comparacion de los descriptores de componentes y no
                se encontro un patron con el que coincide, significa que esta mal formado o es 
                invalido, por lo que se crea un componente ERROR para que el manejadorErrores lo reconozca
            """
            if valido:
                # el string error es el ultimo de la linea, por lo que se puede terminar la exploración de la linea
                token = linea[0:linea.find(" ")]

                # añade el componente de tipo error (se tiene que añadir Error al enum TipoComponente pero no a regex_componentes)
                nuevo_componente = ComponenteLéxico(TipoComponente.ERROR, token, len(linea_original)-len(linea)+len(token),index)
                componentes.append(nuevo_componente)

                if linea.find(" ") == -1:
                    break
                # Despues del string con error se puede seguir explorando la linea
                else:
                    #continua la exploracion
                    linea = linea[linea.find(" "):]

        return componentes

    def es_ignorable(self, tipo_componente):
        """
        Determina si un componente es irrelevante para la lista de componentes, como los comentarios o espacios
        """
        ignorables = [TipoComponente.BLANCOS, TipoComponente.COMENTARIO]

        return tipo_componente in ignorables


"""
    Dado un archivo de texto, se encarga de crear los componentes léxicos
"""
def invocar_explorador(contenido_archivo):
    explorador = Explorador(contenido_archivo)

    lineas = explorador.explorar()

    explorador.imprimir_componentes()
