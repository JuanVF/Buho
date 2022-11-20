# Implementa el generador de buho

from utils.arbolito import Arbol, NodoArbol
from generador.visitadores import VisitantePython
from verificador.verificador import invocar_verificador_para_generador
from analizador.analizador import invocar_analizador_para_verificador


class Generador:
    asa: Arbol
    visitador: VisitantePython

    ambiente_estandar = """import sys
import random
import time

def escribir(valor):
\tprint(str(valor))

def recibirEntrada(comentario):
\tval = input(comentario)
\treturn val

def aleatorio(x, y):
\treturn random.randint(x, y)

def dormir(t):
\ttime.sleep(t)

def valorAbsoluto(x):
\treturn abs(x)
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
        resultado = self.asa.raiz.visitar(self.visitador)
        return resultado

    def generar_archivo(self, resultado, originalPath):
        path = originalPath.replace('.bh', '.py')
        f = open(path, "a")
        f.write(self.ambiente_estandar + '\n' + resultado)
        f.close()

def invocar_generador(contenido_archivo):
    asa = invocar_verificador_para_generador(contenido_archivo)
    #asa = invocar_analizador_para_verificador(contenido_archivo)

    generador = Generador(asa)
    resultado = generador.generar()
    print(generador.ambiente_estandar)
    print(resultado)

def invocar_generador_archivo(contenido_archivo, originalPath):
    #asa = invocar_verificador_para_generador(contenido_archivo)
    asa = invocar_analizador_para_verificador(contenido_archivo)

    generador = Generador(asa)
    resultado = generador.generar()
    generador.generar_archivo(resultado, originalPath)
