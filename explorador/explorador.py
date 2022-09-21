# Explorador para el lenguaje Buho
from enum import Enum, auto

import re


class TipoComponente(Enum):
    """
    Enum con los tipos de componentes disponibles

    Esta clase tiene mayormente un propósito de validación
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

    Notese que no almacena información auxiliar para mostrar errores lo
    cuál es terrible
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
        Da una representación en texto de la instancia actual usando un
        string de formato de python (ver 'python string formatting' en
        google)
        """

        resultado = f'{self.tipo:30} <{self.texto}> en {self.fila}:{self.columna}'
        return resultado

class Explorador:
    """
    Clase que lleva el proceso principal de exploración y deja listos los
    los componentes léxicos usando para ello los descriptores de
    componente.

    Un descriptor de componente es una tupla con dos elementos:
        - El tipo de componente
        - Un string de regex que describe los textos que son generados para
          ese componente
    """
    regex_componentes=[ (TipoComponente.COMENTARIO, r'^//.*'),
                        (TipoComponente.PALABRA_CLAVE, r'^(funcion|inicio_funcion|final_funcion|recibe|devuelve)'),
                        (TipoComponente.ESCRITURA, r'^(escribir)'),
                        (TipoComponente.RECIBIMIENTO, r'^(recibir_entrada|guardar_en|con_comentario|sin_comentario|guardar_en)'),
                        (TipoComponente.CONDICIONAL, r'^(si|inicio_si|final_si|sino|final_sino)'),
                        (TipoComponente.REPETICION, r'^(mientras|inicia_mientras|final_mientas|desde|hasta|inicia_desde|final_desde)'),
                        (TipoComponente.ESPERA, r'^(dormir)'),
                        (TipoComponente.VALOR_ABSOLUTO, r'^(valor_absoluto)'),
                        (TipoComponente.ALEATORIO, r'^(numerico_aletorio|de|a)'),
                        (TipoComponente.TIPO, r'^(numerico|flotante|texto|bool)'),
                        (TipoComponente.DECLARACION, r'^(tiene)'),
                        (TipoComponente.OPERADOR_ARITMETICO, r'^(mas|menos|por|entre|residuo|elevado|modulo)'),
                        (TipoComponente.OPERADOR_LOGICO, r'^(menor|mayor|menor_igual|mayor_igual|diferente|igual|y|o)'),
                        (TipoComponente.TEXTO, r'^(~.?[^~]*)~'),
                        (TipoComponente.IDENTIFICADOR, r'^([a-z]([a-zA-z0-9])*)'),
                        (TipoComponente.NUMERO, r'^(-?[0-9]+)'),
                        (TipoComponente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
                        (TipoComponente.BOOLEANO, r'^(verdadero|falso)'),
                        (TipoComponente.PUNTUACION, r'^(\n)'),
                        (TipoComponente.BLANCOS, r'^(\s)+')]



    def __init__(self, contenido_archivo):
        self.texto = contenido_archivo
        self.componentes = []

    # Opción 1, retornando las líneas como lista
    # archivo = open("nombre_archivo.ext")
    # lineas = archivo.readlines() # Almacena las líneas del archivo en una lista 
    # archivo.close()    
    # return lineas
 

    # Opción 2, invocando  el procesamiento / lectura de línea por línea
    # archivo = open("nombre_archivo.ext",'r')
    # while True:
    #    siguiente_linea = archivo.readline()

    #    if not siguiente_linea:
    #       break
    #    ***método para leer/procesar línea*** siguiente_linea.strip()

    # archivo.close()

    
    def explorar(self):
        """
        Itera sobre cada una de las líneas y las va procesando de forma que
        se generan los componentes lexicos necesarios en la etapa de
        análisis

        Esta clase no esta manejando errores de ningún tipo
        """

        for linea, index in self.texto:
            try:
                resultado = self.procesar_linea(linea, index + 1)
                self.componentes = self.componentes + resultado
            except tokenIncorrecto as e:
                print(e)

    def imprimir_componentes(self):
        """
        Imprime en pantalla en formato amigable al usuario los componentes
        léxicos creados a partir del archivo de entrada
        """

        for componente in self.componentes:
            print(componente) # Esto funciona por que el print llama al
            # método __str__ de la instancia



    def procesar_linea(self, linea, index):
        """
        Se encarga de obtener cada componente lexico de una linea del codigo
        """
        componentes = []

        linea_original = linea

        while linea != "":
            valido = True
            for tipo, patron in self.regex_componentes:
                coincidencia = re.search(patron, linea)

                if coincidencia is not None:
                    if not self.es_ignorable(tipo):
                        token = coincidencia.group(0)
                        coincidencia_original = re.search(token, linea_original)
                        nuevo_componente = ComponenteLéxico(tipo, token, coincidencia_original.end(),index)
                        componentes.append(nuevo_componente)
                    
                    valido = False
                    linea = linea[coincidencia.end():]
                    break
            if valido:
                # Opcion 1, seleccionar el token equivocado y continuar con la llinea
                # este token es el ultimo de la linea
                if linea.find(" ") == -1:
                    token = linea
                    coincidencia_original = re.search(token, linea_original)
                    
                    # añade el componente de tipo error (se tiene que añadir Error al enum TipoComponente pero no a regex_componentes)
                    nuevo_componente = ComponenteLéxico(TipoComponente.ERROR, token, coincidencia_original.end(),index)
                    componentes.append(nuevo_componente)
                    break
                else:
                    token = linea[0:linea.find(" ")]
                    coincidencia_original = re.search(token, linea_original)
                    # añade el componente de tipo error (se tiene que añadir Error al enum TipoComponente pero no a regex_componentes)
                    nuevo_componente = ComponenteLéxico(TipoComponente.ERROR, token, coincidencia_original.end(),index)
                    componentes.append(nuevo_componente)
                    #continua la exploracion
                    linea = linea[linea.find(" "):]
                    """

                # Opcion 2, dejar de leer la linea y levantar la excepcion
                if linea.find(" ") == -1:
                    if linea.find("\n") == -1:
                        raise tokenIncorrecto(linea, index, re.search(token, linea_original).end())
                    else:
                        raise tokenIncorrecto(linea[0:linea.find("\n")], index, re.search(token, linea_original).end())
                else:
                    raise tokenIncorrecto(linea[0:linea.find(" ")], index, re.search(token, linea_original).end())"""

        return componentes

    def es_ignorable(self, tipo_componente):
        """
        Determina si un componente se puede ignorar o no
        """
        ignorables = [TipoComponente.BLANCOS, TipoComponente.COMENTARIO]

        return tipo_componente in ignorables

"""
Manejador de errores.
Se setea el número de línea desde el main. Tiene que llamar setlineaStr(numlinea) desde la funcion que lleva el contador de linea del codigo
Recibe: lista de ComponenteLéxico "componentes".
Si encuentra un tipo de componente "ERROR", imprime el error.
"""
class ManejadorErrores:

    lineaStr = "En la línea número "
    columnaStr = "En la columna "
    componenteStr = "En el componente " 
    error : str
    msjAdicional : str

    def setlineaStr(self,numlinea):
        self.lineaStr = self.lineaStr + str(numlinea) + ". "

    def setcolumnaStr(self,numcolumna):
        self.columnaStr = self.columnaStr + str(numcolumna) + ". "
    
    def setcomponenteStr(self,numcomponente):
        self.componenteStr = self.componenteStr + str(numcomponente) + ". "

    def getMensajeError(self):
        msj = self.error + """
        ******************************************** Error encontrado ****************************************************** 
        \tUbicado en : """ + self.lineaStr + self.columnaStr + self.componenteStr + """\n\t\t...""" + self.msjAdicional + "..." + """        
        ********************************************************************************************************************
        """
        return msj

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

# Tests
if __name__ == '__main__':
    linea_ejemplo = "Funcion es_par recib5e numerico numero inicio_funcion"

    explorador = Explorador(linea_ejemplo)

    # Test para procesar una linea
    componentes = explorador.procesar_linea(linea_ejemplo, 1)
    
    print("Componentes de la linea:")
    print(linea_ejemplo)

    for componente in componentes:
        print(componente)

    #test de imprimir errores
    numlineatest = 1
    manejadorErrores = ManejadorErrores()
    manejadorErrores.setlineaStr(numlineatest)
    manejadorErrores.manejar_errores(componentes)