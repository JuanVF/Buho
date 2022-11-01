# clases para el manejo de un árbol de sintáxis abstracta
from tipoDatos import TipoDatos
from operandosLogicos import OperandosLogicos
from operandosAritmeticos import OperandosAritmeticos

"""
Clase de nodo general para el árbol de sintaxis abstracta
 - atributos: son la línea, columna y referencias del decorado de los nodos
"""
class NodoArbol:
    atributos: dict

    def __init__(self, atributos = None):
        if atributos is None:
            atributos = {}
        self.atributos = atributos

    # metodo visitante para el decorado
    def visitar(self, visitador):
        return visitador.visitar(self)

    def __str__(self):
        resultado = ""
        resultado += '{},'.format(type(self))

        resultado += self.imprimirAtt(self.atributos)

        return resultado

    # imprime un atributo simple de la clase
    def imprimirAtt(self, atributo):
        if atributo is not None:
            return '{:38}'.format(str(self.atributos))
        else:
            return '{:38}\t'.format('')

    # imprime todos los componentes de una lista en un atributo
    def imprimirListAtt(self, listAtributo):
        resultado = ""
        if listAtributo:
            resultado += '<'

            # Imprime los tipos de los nodos del nivel siguiente
            for nodo in listAtributo[:-1]:
                if nodo is not None:
                    resultado += '{},'.format(type(nodo))

            resultado += '{}'.format(type(listAtributo[-1]))
            resultado += '>'
        return resultado

    # imprime los atributos propios y sus nodos hijos en preorden
    def preorden(self):
        print(self)

"""
Clase de nodo para el manejo de errores
 - error: string que describe el error
 - línea: línea del código original donde se presenta
 - columna: columna del código original donde se presenta
 - sugerencia: recomendación para el tratado del error
"""
class NodoError(NodoArbol):
    error : str
    linea : str
    columna : str
    sugerencia : str

    def __init__(self, error = None, linea = None, columna = None, sugerencia = None, atributos = None):
        super().__init__(atributos)
        self.error = error
        self.linea = linea
        self.columna = columna
        self.sugerencia = sugerencia

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirListAtt(self.error)
        resultado += self.imprimirListAtt(self.linea)
        resultado += self.imprimirListAtt(self.columna)
        resultado += self.imprimirListAtt(self.sugerencia)

        return resultado

"""
Clase de nodo principal o raíz del árbol
 - nodos: lista de nodos que componen las funciones y el programa principal
"""
class NodoPrograma(NodoArbol):
    nodos : list

    def __init__(self, nodos = None, atributos = None):
        super().__init__(atributos)
        if nodos is None:
            nodos = []
        self.nodos = nodos

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirListAtt(self.nodos)

        return resultado

    def preorden(self):
        print(self)
        if self.nodos is not None:
            for nodo in self.nodos:
                nodo.preorden()

"""
Clase de nodo general para el manejo de valores
 - tipo: el tipo de dato manejado. Ej: Texto, número, flotante o booleano
   -> tipo se asigna automáticamente en los nodos de tipo específico (como NodoNumero)
"""
class NodoValor(NodoArbol):
    valor : str
    tipo : TipoDatos

    def __init__(self, tipo = None, valor = None, atributos = None):
        super().__init__(atributos)
        self.tipo = tipo

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tipo)

        return resultado

