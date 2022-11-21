# Implementa el veficador de ciruelas
from analizador.analizador import invocar_analizador_para_verificador
from utils.arbolito import NodoDeclaracionComun, NodoDesde, NodoDevuelve, NodoDormir, NodoError, NodoExpresion, \
    NodoIdentificador, NodoOperacion, NodoNumero, NodoFlotante, NodoTexto, NodoAleatorio, NodoBooleano, NodoEscribir, \
    NodoRecibirEntrada, NodoSi, NodoSino, NodoMientras, NodoValorAbsoluto, Arbol, NodoFuncion, NodoParametro, \
    NodoOperacionAritmetica, NodoOperacionLogica, NodoPrograma, NodoLlamada, NodoCondicion, NodoOperando, \
    TipoNodo, NodoValor, NodoArbol
from utils.tipoDatos import TipoDatos
from utils.operandosLogicos import OperandosLogicos
from utils.operandosAritmeticos import OperandosAritmeticos


class TablaSímbolos:
    """
    Almacena información auxiliar para decorar el árbol de sintáxis
    abstracta con información de tipo y alcance.

    La estructura de símbolos es una lista de diccionarios
    """
    símbolos : list = []
    profundidad: int = 0

    def abrir_bloque(self):
        """
        Inicia un bloque de alcance (scope)
        """
        self.profundidad += 1

    def cerrar_bloque(self):
        """
        Termina un bloque de alcance y al acerlo elimina todos los
        registros de la tabla que estan en ese bloque
        """

        for registro in self.símbolos:
            if registro['profundidad'] == self.profundidad:
                self.símbolos.remove(registro)

        self.profundidad -= 1

    def nuevo_registro(self, nodo, nombre_registro=''):
        """
        Introduce un nuevo registro a la tabla de símbolos
        """
        # El nombre del identificador + el nivel de profundidad

        """
        Los atributos son: nombre, profundidad, referencia

        referencia es una referencia al nodo dentro del árbol
        (Técnicamente todo lo 'modificable (mutable)' en python es una
        referencia siempre y cuando use la POO... meh... más o menos.
        """

        diccionario = {}

        diccionario['nombre'] = nombre_registro
        diccionario['profundidad'] = self.profundidad
        diccionario['referencia'] = nodo

        self.símbolos.append(diccionario)

    def obtener_tipo(self, nombre):
        """
        Obtiene el tipo de un identificador
        """
        registro = self.verificar_existencia(nombre)

        if registro['referencia'].tipoNodo != TipoNodo.FUNCION:
            return registro['referencia'].tipo
        else:
            return "UNKNOWN"

    def verificar_existencia(self, nombre):
        """
        Verficia si un identificador existe cómo variable/función global o local
        """
        for registro in self.símbolos:

            # si es local
            if registro['nombre'] == nombre and \
                    registro['profundidad'] <= self.profundidad:
                return registro

        raise Exception('Esa vara no existe', nombre)

    def existe_registro(self, nombre):
        """
        Verifica si un identificador existe cómo variable/función global o local
        """
        for registro in self.símbolos:

            # si es local
            if registro['nombre'] == nombre and \
                    registro['profundidad'] <= self.profundidad:
                return True

        return False

    def __str__(self):
        resultado = 'TABLA DE SÍMBOLOS\n\n'
        resultado += 'Profundidad: ' + str(self.profundidad) + '\n\n'
        for registro in self.símbolos:
            resultado += str(registro) + '\n'

        return resultado


