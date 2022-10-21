# Analizador para el lenguaje Buho

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from explorador.explorador import ComponenteLéxico, TipoComponente

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
        nodos_nuevos += [self.__analizar_identificador()]

        # Verificar que el componente actual sea "tiene"
        self.__verificar("tiene")


        # Verificar que el componente actual sea una operacion
        nodos_nuevos += [self.__analizar_operacion()]
        

    def __analizar_identificador(self):
        """
        Identificador ::= [a-z]([a-zA-z0-9])*
        """

        if self.componente_actual.tipo != TipoComponente.IDENTIFICADOR:
            """
            @Kaled Aqui se deberia levantar una Excepcion de que se esperaba un identificador
            """
            pass
        
        # TODO: Reemplazar esto por la creacion de un nodo de tipo identificador
        nodo = None
        
        return nodo

    def __analizar_operacion(self):
        """
        Operacion ::= Valor ( (OperadoresArtimeticos | OperadoresLogicos) Valor ) ?
        TODO: Implementar esta funcion
        """
        pass

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

