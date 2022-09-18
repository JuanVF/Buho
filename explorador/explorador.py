# Explorador para el lenguaje Ciruelas (scanner)
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



class ComponenteLéxico:
    """
    Clase que almacena la información de un componente léxico

    Notese que no almacena información auxiliar para mostrar errores lo
    cuál es terrible
    """

    tipo    : TipoComponente
    texto   : str

    def __init__(self, tipo_nuevo: TipoComponente, texto_nuevo: str):
        self.tipo = tipo_nuevo
        self.texto = texto_nuevo

    def __str__(self):
        """
        Da una representación en texto de la instancia actual usando un
        string de formato de python (ver 'python string formatting' en
        google)
        """

        resultado = f'{self.tipo:30} <{self.texto}>'
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
    regex_componentes=[ (TipoComponente.COMENTARIO, r'^//:.*'),
                        (TipoComponente.PALABRA_CLAVE, r'^(funcion|inicio_funcion|final_funcion|recibe|devuelve)'),
                        (TipoComponente.ESCRITURA, r'^(escribir)'),
                        (TipoComponente.RECIBIMIENTO, r'^(recibir_entrada|guardar_en|con_comentario|sin_comentario|guardar_en)'),
                        (TipoComponente.CONDICIONAL, r'^(si|inicio_si|final_si|sino|final_sino)'),
                        (TipoComponente.REPETICION, r'^(mientras|inicia_mientras|final_mientas|desde|hasta|inicia_desde|final_desde)'),
                        (TipoComponente.ESPERA, r'^(dormir)'),
                        (TipoComponente.VALOR_ABSOLUTO, r'^(valor_absoluto)'),
                        (TipoComponente.ALEATORIO, r'^("numerico_aletorio"|de|a)'),
                        (TipoComponente.DECLARACION, r'^("numerico"|"flotante"|"texto"|"bool"|"tiene)'),
                        (TipoComponente.OPERADOR_ARITMETICO, r'^("mas"|"menos"|"por"|"entre"|"residuo"|"elevado"|"modulo")'),
                        (TipoComponente.OPERADOR_LOGICO, r'^("menor"|"mayor"|"menor_igual"|"mayor_igual"|"diferente"|"igual"|"y"|"o")'),
                        (TipoComponente.TEXTO, r'^(~.?[^~]*)~'),
                        (TipoComponente.IDENTIFICADOR, r'^([a-z]([a-zA-z0-9])*)'),
                        (TipoComponente.NUMERO, r'^(-?[0-9]+)'),
                        (TipoComponente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
                        (TipoComponente.BOOLEANO, r'^(verdadero|falso)'),
                        (TipoComponente.PUNTUACION, r'^([\n/)'),
                        (TipoComponente.BLANCOS, r'^(\s)*')]



    def __init__(self, contenido_archivo):
        self.texto = contenido_archivo
        self.componentes = []

    def explorar(self):
        """
        Itera sobre cada una de las líneas y las va procesando de forma que
        se generan los componentes lexicos necesarios en la etapa de
        análisis

        Esta clase no esta manejando errores de ningún tipo
        """

        for linea in self.texto:
            resultado = self.procesar_linea(linea)
            self.componentes = self.componentes + resultado

    def imprimir_componentes(self):
        """
        Imprime en pantalla en formato amigable al usuario los componentes
        léxicos creados a partir del archivo de entrada
        """

        for componente in self.componentes:
            print(componente) # Esto funciona por que el print llama al
            # método __str__ de la instancia


    def procesar_linea(self, linea):
        """
        Toma cada línea y la procesa extrayendo los componentes léxicos.

        Acá se deberían generar los errores y almacenar la información
        adicional necesaria para tener errores inteligentes
        """

        componentes = []

        # Toma una línea y le va cortando pedazos hasta que se acaba
        while(linea !=  ""):

            # Separa los descriptores de componente en dos variables
            for tipo_componente, regex in self.descriptores_componentes:


                # Trata de hacer match con el descriptor actual
                respuesta = re.match(regex, linea)

                # Si hay coincidencia se procede a generar el componente
                # léxico final
                if respuesta is not None :

                    # si la coincidencia corresponde a un BLANCO o un
                    # COMENTARIO se ignora por que no se ocupa
                    if tipo_componente is not TipoComponente.BLANCOS and \
                            tipo_componente is not TipoComponente.COMENTARIO:

                        #Crea el componente léxico y lo guarda
                        nuevo_componente = ComponenteLéxico(tipo_componente, respuesta.group())
                        componentes.append(nuevo_componente)


                    # Se elimina el pedazo que hizo match
                    linea = linea[respuesta.end():]
                    break;

        return componentes