"""
Clase de nodo para el manejo de números
 - valor: el número que se está manejando
"""
class NodoNumero(NodoValor):
    valor : int

    def __init__(self, valor = None, atributos = None):
        super().__init__(TipoDatos.NUMERO, valor, atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

"""
Clase de nodo para el manejo de flotantes
 - valor: el flotante que se está manejando
"""
class NodoFlotante(NodoValor):
    valor : float

    def __init__(self, valor = None, atributos = None):
        super().__init__(TipoDatos.FLOTANTE, valor, atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

"""
Clase de nodo para el manejo de texto
 - valor: el string que se está manejando
"""
class NodoTexto(NodoValor):
    valor : str

    def __init__(self, valor = None, atributos = None):
        super().__init__(TipoDatos.TEXTO, valor, atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

"""
Clase de nodo para el manejo de booleanos
 - valor: verdadero o falso que se está manejando
"""
class NodoBooleano(NodoValor):
    valor : bool

    def __init__(self, valor = None, atributos = None):
        super().__init__(TipoDatos.BOOLEANO, valor, atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

"""
Clase de nodo para el manejo de identificadores
 - identificador: string que del identificador que se está manejando
"""
class NodoIdentificador(NodoArbol):
    identificador : str

    def __init__(self, identificador = None, atributos = None):
        super().__init__(atributos)
        self.identificador = identificador

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.identificador)

        return resultado

"""
Clase de nodo para la llamada a funciones
 - identificador: Nodo identificador con el nombre de la función a invocar
 - params: lista de nodos de valores, identificador o llamada que se pasan
           como parámetros a la función
"""
class NodoLlamada(NodoArbol):
    identificador : NodoIdentificador
    params : list

    def __init__(self, identificador = None, params = None, atributos = None):
        super().__init__(atributos)
        self.identificador = identificador
        self.params = params

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.identificador)
        resultado += self.imprimirListAtt(self.params)

        return resultado

    def preorden(self):
        print(self)
        if self.params is not None:
            for param in self.params:
                param.preorden()

"""
Clase de nodo para las operaciones
"""
class NodoOperacion(NodoArbol):
    primer_valor : NodoValor
    operacion : NodoArbol
    segundo_valor : NodoValor

    def __init__(self, primer_valor = None, operacion = None, segundo_valor = None, atributos = None):
        super().__init__(atributos)

        self.primer_valor = primer_valor
        self.operacion = operacion
        self.segundo_valor = segundo_valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.primer_valor)
        resultado += self.imprimirAtt(self.operacion)
        resultado += self.imprimirAtt(self.segundo_valor)

        return resultado

    def preorden(self):
        print(self)
        if self.primer_valor is not None:
            self.primer_valor.preorden()
        if self.operacion is not None:
            self.operacion.preorden()
        if self.segundo_valor is not None:
            self.segundo_valor.preorden()

"""
Clase de nodo para las operaciones aritméticas
 - operado: nodo valor, identificador, llamada u operación aritmética al que se le aplicara la operación aritmética
 - operador: suma, resta, division, etc...
 - operando: nodo valor, identificador, llamada u operación aritmética que aplica la operación aritmética
"""
class NodoOperacionAritmetica(NodoArbol):
    operado : NodoArbol
    operador : OperandosAritmeticos
    operando : NodoArbol

    def __init__(self, operado = None, operador = None, operando = None, atributos = None):
        super().__init__(atributos)
        self.operado = operado
        self.operador = operador
        self.operando = operando

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.operado)
        resultado += self.imprimirAtt(self.operador)
        resultado += self.imprimirAtt(self.operando)

        return resultado

    def preorden(self):
        print(self)
        if self.operado is not None:
            self.operado.preorden()
        if self.operador is not None:
            print(self.operador)
        if self.operando is not None:
            self.operando.preorden()

"""
Clase de nodo para las operaciones lógicas
 - operado: nodo valor, identificador, llamada u operación lógica al que se le aplicara la operación lógicas
 - operador: and, or, !=, ==, etc...
 - operando: nodo valor, identificador, llamada u operación lógica que aplica la operación lógicas
"""
class NodoOperacionLogica(NodoArbol):
    operado : NodoArbol
    operador : OperandosLogicos
    operando : NodoArbol

    def __init__(self, operado = None, operador = None, operando = None, atributos = None):
        super().__init__(atributos)
        self.operado = operado
        self.operador = operador
        self.operando = operando

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.operado)
        resultado += self.imprimirAtt(self.operador)
        resultado += self.imprimirAtt(self.operando)

        return resultado

    def preorden(self):
        print(self)
        if self.operado is not None:
            self.operado.preorden()
        if self.operador is not None:
            print(self.operador)
        if self.operando is not None:
            self.operando.preorden()

"""
Clase de nodo para las expresiones o asignación de valores a una variable
 - identificador: nodo identificador al que se le asigna los datos
 - valor: nodo valor, llamada, identificador u operación que se le asigna al identificador
"""
class NodoExpresion(NodoArbol):
    identificador : NodoIdentificador
    operacion : NodoOperacion

    def __init__(self, identificador = None, valor = None, atributos = None):
        super().__init__(atributos)
        self.identificador = identificador
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.identificador)
        resultado += self.imprimirAtt(self.valor)

        return resultado

    def preorden(self):
        print(self)
        if self.identificador is not None:
            self.identificador.preorden()

