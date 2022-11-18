# Implementa el visitador del generador de buho

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

    def visitar_programa(self, nodo_actual : NodoPrograma):
        """
        Programa::= (Comentario | Declaracion | Expresion | Operandos | Funcion*
        """

        instrucciones = []
        # Se ignoran los comentarios

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return '\n'.join(instrucciones)

    def visitar_funcion(self, nodo_actual : NodoFuncion):
        """
        Funcion ::= "funcion" Identificador Parametros? "inicio_funcion" (Instruccion+)? Devuelve "final_funcion."
        """

        resultado = """\ndef {}({}):\n{}"""
        self.tabuladores += 1
        identificador = nodo_actual.identificador.visitar(self)

        parametros = []
        if nodo_actual.parametros is not None:
            for nodo in nodo_actual.parametros:
                parametros += [nodo.visitar(self)]

        instrucciones = []
        for nodo in nodo_actual.instrucciones:
            instrucciones += [self.retornar_tabuladores() + nodo.visitar(self)]

        if nodo_actual.devuelve is not None:
            instrucciones += [self.retornar_tabuladores() + nodo_actual.devuelve.visitar(self)]

        self.tabuladores -= 1
        return resultado.format(identificador, ', '.join(parametros), '\n'.join(instrucciones))

    def visitar_parametro(self, nodo_actual : NodoParametro):
        """
        Parametro ::= Tipo Identificador
        """
        identificador = nodo_actual.identificador.visitar(self)
        resultado = """{} : {}"""
        return resultado.format(identificador, self.tipoDatosCambio(nodo_actual.tipo))

    def visitar_devuelve(self, nodo_actual : NodoDevuelve):
        """
       Devuelve ::= "devuelve" (Valor)? "\n"
        """

        resultado = 'return {}'
        valor = nodo_actual.valor.visitar(self)

        return resultado.format(valor)

    def visitar_mientras(self, nodo_actual : NodoMientras):
        """
        Mientras ::= "mientras" Condición "inicia_mientras" Instruccion+ "final_mientras"
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
        Desde ::= "desde" Numero "hasta" Numero "inicia_desde" Instruccion+ "final_desde"
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
        Si ::= "si" Condicion "inicio_si" Instruccion+ "final_si" ("\n" Sino)?
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
        self.tabuladores -= 1

        if nodo_actual.sino is not None:
            resultadoELSE = nodo_actual.sino.visitar(self)

        return resultado.format(resultadoIF, resultadoELSE)

    def visitar_sino(self, nodo_actual : NodoSino):
        """
        Sino ::= "sino" Instruccion+ "final_sino"
        """

        resultado = self.retornar_tabuladores() + """else:\n{}"""
        self.tabuladores += 1

        instrucciones = []

        for nodo in nodo_actual.instrucciones:
            instrucciones += [self.retornar_tabuladores() + nodo.visitar(self)]

        self.tabuladores -= 1
        return resultado.format('\n'.join(instrucciones))

    def visitar_llamada(self, nodo_actual : NodoLlamada):
        """
        Llamada ::= "llamar" Identificador ("recibe" Parametro+)?
        """

        resultado = """{}({})"""

        identificador = nodo_actual.identificador.visitar(self)
        parametros = []

        for nodo in nodo_actual.params:
            parametros += [nodo.visitar(self)]

        return resultado.format(identificador, ', '.join(parametros))

    def visitar_declaracion_comun(self, nodo_actual : NodoDeclaracionComun):
        """
        DeclaracionComun ::= Tipo Expresion
        """

        return nodo_actual.expresion.visitar(self)

    def visitar_expresion(self, nodo_actual : NodoExpresion):
        """
        Expresion::= Identificador "tiene" (Operacion | Valor) "\n"
        """
        resultado = """{} = {}"""
        identificador = nodo_actual.identificador.visitar(self)
        valor = nodo_actual.operacion.visitar(self)
        return resultado.format(identificador, valor)

    def visitar_operacion_aritmetica(self, nodo_actual : NodoOperacionAritmetica):
        """
        Operacion ::= Valor (OperadoresArtimeticos) Valor
        """

        resultado = """{}{}{}"""
        operado = nodo_actual.operado.visitar(self)
        operador = ""
        operando = ""
        if nodo_actual.operador is not None:
            operador = self.operandosAritmeticosCambio(nodo_actual.operador)
            operando = nodo_actual.operando.visitar(self)

        return resultado.format(operado, operador, operando)

    def visitar_operacion_logica(self, nodo_actual : NodoOperacionLogica):
        """
        Operacion ::= Valor (OperadoresLogicos) Valor
        """

        resultado = """{}{}{}"""
        operado = nodo_actual.operado.visitar(self)
        operador = ""
        operando = ""
        if nodo_actual.operador is not None:
            operador = self.operandosLogicosCambio(nodo_actual.operador)
            operando = nodo_actual.operando.visitar(self)

        return resultado.format(operado, operador, operando)

    def visitar_numero(self, nodo_actual : NodoNumero):
        """
        Numero ::= (-)?\d+
        """
        return str(nodo_actual.valor)

    def visitar_flotante(self, nodo_actual : NodoFlotante):
        """
        Flotante ::= (-)?([0-9]*[,])[0-9]+
        """
        return str(nodo_actual.valor)

    def visitar_texto(self, nodo_actual: NodoTexto):
        """
        Texto ::= ^(\").+(\")$
        """
        return nodo_actual.valor

    def visitar_booleano(self, nodo_actual : NodoBooleano):
        """
        Booleano ::= ("verdadero" | "falso")
        """
        return str(nodo_actual.valor)

    def visitar_identificador(self, nodo_actual : NodoIdentificador):
        """
        Identificador ::= [a-z]([a-zA-z0-9])*
        """
        return nodo_actual.identificador

    def visitar_condicion(self, nodo_actual : NodoCondicion):
        """
        Condicion ::= Comparacion (("y" | "o")| Comparacion)?
        """
        operaciones = []
        operadores = []

        for nodo in nodo_actual.condicion:
            operaciones += [nodo.visitar(self), ]
        for operador in nodo_actual.operadores:
            operadores += [self.operandosLogicosCambio(operador), ]

        resultado = operaciones[0] + " "
        if len(nodo_actual.operadores) == 0:
            return operaciones[0]
        else:
            for i in range(len(operadores)):
                resultado += operadores[i] + " " + operaciones[i+1] + " "
            return resultado

    def retornar_tabuladores(self):
        return "\t" * self.tabuladores

    def visitar_escribir(self, nodo_actual : NodoEscribir):
        """
        Escribir ::= "escribir" (Booleano | Numero | Texto | Identificador)*
        """
        resultado = """escribir({})"""
        return resultado.format(nodo_actual.valor.visitar(self))

    def visitar_recibir_entrada(self, nodo_actual : NodoRecibirEntrada):
        """
        Recibir_entrada ::= "recibir_entrada" ("con_comentario" (Booleano | Numero| Texto) | "sin_comentario" ) Guardar_en
        """
        resultado = """{} = recibirEntrada({})"""
        identificador = nodo_actual.identificadorObjetivo.visitar(self)
        return resultado.format(identificador, nodo_actual.comentario.visitar(self))

    def visitar_aleatorio(self, nodo_actual : NodoAleatorio):
        """
        Aleatorio::= "numerico_aletorio" ("de" Numero "a" Numero)?
        """
        resultado = """aleatorio({}, {})"""
        return resultado.format(nodo_actual.inicioRango, nodo_actual.finalRango)

    def visitar_dormir(self, nodo_actual : NodoDormir):
        """
        Dormir ::= "dormir" Numero
        """
        resultado = """dormir({})"""
        return resultado.format(nodo_actual.tiempo)

    def visitar_valor_absoluto(self, nodo_actual : NodoValorAbsoluto):
        """
        ValorAbsoluto ::= "valor_absoluto" Numero
        """
        resultado = """valorAbsoluto({})"""
        return resultado.format(nodo_actual.numero)

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
