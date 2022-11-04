# Analizador para el lenguaje Buho

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from explorador.explorador import ComponenteLéxico, TipoComponente
from utils.arbolito import NodoDeclaracionComun, NodoDesde, NodoDevuelve, NodoDormir, NodoError, NodoExpresion, NodoIdentificador, NodoOperacion, NodoNumero, NodoFlotante, NodoTexto, NodoAleatorio, NodoBooleano, NodoEscribir, NodoRecibirEntrada, NodoSi, NodoSino, NodoMientras, NodoValorAbsoluto, Arbol

class Analizador:
    componentes_lexicos : list
    cantidad_componentes : int
    posicion_componente_actual : int
    componente_actual : ComponenteLéxico

    def __init__(self, lista_componentes):

        self.componentes_lexicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)

        self.posicion_componente_actual = 0
        self.componente_actual = lista_componentes[0]

        self.asa = Arbol()

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()


    def analizar(self):
        """
        Método principal que inicia el análisis siguiendo el esquema de
        análisis por descenso recursivo
        """
        #self.asa.raiz = self.__analizar_programa() TODO
        return


    def __analizar_expresion(self):
        """
        Expresion ::= Identificador "tiene" Operacion
        """

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
        Error Sintáctico
        """
        nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
        self.componente_actual.fila, self.componente_actual.columna,
        "Debe ser un valor entre Identificador | Numero | Flotante | Texto | Booleano | Aleatorio")
        return nodoError

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


    def __analizar_operando(self):    
        """
        Operandos::= (Escribir | Recibir_entrada | Si | Mientras | Desde | Dormir | ValorAbsoluto)

        OJO! Por favor note que el nombre de la regla es igual a la palabra reservada,
             con la diferencia de que esta última empieza con minúscula.
             En el momento de analizar el componente actual, se debe tomar 
             en cuenta este aspecto para buscarlo adecuadamente (utilizando la palabra reservada)
    
        """
        
        nodos_nuevos = []  

        
        self.__verificar('(')

        # Operandos a elegir, buscamos con minúscula porque así lo inidca la sintáxis. 
        if self.componente_actual.texto == 'escribir':
            nodos_nuevos += [self.__analizar_escribir()]

        elif self.componente_actual.texto == 'recibir_entrada':
            nodos_nuevos += [self.__analizar_recibir_entrada()]

        elif self.componente_actual.texto == 'si':
            nodos_nuevos += [self.__analizar_si()]

        elif self.componente_actual.texto == 'mientras':
            nodos_nuevos += [self.__analizar_mientras()]

        elif self.componente_actual.texto == 'desde':
            nodos_nuevos += [self.__analizar_Desde()]

        elif self.componente_actual.texto == 'dormir':
            nodos_nuevos += [self.__analizar_Dormir()]

        elif self.componente_actual.texto == 'valor_absoluto':
            nodos_nuevos += [self.__analizar_ValorAbsoluto()]    

        else: #Reservado para manejar errores
            nodos_nuevos += [self.__analizar_error()]

        
        self.__verificar(')')

        #return No vi tal cosa como NodoOperando, es NodoFuncion???

    def __analizar_escribir(self):
        """
        Escribir ::= "escribir" (Booleano | Numero | Texto | Identificador)**
        """

        # Se empieza el análisis
        self.__verificar('escribir') #Palabra reservada
        self.__verificar('(')
      
        valor = self.__analizar_valor() # Ojo que esto deja que Flotante y Aleatorio entren, y estos valores no estan contemplados en la gramatica. 

        self.__verificar(')')

        return NodoEscribir(valor)

    def __analizar_recibir_entrada(self):
        """
        Recibir_entrada ::= "recibir_entrada" ("con_comentario" (Booleano | Numero | Texto) | "sin_comentario" ) Guardar_en
        
        Guardar_en ::= "guardar_en" Identificador
        """
        
        # Se empieza el análisis de recibir_entrada
        self.__verificar('recibir_entrada') #Palabra reservada
        self.__verificar('(')

        if self.__verificar('con_comentario'): 
            # Revisar esto porque NO me estoy pasando el comentario por el quinto forro del pantalón
            # Sin embargo, es necesario verificar el string que es parte de la sintaxis
            # Además, el comentario es uno de los parámetros del NodoRecibirEntrada
            tipo = self.componente_actual.tipo

            if tipo == TipoComponente.BOOLEANO:
                comentario = self.__verificar_booleano()
                #pass

            if tipo == TipoComponente.NUMERO:
                comentario = self.__verificar_numero()
                #pass

            if tipo == TipoComponente.TEXTO:
                comentario = self.__verificar_texto()
                #pass

            self.__verificar(')')

        elif self.__verificar('sin_comentario'):
            pass

        else:
            """
            Aqui se deberia levantar una Excepcion de que no se esta respetando el string de la gramatica
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "recibir_entrada debe tener con_comentario un Booleano o Numero o Texto o un sin_comentario o bien seguido de un guardar_en ")
            return nodoError

        # Entra en juego Guardar_en
        self.__verificar('guardar_en') #Palabra reservada
        identificador_objetivo = self.__verificar_identificador()

        return NodoRecibirEntrada(comentario, identificador_objetivo)

    def __analizar_si(self):
        """
        Si ::= "si" Condicion "inicio_si" Instruccion+ "final_si" ("\n" sino)?
        
        Sino ::= "sino" Instruccion+ "final_sino"
        """
        
        # Se empieza el análisis del Si
        self.__verificar('si') #Palabra reservada
        condicion = self.__analizar_condicion()
        self.__verificar('inicio_si') #Palabra reservada
        instrucciones = self.__analizar_instrucciones()
        self.__verificar('final_si') #Palabra reservada
        self.__verificar('\n') #Palabra reservada

        # Aqui entra en juego el sino

        #De la siguiente manera se implementan los "0 o 1 repetición" (?):

        if self.componente_actual.texto == 'sino':
            instrucciones_sino = self.__analizar_instrucciones()
            sino = NodoSino(instrucciones_sino)
        # no entrar en el if representa las 0 repeticiones

        return NodoSi(condicion, instrucciones, sino) # Preguntar por qué el sino no es opcional

    def __analizar_mientras(self):
        """
        Mientras ::= "mientras" Condición "inicia_mientras" Instruccion+ "final_mientras"
        """
        
        # Se empieza el análisis del mientras
        self.__verificar('mientras') #Palabra reservada
        condicion = self.__analizar_condicion()
        self.__verificar('inicia_mientras') #Palabra reservada
        instrucciones = self.__analizar_instrucciones()
        self.__verificar('final_mientras') #Palabra reservada

        return NodoMientras(condicion, instrucciones)

    def __analizar_Desde(self):
        """
        Desde ::= "desde" Numero "hasta" Numero "inicia_desde" Instruccion+ "final_desde"
        """
        self.__verificar('desde')
        iniciorango = self.__verificar_numero()
        self.__verificar('hasta')
        finalrango = self.__verificar_numero()
        self.__verificar('inicia_desde')

        instrucciones = self.__analizar_instrucciones()
        self.__verificar('final_desde')

        return NodoDesde(iniciorango, finalrango, instrucciones)

    def __analizar_condicion(self):
        """
            Instruccion ::= (Declaracion | Expresion | Operandos | Devuelve)
            Comentario no se lee ya que es excluido desde el explorador. 
            AccesoDatosComplejos tambien se excluyó
        """
        nodos_nuevos = []
        while(True):

            if self.componente_actual.tipo == TipoComponente.TIPO:
                nodos_nuevos += [self.__analizar_declaracion()]

            elif self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
                nodos_nuevos += [self.__analizar_expresion()]

            elif self.componente_actual.texto in ['escribir','recibir_entrada','si','mientras','desde','dormir','valor_absoluto']:
                nodos_nuevos += [self.__analizar_operando()]

            elif self.componente_actual.texto == 'devuelve':
                nodos_nuevos += [self.__analizar_devuelve()] #pendiente

            else:                
                break
        
        if nodos_nuevos == []:
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "La instruccion no es valida en este bloque de intruccion, solo Declaracion | Expresion | Operandos | Devuelve ")
            return nodoError
        return nodos_nuevos    

    def __analizar_instrucciones(self):
        """
            Instruccion ::= (Declaracion | Expresion | Operandos | Devuelve)
            Comentario no se lee ya que es excluido desde el explorador. 
            AccesoDatosComplejos tambien se excluyó
        """
        nodos_nuevos = []
        while(True):

            if self.componente_actual.tipo == TipoComponente.TIPO:
                nodos_nuevos += [self.__analizar_declaracion()]

            elif self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
                nodos_nuevos += [self.__analizar_expresion()]

            elif self.componente_actual.texto in ['escribir','recibir_entrada','si','mientras','desde','dormir','valor_absoluto']:
                nodos_nuevos += [self.__analizar_operando()]

            elif self.componente_actual.texto == 'devuelve':
                nodos_nuevos += [self.__analizar_devuelve()] #pendiente

            else:                
                break
        
        if nodos_nuevos == []:
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "La instruccion no es valida en este bloque de intruccion, solo Declaracion | Expresion | Operandos | Devuelve ")
            return nodoError
        return nodos_nuevos

    def __analizar_devuelve(self):
        """
        Devuelve ::= "devuelve" (Valor)
        """
        
        self.__verificar('devuelve')
        self.__verificar('(')
        valor = self.__analizar_valor()
        self.__verificar(')')

        nodo = NodoDevuelve(valor)
        return nodo

    def __analizar_declaracion(self):
        """
            DeclaracionComun ::= Tipo Expresion "\n"
        """
        tipo = self.componente_actual.texto
        expresion = self.__analizar_expresion()
        return NodoDeclaracionComun(tipo,expresion)


    def __analizar_Dormir(self):
        """
        Dormir ::= "dormir" Numero
        """
        self.__verificar('desde')
        tiempo = self.__verificar_numero()

        return NodoDormir(tiempo)


    def __analizar_ValorAbsoluto(self):
        """
        ValorAbsoluto ::= "valor_absoluto" Numero
        """
        self.__verificar('valor_absoluto')
        numero = self.__verificar_numero()

        return NodoValorAbsoluto(numero)

    def __verificar_numero(self):
        """
        Numero ::= (-)?\d+
        """
        if self.componente_actual.tipo != TipoComponente.NUMERO:
            """
            Error Sintáctico
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "Debe ser un valor numerico")
            return nodoError

        nodo = NodoNumero(self.componente_actual.texto)

        self.__siguiente_componente()

        return nodo

    def __verificar_flotante(self):
        """
        Numero ::=  (-)?([0-9]*[,])[0-9]+
        """
        if self.componente_actual.tipo != TipoComponente.FLOTANTE:
            """
            Error Sintáctico
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "Debe ser un valor flotante")
            return nodoError

        nodo = NodoFlotante(self.componente_actual.texto)

        self.__siguiente_componente()

        return nodo

    def __verificar_texto(self):
        """
        Texto ::= ^(\").+(\")$
        """
        if self.componente_actual.tipo != TipoComponente.TEXTO:
            """
            Error Sintáctico
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "Debe ser un valor de tipo texto")
            return nodoError

        nodo = NodoTexto(self.componente_actual.texto)

        self.__siguiente_componente()

        return nodo

    def __verificar_booleano(self):
        """
        Booleano ::= ("verdadero" | "falso")
        """
        if self.componente_actual.tipo != TipoComponente.BOOLEANO:
            """
            Error Sintáctico
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "Debe ser un valor booleano")
            return nodoError

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
            Error Sintáctico
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "Hace falta un identificador")
            return nodoError

        nodo = NodoIdentificador(self.componente_actual.texto)

        self.__siguiente_componente()
        
        return nodo

    def __verificar(self, texto):
        """
        Verifica que el componente actual sea el texto esperado
        """
        if self.componente_actual != texto:
            """
            Error Sintáctico
            """
            nodoError = NodoError("Error con el componente "+self.componente_actual.texto,
            self.componente_actual.fila, self.componente_actual.columna,
            "El componente "+texto+" no es reconocido.")
            return nodoError

        self.__siguiente_componente()

    def __siguiente_componente(self):
        """
        Avanza al siguiente componente léxico
        """
        self.posicion_componente_actual += 1

        if self.posicion_componente_actual >= self.cantidad_componentes:
            return

        self.componente_actual = self.componentes_léxicos[self.posición_componente_actual]