"""
Clase de nodo para las declaraciones de tipo simple
 - tipo: tipo de dato que se le asignara a la variable (Texto, bool, número, float)
 - Expresión: definición del nombre de la variable y valor inicial
"""
class NodoDeclaracionComun(NodoArbol):
    tipo : TipoDatos
    expresion : NodoExpresion

    def __init__(self, tipo = None, expresion = None, atributos = None):
        super().__init__(atributos)
        self.tipo = tipo
        self.expresion = expresion

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tipo)
        resultado += self.imprimirAtt(self.expresion)

        return resultado

"""
Clase de nodo para la escritura en la línea de comando
 - valor: nodo identificador, valor, operación o llamada que se desea escribir
"""
class NodoEscribir(NodoArbol):
    valor : NodoArbol

    def __init__(self, valor = None, atributos = None):
        super().__init__(atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

"""
Clase de nodo para la entrada de datos simple en la línea de comando
 - comentario: si no se desea añadir un comentario = None, de lo contrario un string, 
               nodo identificador, valor, operación o llamada que se desee escribir
 - identificadorObjetivo: nodo identificador donde se guardara la información recibida
"""
class NodoRecibirEntrada(NodoArbol):
    comentario : NodoValor
    identificadorObjetivo : NodoIdentificador

    def __init__(self, comentario = None, identificadorObjetivo = None, atributos = None):
        super().__init__(atributos)
        self.comentario = comentario
        self.identificadorObjetivo = identificadorObjetivo

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.comentario)
        resultado += self.imprimirAtt(self.identificadorObjetivo)

        return resultado

    def preorden(self):
        print(self)
        if self.identificadorObjetivo is not None:
            self.identificadorObjetivo.preorden()

"""
Clase de nodo para el manejo de condiciones en ciclos y bifurcaciones
 - condición: cualquier operación lógica que retorne un booleano
"""
class NodoCondicion(NodoArbol):
    condicion : NodoOperacionLogica

    def __init__(self, condicion = None, atributos = None):
        super().__init__(atributos)
        self.condicion = condicion

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.condicion)

        return resultado

    def preorden(self):
        print(self)
        if self.condicion is not None:
            self.condicion.preorden()

"""
Clase de nodo para el bloque alternativo de una bifurcación
 - instrucciones: lista de nodoArbol con las instrucciones dentro de ese bloque
"""
class NodoSino(NodoArbol):
    instrucciones : list

    def __init__(self, instrucciones = None, atributos = None):
        super().__init__(atributos)
        self.instrucciones = instrucciones

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirListAtt(self.instrucciones)

        return resultado

    def preorden(self):
        print(self)
        if self.instrucciones is not None:
            for nodo in self.instrucciones:
                nodo.preorden()

"""
Clase de nodo para el manejo de bifurcaciones
 - condición: condición por la cual se entra en la bifurcación
 - instrucciones: lista de nodoArbol con las instrucciones dentro de ese bloque
 - sino: si no hay una bifurcación alternativa es = None, de lo contrario es un nodo sino
"""
class NodoSi(NodoArbol):
    condicion : NodoCondicion
    instrucciones : list
    sino : NodoSino

    def __init__(self, condicion = None, instrucciones = None, sino = None, atributos = None):
        super().__init__(atributos)
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.sino = sino

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.condicion)
        resultado += self.imprimirListAtt(self.instrucciones)
        resultado += self.imprimirAtt(self.sino)

        return resultado

    def preorden(self):
        print(self)
        self.condicion.preorden()
        if self.instrucciones is not None:
            for nodo in self.instrucciones:
                nodo.preorden()
        if self.sino is not None:
            self.sino.preorden()

"""
Clase de nodo para el manejo de bucle "while" o mientras
 - condición: nodo condición, con la condición verdadera mientras se ejecute el ciclo
 - instrucciones: lista de nodoArbol con las instrucciones dentro de ese bloque
"""
class NodoMientras(NodoArbol):
    condicion : NodoOperacionLogica
    instrucciones : list

    def __init__(self, condicion = None, instrucciones = None, atributos = None):
        super().__init__(atributos)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.condicion)
        resultado += self.imprimirListAtt(self.instrucciones)

        return resultado

    def preorden(self):
        print(self)
        self.condicion.preorden()
        if self.instrucciones is not None:
            for nodo in self.instrucciones:
                nodo.preorden()

