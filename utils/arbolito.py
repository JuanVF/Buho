from tipoDatos import TipoDatos
from operandosLogicos import OperandosLogicos
from operandosAritmeticos import OperandosAritmeticos

class NodoArbol:
    contenido : str
    atributos: dict

    def __init__(self, contenido = None, atributos = None):
        if atributos is None:
            atributos = {}
        self.contenido = contenido
        self.atributos = atributos

    def visitar(self, visitador):
        return visitador.visitar(self)

    def __str__(self):
        resultado = ""
        resultado += '{},'.format(type(self))
        if self.contenido is not None:
            resultado += '{:10}\t'.format(self.contenido)
        else:
            resultado += '{:10}\t'.format('')

        resultado += self.imprimirAtt(self.atributos)

        return resultado

    def imprimirAtt(self, atributo):
        if atributo is not None:
            return '{:38}'.format(str(self.atributos))
        else:
            return '{:38}\t'.format('')

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

    def preorden(self):
        print(self)

class NodoError(NodoArbol):
    error : str
    linea : str
    columna : str
    sugerencia : str

    def __init__(self, contenido = None, atributos = None, error = None, linea = None, columna = None, sugerencia = None):
        super().__init__(contenido, atributos)
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

class NodoPrograma(NodoArbol):
    nodos : list

    def __init__(self, contenido = None, atributos = None, nodos = None):
        super().__init__(contenido, atributos)
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

class NodoValor(NodoArbol):
    tipo : TipoDatos

    def __init__(self, contenido = None, atributos = None, tipo = None):
        super().__init__(contenido, atributos)
        self.tipo = tipo

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tipo)

        return resultado

class NodoNumero(NodoValor):
    valor : int

    def __init__(self, contenido = None, atributos = None, valor = None):
        super().__init__(contenido, atributos, TipoDatos.NUMERO)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

class NodoFlotante(NodoValor):
    valor : float

    def __init__(self, contenido = None, atributos = None, valor = None):
        super().__init__(contenido, atributos, TipoDatos.FLOTANTE)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

class NodoTexto(NodoValor):
    valor : str

    def __init__(self, contenido = None, atributos = None, valor = None):
        super().__init__(contenido, atributos, TipoDatos.TEXTO)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

class NodoBooleano(NodoValor):
    valor : bool

    def __init__(self, contenido = None, atributos = None, valor = None):
        super().__init__(contenido, atributos, TipoDatos.BOOLEANO)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

class NodoIdentificador(NodoArbol):
    identificador : str

    def __init__(self, contenido = None, atributos = None, identificador = None):
        super().__init__(contenido, atributos)
        self.identificador = identificador

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.identificador)

        return resultado

class NodoLlamada(NodoArbol):
    identificador : NodoIdentificador
    params : list

    def __init__(self, contenido = None, atributos = None, identificador = None, params = None):
        super().__init__(contenido, atributos)
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

class NodoOperacionAritmetica(NodoArbol):
    operado : NodoArbol
    operador : OperandosAritmeticos
    operando : NodoArbol

    def __init__(self, contenido = None, atributos = None, operado = None, operador = None, operando = None):
        super().__init__(contenido, atributos)
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

class NodoOperacionLogica(NodoArbol):
    operado : NodoArbol
    operador : OperandosLogicos
    operando : NodoArbol

    def __init__(self, contenido = None, atributos = None, operado = None, operador = None, operando = None):
        super().__init__(contenido, atributos)
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

class NodoExpresion(NodoArbol):
    identificador : NodoIdentificador
    valor : NodoArbol

    def __init__(self, contenido = None, atributos = None, identificador = None, valor = None):
        super().__init__(contenido, atributos)
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

class NodoDeclaracionComun(NodoArbol):
    tipo : TipoDatos
    expresion : NodoExpresion

    def __init__(self, contenido = None, atributos = None, tipo = None, expresion = None):
        super().__init__(contenido, atributos)
        self.tipo = tipo
        self.expresion = expresion

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tipo)
        resultado += self.imprimirAtt(self.expresion)

        return resultado

