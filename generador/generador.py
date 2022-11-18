# Implementa el veficador de ciruelas

from utils.arbolito import Arbol, NodoArbol
from generador.visitadores import VisitantePython
from verificador.verificador import invocar_verificador_para_generador

class Generador:
    asa: Arbol
    visitador: VisitantePython

    ambiente_estandar = """import sys
import random
import time

def escribir(valor):
    print(str(valor))

def recibirEntrada(comentario):
    val = input(comentario)
    return val

def aleatorio(x, y):
    return random.randint(x, y)

def dormir(t):
    time.sleep(t)

def valorAbsoluto(x):
    return abs(x)
"""

    def __init__(self, nuevo_asa: Arbol):

        self.asa = nuevo_asa
        self.visitador = VisitantePython()

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """

        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()

    def generar(self):
        #resultado = self.visitador.visitar(self.asa.raiz)
        resultado = self.asa.raiz.visitar(self.visitador)
        print(self.ambiente_estandar)
        print(resultado)

def invocar_generador(contenido_archivo):
    asa = invocar_verificador_para_generador(contenido_archivo)

    generador = Generador(asa)
    generador.generar()
    #generador.imprimir_asa()
