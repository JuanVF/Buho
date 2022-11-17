# Implementa el veficador de ciruelas

from utils.arbolito import NodoDeclaracionComun, NodoDesde, NodoDevuelve, NodoDormir, NodoError, NodoExpresion, \
    NodoIdentificador, NodoOperacion, NodoNumero, NodoFlotante, NodoTexto, NodoAleatorio, NodoBooleano, NodoEscribir, \
    NodoRecibirEntrada, NodoSi, NodoSino, NodoMientras, NodoValorAbsoluto, Arbol, NodoFuncion, NodoParametro, \
    NodoOperacionAritmetica, NodoOperacionLogica, NodoPrograma, NodoLlamada, NodoCondicion, NodoOperando, NodoArbol
from utils.tipoDatos import TipoDatos
from utils.operandosLogicos import OperandosLogicos
from utils.operandosAritmeticos import OperandosAritmeticos

"""
nodos eliminados: 
    visitar_parámetros_invocación
    visitar_instrucción
    visitar_principal
    visitar_bloque_instrucciones
    visitar_expresión_matemática
    visitar_literal
    visitar_numero
"""
class VisitantePython:
    tabuladores = 0
    
    def visitar(self, nodo):
        """
        Este método es necesario por que uso un solo tipo de nodo para
        todas las partes del árbol por facilidad... pero cómo lo hice
        tuanis allá... pues bueno... acá hay que pagar el costo.
        """

        resultado = nodo.visitar(self)

        """if type(nodo) is NodoPrograma:
            resultado = self.visitar_programa(nodo)

        elif type(nodo) is TipoNodo.ASIGNACIÓN:
            resultado = self.visitar_asignación(nodo)

        elif type(nodo) is TipoNodo.EXPRESIÓN_MATEMÁTICA:
            resultado = self.visitar_expresión_matemática(nodo)

        elif type(nodo) is TipoNodo.EXPRESIÓN:
            resultado = self.visitar_expresión(nodo)

        elif type(nodo) is TipoNodo.FUNCIÓN:
            resultado = self.visitar_función(nodo)

        elif type(nodo) is TipoNodo.INVOCACIÓN:
            resultado = self.visitar_invocación(nodo)

        elif type(nodo) is TipoNodo.PARÁMETROS_INVOCACIÓN:
            resultado = self.visitar_parámetros_invocación(nodo)

        elif type(nodo) is TipoNodo.PARÁMETROS_FUNCIÓN:
            resultado = self.visitar_parámetros_función(nodo)

        elif type(nodo) is TipoNodo.INSTRUCCIÓN:
            resultado = self.visitar_instrucción(nodo)

        elif type(nodo) is TipoNodo.REPETICIÓN:
            resultado = self.visitar_repetición(nodo)

        elif type(nodo) is TipoNodo.BIFURCACIÓN:
            resultado = self.visitar_bifurcación(nodo)

        elif type(nodo) is TipoNodo.DIAYSI:
            resultado = self.visitar_diaysi(nodo)

        elif type(nodo) is TipoNodo.SINO:
            resultado = self.visitar_sino(nodo)

        elif type(nodo) is TipoNodo.OPERADOR_LÓGICO:
            resultado = self.visitar_operador_lógico(nodo)

        elif type(nodo) is TipoNodo.CONDICIÓN:
            resultado = self.visitar_condición(nodo)

        elif type(nodo) is TipoNodo.COMPARACIÓN:
            resultado = self.visitar_comparación(nodo)

        elif type(nodo) is TipoNodo.RETORNO:
            resultado = self.visitar_retorno(nodo)

        elif type(nodo) is TipoNodo.ERROR:
            resultado = self.visitar_error(nodo)

        elif type(nodo) is TipoNodo.PRINCIPAL:
            resultado = self.visitar_principal(nodo)

        elif type(nodo) is TipoNodo.BLOQUE_INSTRUCCIONES:
            resultado = self.visitar_bloque_instrucciones(nodo)

        elif type(nodo) is TipoNodo.OPERADOR:
            resultado = self.visitar_operador(nodo)

        elif type(nodo) is TipoNodo.VALOR_VERDAD:
            resultado = self.visitar_valor_verdad(nodo)

        elif type(nodo) is TipoNodo.COMPARADOR:
            resultado = self.visitar_comparador(nodo)

        elif type(nodo) is TipoNodo.TEXTO:
            resultado = self.visitar_texto(nodo)

        elif type(nodo) is TipoNodo.ENTERO:
            resultado = self.visitar_entero(nodo)

        elif type(nodo) is TipoNodo.FLOTANTE:
            resultado = self.visitar_flotante(nodo)

        elif type(nodo) is TipoNodo.IDENTIFICADOR:
            resultado = self.visitar_identificador(nodo)

        else:
            # Puse esta opción nada más para que se vea bonito... 
            raise Exception('En realidad nunca va a llegar acá')"""
        return resultado

    def visitar_programa(self, nodo_actual : NodoPrograma):
        """
        Programa ::= (Comentario | Asignación | Función)* Principal
        """

        instrucciones = []
        # Se ignoran los comentarios

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return '\n'.join(instrucciones)

    def visitar_funcion(self, nodo_actual : NodoFuncion):
        """
        Función ::= (Comentario)? mae Identificador (ParámetrosFunción) BloqueInstrucciones
        """

        resultado = """\ndef {}({}):\n{}"""
        self.tabuladores += 1

        parametros = []
        for nodo in nodo_actual.parametros:
            parametros += [nodo.visitar(self)]

        instrucciones = []
        for nodo in nodo_actual.instrucciones:
            instrucciones += [self.retornar_tabuladores() + nodo.visitar(self)]

        if nodo_actual.devuelve is not None:
            instrucciones += [self.retornar_tabuladores() + nodo_actual.devuelve.visitar(self)]

        self.tabuladores -= 1
        return resultado.format(nodo_actual.identificador, ', '.join(parametros), '\n'.join(instrucciones))

    def visitar_parametro(self, nodo_actual : NodoParametro):
        """
        ParámetrosFunción ::= Identificador (/ Identificador)+
        """

        resultado = """{} : {}"""
        resultado.format(nodo_actual.identificador, self.tipoDatosCambio(nodo_actual.tipo))

    def visitar_devuelve(self, nodo_actual : NodoDevuelve):
        """
        Retorno :: sarpe (Valor)?
        """

        resultado = 'return {}'
        valor = nodo_actual.valor.visitar(self)

        return resultado.format(valor)

    def visitar_mientras(self, nodo_actual : NodoMientras):
        """
        Repetición ::= upee ( Condición ) BloqueInstrucciones
        """

        resultado = """while {}:\n{}"""
        self.tabuladores += 1

        instrucciones = []
        condicion = nodo_actual.condicion.visitar(self)

        # Visita la condición
        for nodo in nodo_actual.instrucciones:
            instrucciones.append(self.retornar_tabuladores() + nodo.visitar(self))

        self.tabuladores -= 1
        return resultado.format(condicion, '\n'.join(instrucciones))

    def visitar_desde(self, nodo_actual : NodoDesde):
        """
        Repetición ::= upee ( Condición ) BloqueInstrucciones
        """

        resultado = """for {} in range({}, {}):\n{}"""
        self.tabuladores += 1

        instrucciones = []
        inicioRango = nodo_actual.inicioRango
        finalRango = nodo_actual.finalRango
        variable = "x" + str(self.tabuladores)

        # Visita la condición
        for nodo in nodo_actual.instrucciones:
            instrucciones.append(self.retornar_tabuladores() + nodo.visitar(self))

        self.tabuladores -= 1
        return resultado.format(variable, inicioRango, finalRango, '\n'.join(instrucciones))

    def visitar_si(self, nodo_actual: NodoSi):
        """
        DiaySi ::= diay siii ( Condición ) BloqueInstrucciones
        """

        resultado = """{}\n{}"""
        resultadoIF = """if {}:\n{}"""
        resultadoELSE = ""
        self.tabuladores += 1

        condicion = nodo_actual.condicion.visitar(self)
        instrucciones = []

        for nodo in nodo_actual.instrucciones:
            instrucciones.append(self.retornar_tabuladores() + nodo.visitar(self))
        resultadoIF = resultadoIF.format(condicion, '\n'.join(instrucciones))

        if nodo_actual.sino is not None:
            resultadoELSE = nodo_actual.sino.visitar(self)

        self.tabuladores -= 1
        return resultado.format(resultadoIF, resultadoELSE)

    def visitar_sino(self, nodo_actual : NodoSino):
        """
        Sino ::= sino ni modo BloqueInstrucciones
        """

        resultado = """else:\n{}"""
        self.tabuladores += 1

        instrucciones = []

        for nodo in nodo_actual.instrucciones:
            instrucciones += [self.retornar_tabuladores() + nodo.visitar(self)]

        self.tabuladores -= 1
        return resultado.format('\n'.join(instrucciones))

    def visitar_llamada(self, nodo_actual : NodoLlamada):
        """
        Invocación ::= Identificador ( ParámetrosInvocación )
        """

        resultado = """{}({})"""

        parametros = []

        for nodo in nodo_actual.params:
            parametros += [nodo.visitar(self)]

        return resultado.format(nodo_actual.identificador, ', '.join(parametros))

    def visitar_declaracion_comun(self, nodo_actual : NodoDeclaracionComun):
        """
        Asignación ::= Identificador metale (Identificador | Literal | ExpresiónMatemática | Invocación )
        """

        return nodo_actual.expresion.visitar(self)

    def visitar_expresion(self, nodo_actual : NodoExpresion):
        """
        Expresión ::= ExpresiónMatemática Operador ExpresiónMatemática
        """
        resultado = """{} = {}"""
        valor = nodo_actual.operacion.visitar(self)
        return resultado.format(nodo_actual.identificador, valor)

    def visitar_operacion_aritmetica(self, nodo_actual : NodoOperacionAritmetica):
        """
        Expresión ::= ExpresiónMatemática Operador ExpresiónMatemática
        """

        resultado = """{} {} {}"""
        operado = nodo_actual.operado.visitar(self)
        operador = ""
        operando = ""
        if nodo_actual.operador is not None:
            operador = self.operandosAritmeticosCambio(nodo_actual.operador)
            operando = nodo_actual.operando.visitar(self)

        return resultado.format(operado, operador, operando)

    def visitar_operacion_logica(self, nodo_actual : NodoOperacionLogica):
        """
        Expresión ::= ExpresiónMatemática Operador ExpresiónMatemática
        """

        resultado = """{} {} {}"""
        operado = nodo_actual.operado.visitar(self)
        operador = ""
        operando = ""
        if nodo_actual.operador is not None:
            operador = self.operandosLogicosCambio(nodo_actual.operador)
            operando = nodo_actual.operando.visitar(self)

        return resultado.format(operado, operador, operando)

    def visitar_numero(self, nodo_actual : NodoNumero):
        """
        Entero ::= (-)?\d+
        """
        return str(nodo_actual.valor)

    def visitar_flotante(self, nodo_actual : NodoFlotante):
        """
        Flotante ::= (-)?\d+.(-)?\d+
        """
        return str(nodo_actual.valor)

    def visitar_texto(self, nodo_actual):
        """
        Texto ::= ~/\w(\s\w)*)?~
        """
        return nodo_actual.valor

    def visitar_booleano(self, nodo_actual : NodoBooleano):
        """
        ValorVerdad ::= (True | False)
        """
        return str(nodo_actual.valor)

    def visitar_identificador(self, nodo_actual : NodoIdentificador):
        """
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        return nodo_actual.identificador

    def visitar_condicion(self, nodo_actual : NodoCondicion):
        """
        Condición ::= Comparación ((divorcio|casorio) Comparación)?
        """
        operaciones = []
        operadores = []

        for nodo in nodo_actual.condicion:
            operaciones += [nodo.visitar(self), ]
        for operador in nodo_actual.operadores:
            operadores += [self.operandosLogicosCambio(operador), ]

        resultado = operaciones[0] + " "
        if len(nodo_actual.operadores) == 0:
            return resultado
        else:
            for i in range(len(operadores)):
                resultado += operadores[i] + " " + operaciones[i+1] + " "
            return resultado

    def retornar_tabuladores(self):
        return "\t" * self.tabuladores

    def tipoDatosCambio(self, tipo : TipoDatos):
        if tipo == TipoDatos.TEXTO:
            return "str"
        elif tipo == TipoDatos.NUMERO:
            return "int"
        elif tipo == TipoDatos.BOOLEANO:
            return "bool"
        elif tipo == TipoDatos.FLOTANTE:
            return "float"
        return ""

    def operandosAritmeticosCambio(self, tipo : OperandosAritmeticos):
        if tipo == OperandosAritmeticos.MAS:
            return "+"
        if tipo == OperandosAritmeticos.MENOS:
            return "-"
        if tipo == OperandosAritmeticos.POR:
            return "*"
        if tipo == OperandosAritmeticos.ENTRE:
            return "/"
        if tipo == OperandosAritmeticos.RESIDUO:
            return "//"
        if tipo == OperandosAritmeticos.ELEVADO:
            return "**"
        if tipo == OperandosAritmeticos.MODULO:
            return "%"
        return ""

    def operandosLogicosCambio(self, tipo : OperandosLogicos):
        if tipo == OperandosLogicos.MENOR:
            return "<"
        if tipo == OperandosLogicos.MAYOR:
            return ">"
        if tipo == OperandosLogicos.MENOR_IGUAL:
            return "<="
        if tipo == OperandosLogicos.MAYOR_IGUAL:
            return "=>"
        if tipo == OperandosLogicos.DIFERENTE:
            return "!="
        if tipo == OperandosLogicos.IGUAL:
            return "=="
        if tipo == OperandosLogicos.Y:
            return "and"
        if tipo == OperandosLogicos.O:
            return "or"
        if tipo == OperandosLogicos.NO:
            return "not"
        return ""

    def visitar_escribir(self, nodo_actual : NodoEscribir):
        resultado = """escribir({})"""
        return resultado.format(nodo_actual.valor)

    def visitar_recibir_entrada(self, nodo_actual : NodoRecibirEntrada):
        resultado = """{} = recibirEntrada({})"""
        return resultado.format(nodo_actual.identificadorObjetivo, nodo_actual.comentario)

    def visitar_aleatorio(self, nodo_actual : NodoAleatorio):
        resultado = """aleatorio({}, {})"""
        return resultado.format(nodo_actual.inicioRango, nodo_actual.finalRango)

    def visitar_dormir(self, nodo_actual : NodoDormir):
        resultado = """dormir({})"""
        return resultado.format(nodo_actual.tiempo)

    def visitar_valor_absoluto(self, nodo_actual : NodoValorAbsoluto):
        resultado = """valorAbsoluto({})"""
        return resultado.format(nodo_actual.numero)

    #-------------------------------------------------todo?-------------------------------------------------------------

    def visitar_error(self, nodo_actual):
        """
        Error ::= safis Valor
        """
        resultado = 'print("\033[91m", {}, "\033[0m", file=sys.stderr)'
        valor = ''

        # Verifico si 'Valor' es un identificador que exista (IDENTIFICACIÓN)
        for nodo in nodo_actual.nodos:
            valor = nodo.visitar(self)

        return resultado.format(valor)