class NodoEscribir(NodoArbol):
    valor : NodoArbol

    def __init__(self, contenido = None, atributos = None, valor = None):
        super().__init__(contenido, atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

class NodoRecibirEntrada(NodoArbol):
    comentario : NodoValor
    identificadorObjetivo : NodoIdentificador

    def __init__(self, contenido = None, atributos = None, comentario = None, identificadorObjetivo = None):
        super().__init__(contenido, atributos)
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

class NodoCondicion(NodoArbol):
    condicion : NodoOperacionLogica
    operadorLogico : OperandosLogicos.Y or OperandosLogicos.O
    otraCondicion : NodoOperacionLogica

    def __init__(self, contenido = None, atributos = None, condicion = None, operadorLogico = None, otraCondicion = None):
        super().__init__(contenido, atributos)
        self.condicion = condicion
        self.operadorLogico = operadorLogico
        self.otraCondicion = otraCondicion

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.condicion)
        resultado += self.imprimirAtt(self.operadorLogico)
        resultado += self.imprimirAtt(self.otraCondicion)

        return resultado

    def preorden(self):
        print(self)
        if self.condicion is not None:
            self.condicion.preorden()
        print(self.operadorLogico)
        if self.otraCondicion is not None:
            self.otraCondicion.preorden()

class NodoSino(NodoArbol):
    instrucciones : list

    def __init__(self, contenido = None, atributos = None, instrucciones = None):
        super().__init__(contenido, atributos)
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

class NodoSi(NodoArbol):
    condicion : NodoCondicion
    instrucciones : list
    sino : NodoSino

    def __init__(self, contenido = None, atributos = None, condicion = None, instrucciones = None, sino = None):
        super().__init__(contenido, atributos)
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

class NodoMientras(NodoArbol):
    condicion : NodoOperacionLogica
    instrucciones : list

    def __init__(self, contenido = None, atributos = None, condicion = None, instrucciones = None):
        super().__init__(contenido, atributos)
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

class NodoDesde(NodoArbol):
    inicioRango : int
    finalRango : int
    instrucciones : list

    def __init__(self, contenido = None, atributos = None, inicioRango = None, finalRango = None, instrucciones = None):
        super().__init__(contenido, atributos)
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

class NodoAleatorio(NodoArbol):
    inicioRango : int
    finalRango : int

    def __init__(self, contenido = None, atributos = None, inicioRango = None, finalRango = None):
        super().__init__(contenido, atributos)
        self.inicioRango = inicioRango
        self.finalRango = finalRango

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.inicioRango)
        resultado += self.imprimirAtt(self.finalRango)

        return resultado

class NodoDormir(NodoArbol):
    tiempo : int

    def __init__(self, contenido = None, atributos = None, tiempo = None):
        super().__init__(contenido, atributos)
        self.tiempo = tiempo

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tiempo)

        return resultado

class NodoValorAbsoluto(NodoArbol):
    numero : int

    def __init__(self, contenido = None, atributos = None, numero = None):
        super().__init__(contenido, atributos)
        self.numero = numero

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.numero)

        return resultado

class NodoParametro(NodoArbol):
    tipo : TipoDatos
    identificador : NodoIdentificador

    def __init__(self, contenido = None, atributos = None, tipo = None, identificador = None):
        super().__init__(contenido, atributos)
        self.tipo = tipo
        self.identificador = identificador

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.tipo)
        resultado += self.imprimirAtt(self.identificador)

        return resultado

class NodoDevuelve(NodoArbol):
    valor : NodoArbol

    def __init__(self, contenido = None, atributos = None, valor = None):
        super().__init__(contenido, atributos)
        self.valor = valor

    def __str__(self):
        resultado = super().__str__()
        resultado += self.imprimirAtt(self.valor)

        return resultado

    def preorden(self):
        print(self)
        if self.valor is not None:
            self.valor.preorden()

class NodoFuncion(NodoArbol):
    identificador : NodoIdentificador
    parametros : list
    instrucciones : list
    devuelve : NodoDevuelve

    def __init__(self, contenido = None, atributos = None, identificador = None, parametros = None, instrucciones = None, devuelve = None):
        super().__init__(contenido, atributos)
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