class Visitante:
    tabla_símbolos: TablaSímbolos

    def __init__(self, nueva_tabla_símbolos):
        self.tabla_símbolos = nueva_tabla_símbolos

    def visitar(self, nodo: NodoArbol):
        """
        Decide qué método usar para visitar un nodo
        """
        if nodo.tipoNodo is TipoNodo.PROGRAMA:
            self.visitar_programa(nodo)
        elif nodo.tipoNodo is TipoNodo.DECLARACION_COMUN:
            self.visitar_declaracion_comun(nodo)
        elif nodo.tipoNodo is TipoNodo.EXPRESION:
            self.visitar_expresion(nodo)
        elif nodo.tipoNodo is TipoNodo.OPERACION_ARITMETICA or \
                nodo.tipoNodo is TipoNodo.OPERACION_LOGICA:
            self.visitar_operacion(nodo)
        elif nodo.tipoNodo is TipoNodo.VALOR:
            self.visitar_valor(nodo)
        elif nodo.tipoNodo is TipoNodo.OPERANDO:
            self.visitar_operando(nodo)
        elif nodo.tipoNodo is TipoNodo.RECIBIR_ENTRADA:
            self.visitar_recibir_entrada(nodo)
        elif nodo.tipoNodo is TipoNodo.SI:
            self.visitar_si(nodo)
        elif nodo.tipoNodo is TipoNodo.SINO:
            self.visitar_sino(nodo)
        elif nodo.tipoNodo is TipoNodo.MIENTRAS:
            self.visitar_mientras(nodo)
        elif nodo.tipoNodo is TipoNodo.DESDE:
            self.visitar_desde(nodo)
        elif nodo.tipoNodo is TipoNodo.FUNCION:
            self.visitar_funcion(nodo)
        elif nodo.tipoNodo is TipoNodo.LLAMADA:
            self.visitar_llamada(nodo)
        elif nodo.tipoNodo is TipoNodo.PARAMETRO:
            self.visitar_parametro(nodo)

    def visitar_llamada(self, nodo : NodoLlamada):
        """
        Llamada ::= "llamar" Identificador ("recibe" Parametro+)?
        """
        # Verificar que la función exista
        registro = self.tabla_símbolos.verificar_existencia(nodo.nombre)

        ref : NodoFuncion = registro['referencia']

        # Verificar que el número de parámetros sea el correcto
        if len(nodo.params) != len(ref.parametros):
            raise Exception('Número de parámetros incorrecto')

    def visitar_desde(self, nodo : NodoDesde):
        """
        Desde ::= "desde" Numero "hasta" Numero "inicia_desde" Instruccion+ "final_desde"
        """
        for n in nodo.instrucciones:
            self.visitar(n)

    def visitar_mientras(self, nodo : NodoMientras):
        """
        Mientras ::= "mientras" Condición "inicia_mientras" Instruccion+ "final_mientras"
        """
        for n in nodo.instrucciones:
            self.visitar(n)

    def visitar_recibir_entrada(self, nodo: NodoRecibirEntrada):
        """
        Recibir_entrada ::= "recibir_entrada" ("con_comentario" (Booleano | Numero| Texto) | "sin_comentario" ) Guardar_en
        Guardar_en ::= "guardar_en" Identificador
        """

        comentario = nodo.comentario
        iden = nodo.identificadorObjetivo

        if comentario is not None and iden is not None:
            self.visitar_valor(comentario)
            self.visitar_identificador(iden)

            dec : NodoDeclaracionComun = self.tabla_símbolos.verificar_existencia(iden.identificador)

            if dec.tipo != comentario.tipo:
                raise Exception('El tipo de dato no coincide con el tipo de dato del identificador')

    def visitar_si(self, nodo: NodoSi):
        """
        Si ::= "si" Condicion "inicio_si" Instruccion+ "final_si" (Sino)?
        """
        for n in nodo.instrucciones:
            self.visitar(n)
        
        if nodo.sino is not None:
            self.visitar_sino(nodo.sino)

    def visitar_sino(self, nodo : NodoSino):
        """
        Sino ::= "sino" Instruccion+ "final_sino"
        """
        for n in nodo.instrucciones:
            self.visitar(n)

    def visitar_operando(self, nodo_actual : NodoOperando):
        """
        Programa::= (Declaracion | Expresion | Operandos | Funcion)*
        """
        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

    def visitar_programa(self, nodo_actual : NodoPrograma):
        """
        Programa::= (Declaracion | Expresion | Operandos | Funcion)*
        """
        for nodo in nodo_actual.nodos:
            self.visitar(nodo)

    def visitar_declaracion_comun(self, nodo_actual : NodoDeclaracionComun):
        """
        DeclaracionComun ::= Tipo Expresion
        """
        expresion = nodo_actual.expresion

        self.tabla_símbolos.nuevo_registro(nodo_actual, expresion.identificador.identificador)

        self.visitar_expresion(expresion)

        if self.tabla_símbolos.existe_registro(expresion.identificador):
            raise Exception('[Buho]: La variable ya existe: ', expresion.identificador)

    def visitar_expresion(self, nodo_actual : NodoExpresion):
        """
        Expresion ::= Identificador "tiene" Operacion
        """

        # Verificamos que el identificador exista
        self.visitar_identificador(nodo_actual.identificador)

        # Verificamos que la operacion entre datos sea correcta
        self.visitar_operacion(nodo_actual.operacion)

        # Verificamos que el tipo de dato de la operacion
        # sea el mismo que el tipo de dato del identificador
        nombre_identificador = nodo_actual.identificador.identificador

        nodo_iden : NodoParametro | NodoIdentificador = self.tabla_símbolos.verificar_existencia(nombre_identificador)['referencia']
        nodo_ope : NodoOperacionAritmetica | NodoOperacionLogica = nodo_actual.operacion
        
        tipo_primer = nodo_ope.operado.tipo

        if tipo_primer == TipoDatos.IDENTIFICADOR:
            var = nodo_ope.operado.valor.identificador
            tipo_primer = self.tabla_símbolos.obtener_tipo(var)

        if (tipo_primer == TipoDatos.LLAMADA):
            var = nodo_ope.operado.valor.identificador.identificador
            tipo_primer = self.tabla_símbolos.obtener_tipo(var)

            # No sabemos el tipo de dato que regresa la función
            # por la propia gramatica del lenguaje, asumiremos
            # que funciona correctamente
            if tipo_primer == "UNKNOWN":
                return

        # La variable se esta declarando en este punto
        # por lo que no se puede verificar el tipo de dato
        if nodo_iden.tipoNodo == TipoNodo.IDENTIFICADOR \
            and not self.tabla_símbolos.existe_registro(nombre_identificador):
            return

        if nodo_iden.tipo != tipo_primer:
            raise Exception("El tipo de dato de la operacion no es el mismo que el tipo de dato del identificador")

    def visitar_operacion(self, nodo_actual : NodoOperacionAritmetica | NodoOperacionLogica):
        """
        Operacion ::= Valor ( (OperadoresAritmeticos | OperadoresLogicos) Valor ) ?
        """
        primer_valor = nodo_actual.operado
        segundo_valor = nodo_actual.operando
        operacion = nodo_actual.operador

        self.visitar_valor(primer_valor)

        if segundo_valor is not None:
            self.visitar_valor(segundo_valor)

            tipo_primer = primer_valor.tipo
            tipo_segundo = segundo_valor.tipo

            if tipo_primer == TipoDatos.IDENTIFICADOR:
                tipo_primer = self.tabla_símbolos.obtener_tipo(primer_valor.valor.identificador)

            if tipo_segundo == TipoDatos.IDENTIFICADOR:
                tipo_segundo = self.tabla_símbolos.obtener_tipo(segundo_valor.valor.identificador)

            if tipo_primer != tipo_segundo:
                raise Exception("El tipo de dato de los dos valores no es el mismo")

            es_numerico : bool = primer_valor.tipo == TipoDatos.NUMERO or primer_valor.tipo == TipoDatos.FLOTANTE
            es_booleano : bool = primer_valor.tipo == TipoDatos.BOOLEANO
            es_texto : bool = primer_valor.tipo == TipoDatos.TEXTO

            es_numerico : bool = primer_valor.tipo == TipoDatos.NUMERO or primer_valor.tipo == TipoDatos.FLOTANTE
            es_booleano : bool = primer_valor.tipo == TipoDatos.BOOLEANO
            es_texto : bool = primer_valor.tipo == TipoDatos.TEXTO

            if es_booleano and operacion.tipoNodo == TipoNodo.OPERACION_ARITMETICA:
                raise Exception("No se puede realizar una operacion aritmetica con valores booleanos")

            if es_numerico and operacion.tipoNodo == TipoNodo.OPERACION_LOGICA:
                raise Exception("No se puede realizar una operacion logica con valores numericos")

            if es_texto and operacion.tipoNodo == TipoNodo.OPERACION_LOGICA:
                raise Exception("No se puede realizar una operacion logica con valores de texto")

            if es_texto and operacion.tipoNodo == TipoNodo.OPERACION_ARITMETICA:
                raise Exception("No se puede realizar una operacion aritmetica con valores de texto")     

    def visitar_valor(self, nodo_actual : NodoArbol):
        """
        Valor ::= (Identificador | Numero | Flotante | Texto | Booleano | Aleatorio)
        """
        
        # Verificamos en caso de que sea un identificador
        tipos = {
            TipoNodo.NUMERO : False,
            TipoNodo.FLOTANTE : False,
            TipoNodo.TEXTO : False,
            TipoNodo.BOOLEANO : False
        }

        # Verificamos que el identificador exista
        es_identificador = nodo_actual.valor.tipoNodo not in tipos

        if es_identificador:
            if nodo_actual.valor.tipoNodo == TipoNodo.IDENTIFICADOR:
                iden : NodoIdentificador = nodo_actual.valor

                self.tabla_símbolos.verificar_existencia(iden.identificador)
            if nodo_actual.valor.tipoNodo == TipoNodo.LLAMADA:
                iden : NodoLlamada = nodo_actual.valor

                self.tabla_símbolos.verificar_existencia(iden.identificador.identificador)

    def visitar_funcion(self, nodo_actual : NodoFuncion):
        """
        Funcion ::= "funcion" Identificador Parametros? "inicio_funcion" (Instruccion+)? Devuelve "final_funcion"
        """

        # Meto la función en la tabla de símbolos (IDENTIFICACIÓN)
        nombre_func = nodo_actual.identificador.identificador
        self.tabla_símbolos.nuevo_registro(nodo_actual, nombre_func)

        self.tabla_símbolos.abrir_bloque()

        for parametro in nodo_actual.parametros:
            self.visitar(parametro)

        for nodo in nodo_actual.instrucciones:
            self.visitar(nodo)

        self.tabla_símbolos.cerrar_bloque()

    def visitar_parametro(self, nodo_actual : NodoParametro):
        """
        Parametro ::= Tipo Identificador
        """
            
        # Meto el parámetro en la tabla de símbolos (IDENTIFICACIÓN)
        self.tabla_símbolos.nuevo_registro(nodo_actual, nodo_actual.identificador.identificador)

    def visitar_identificador(self, nodo_actual : NodoIdentificador):
        """
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        self.tabla_símbolos.verificar_existencia(nodo_actual.identificador)


class Verificador:
    asa: Arbol
    visitador: Visitante
    tabla_símbolos: TablaSímbolos

    def __init__(self, nuevo_asa: Arbol):
        self.asa = nuevo_asa

        self.tabla_símbolos = TablaSímbolos()

        self.visitador = Visitante(self.tabla_símbolos)

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """

        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()

    def verificar(self):
        self.visitador.visitar(self.asa.raiz)

def invocar_verificador(contenido_archivo):
    asa = invocar_analizador_para_verificador(contenido_archivo)

    verificador = Verificador(asa)
    verificador.verificar()

    verificador.imprimir_asa()

def invocar_verificador_para_generador(contenido_archivo):
    asa = invocar_analizador_para_verificador(contenido_archivo)

    verificador = Verificador(asa)
    verificador.verificar()

    return verificador.asa