"""
Clase de nodo para el manejo de bucle "for" o desde
 - inicioRango: Número inicial del cual inicia el bucle, puede ser None
 - finalRango: Número final donde se parara el bucle, no puede ser None
 - instrucciones: lista de nodoArbol con las instrucciones dentro de ese bloque
"""
class NodoDesde(NodoArbol):
    inicioRango : int
    finalRango : int
    instrucciones : list

    def __init__(self, inicioRango = None, finalRango = None, instrucciones = None, atributos = None):
        super().__init__(atributos)
        self.inicioRango = inicioRango
        self.finalRango = finalRango
        self.instrucciones = instrucciones

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.inicioRango)
        resultado += self.imprimirAtt(self.finalRango)
        resultado += self.imprimirListAtt(self.instrucciones)

        return resultado

    def preorden(self):
        print(self)
        if self.instrucciones is not None:
            for nodo in self.instrucciones:
                nodo.preorden()

"""
Clase de nodo para la función de ambiente general aleatorio
 - inicioRango: inicio del rango para el número aleatorio, puede ser None
 - finalRango: final del rango para el número aleatorio, puede ser None
"""
class NodoAleatorio(NodoArbol):
    inicioRango : int
    finalRango : int

    def __init__(self, inicioRango = None, finalRango = None, atributos = None):
        super().__init__(atributos)
        self.inicioRango = inicioRango
        self.finalRango = finalRango

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.inicioRango)
        resultado += self.imprimirAtt(self.finalRango)

        return resultado

"""
Clase de nodo para la función de ambiente general aleatorio
 - tiempo: número positivo por el cual se pausara temporalmente el hilo
"""
class NodoDormir(NodoArbol):
    tiempo : int

    def __init__(self, tiempo = None, atributos = None):
        super().__init__(atributos)
        self.tiempo = tiempo

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tiempo)

        return resultado

"""
Clase de nodo para la función de ambiente general absoluto
 - número: número al cual se le aplicara la función de absoluto (|x| = x or |-x| = x)
"""
class NodoValorAbsoluto(NodoArbol):
    numero : int

    def __init__(self, numero = None, atributos = None):
        super().__init__(atributos)
        self.numero = numero

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.numero)

        return resultado

"""
Clase de nodo para la declaración de parámetros dentro de una función
 - tipo: tipo de parámetro que se espera, puede ser texto, número, flotante o booleano
 - identificador: nombre de referencia del parámetro
"""
class NodoParametro(NodoArbol):
    tipo : TipoDatos
    identificador : NodoIdentificador

    def __init__(self, tipo = None, identificador = None, atributos = None):
        super().__init__(atributos)
        self.tipo = tipo
        self.identificador = identificador

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tipo)
        resultado += self.imprimirAtt(self.identificador)

        return resultado

"""
Clase de nodo para la devolución de valores al final de una función
 - valor: valor que se devolverá al retornar el curso principal del programa, puede ser none
"""
class NodoDevuelve(NodoArbol):
    valor : NodoArbol

    def __init__(self, valor = None, atributos = None):
        super().__init__(atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

    def preorden(self):
        print(self)
        if self.valor is not None:
            self.valor.preorden()

"""
Clase de nodo para la declaración de funciones
 - identificador: nodo identificador por el cual se referenciara la función
 - Parámetros: lista de nodos parámetro que recibe la función, puede estar vacía
 - instrucciones: lista de nodos árbol con las instrucciones dentro de esta función
 - devuelve: es el valor retornante de la función y puede ser None (default = 0)
"""
class NodoFuncion(NodoArbol):
    identificador : NodoIdentificador
    parametros : list
    instrucciones : list
    devuelve : NodoDevuelve

    def __init__(self, identificador = None, parametros = None, instrucciones = None, devuelve = None, atributos = None):
        super().__init__(atributos)
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.devuelve = devuelve

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.identificador)
        resultado += self.imprimirAtt(self.parametros)
        resultado += self.imprimirListAtt(self.instrucciones)
        resultado += self.imprimirAtt(self.devuelve)

        return resultado

    def preorden(self):
        print(self)

        if self.parametros is not None:
            for nodo in self.parametros:
                nodo.preorden()
        
        if self.instrucciones is not None:
            for nodo in self.instrucciones:
                nodo.preorden()
                
        if self.devuelve is not None:
            self.devuelve.preorden()

class Arbol:
    raiz : NodoArbol

    def imprimir_preorden(self):
        self.raiz.preorden()
