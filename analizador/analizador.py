# Analizador para el lenguaje Buho

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from explorador.explorador import ComponenteLéxico, TipoComponente
from utils.arbolito import NodoExpresion, NodoIdentificador, NodoOperacion, NodoNumero, NodoFlotante, NodoTexto, NodoAleatorio, NodoBooleano

class Analizador:
    componentes_lexicos : list
    cantidad_componentes : int
    posicion_componente_actual : int
    componente_actual : ComponenteLéxico

    def __analizar_expresion(self):
        """
        Expresion ::= Identificador "tiene" Operacion
        """

        nodos_nuevos = []

        # Verificar que el componente actual sea un identificador
        identificador = self.__verificar_identificador()

        # Verificar que el componente actual sea "tiene"
        self.__verificar("tiene")

        # Verificar que el componente actual sea una operacion
        operacion = self.__analizar_operacion()

        return NodoExpresion(identificador, operacion)

    def __analizar_operacion(self):
        """
        Operacion ::= Valor ( (OperadoresAritmeticos | OperadoresLogicos) Valor ) ?
        """
        primer_valor = self.__analizar_valor()

        es_aritmetico = self.componente_actual.tipo == TipoComponente.OPERADOR_ARITMETICO
        es_logico = self.componente_actual.tipo == TipoComponente.OPERADOR_LOGICO

        if not es_aritmetico and not es_logico:
            return NodoOperacion(primer_valor)

        operador = None

        if es_aritmetico:
            operador = self.__analizar_operador_aritmetico()
        
        if es_logico:
            operador = self.__analizar_operador_logico()

        segundo_valor = self.__analizar_valor()

        return NodoOperacion(primer_valor, operacion, segundo_valor)

    def __analizar_operacion_aritmetica(self):
        """
        OperadoresAritmeticos ::=  ("mas" | "menos" | "por" | "entre" | "residuo" | "elevado" | "modulo" )
        TODO: Implementar esto
        """     
        pass

    def __analizar_operacion_logica(self):
        """
        OperadoresLogicos ::= ("menor" | "mayor" | "menor_igual" | "mayor_igual" | "diferente" | "igual" | "y" | "o" | "no")
        TODO: Implementar esto
        """
        pass

    def __analizar_valor(self):
        """
        Valor ::= (Identificador | Numero | Flotante | Texto | Booleano | Aleatorio)
        """
        tipo = self.componente_actual.tipo

        if tipo == TipoComponente.IDENTIFICADOR:
            return self.__verificar_identificador()

        if tipo == TipoComponente.NUMERO:
            return self.__verificar_numero()

        if tipo == TipoComponente.FLOTANTE:
            return self.__verificar_flotante()

        if tipo == TipoComponente.TEXTO:
            return self.__verificar_texto()

        if tipo == TipoComponente.BOOLEANO:
            return self.__verificar_booleano()

        if tipo == TipoComponente.ALEATORIO:
            return self.__analizar_aleatorio()

        """
        @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un valor
        """
        pass

    def __analizar_aleatorio(self):
        """
        Aleatorio::= "numerico_aletorio" ("de" Numero "a" Numero)?
        """

        # Verificar que el componente actual sea "numerico_aletorio"
        self.__verificar("numerico_aletorio")

        if self.componente_actual.texto == "de":
            # Verificar que el componente actual sea "de"
            self.__verificar("de")

            # Verificar que el componente actual sea un numero
            primer_numero = self.__verificar_numero()

            # Verificar que el componente actual sea "a"
            self.__verificar("a")

            # Verificar que el componente actual sea un numero
            segundo_numero = self.__verificar_numero()

            return NodoAleatorio(primer_numero, segundo_numero)
        else:
            return NodoAleatorio()

    def __verificar_numero(self):
        """
        Numero ::= (-)?\d+
        """
        if self.componente_actual.tipo != TipoComponente.NUMERO:
            """
            @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un numero
            """
            pass

        nodo = NodoNumero(self.componente_actual.texto)

        self.__siguiente_componente()

        return nodo

    def __verificar_flotante(self):
        """
        Numero ::=  (-)?([0-9]*[,])[0-9]+
        """
        if self.componente_actual.tipo != TipoComponente.FLOTANTE:
            """
            @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un flotante
            """
            pass

        nodo = NodoFlotante(self.componente_actual.texto)

        self.__siguiente_componente()

        return nodo

    def __verificar_texto(self):
        """
        Texto ::= ^(\").+(\")$
        """
        if self.componente_actual.tipo != TipoComponente.TEXTO:
            """
            @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un texto
            """
            pass

        nodo = NodoTexto(self.componente_actual.texto)

        self.__siguiente_componente()

        return nodo

    def __verificar_booleano(self):
        """
        Booleano ::= ("verdadero" | "falso")
        """
        if self.componente_actual.tipo != TipoComponente.BOOLEANO:
            """
            @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un booleano
            """
            pass

        results = {
            "verdadero": True,
            "falso": False
        }

        """
        Ya el explorador verifico que es uno de esos dos valores
        por lo que no es necesario verificarlo de nuevo
        """
        nodo = NodoBooleano(results[self.componente_actual.texto])

        self.__siguiente_componente()

        return nodo

    def __verificar_identificador(self):
        """
        Identificador ::= [a-z]([a-zA-z0-9])*
        """

        if self.componente_actual.tipo != TipoComponente.IDENTIFICADOR:
            """
            @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un identificador
            """
            pass

        nodo = NodoIdentificador(self.componente_actual.texto)

        self.__siguiente_componente()
        
        return nodo

    def __verificar(self, texto):
        """
        Verifica que el componente actual sea el texto esperado
        """
        if self.componente_actual != texto:
            """
            @Kaled Aqui se deberia levantar una Excepcion de sintaxis incorrecta
            """
            pass

        self.__siguiente_componente()

    def __siguiente_componente(self):
        """
        Avanza al siguiente componente léxico
        """
        self.posicion_componente_actual += 1

        if self.posicion_componente_actual >= self.cantidad_componentes:
            return

        self.componente_actual = self.componentes_léxicos[self.posición_componente_actual]

