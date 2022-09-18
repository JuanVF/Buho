# Explorador para el lenguaje Buho
from enum import Enum, auto

import re

class Explorador:
    # TODO: Agregar los componentes
    # NOTA: En lo de G Docs falta el de Tipo
    descriptores_componentes = [ ]


    def procesar_linea(self, linea):
        componentes = []

        while linea != "":
            for tipo, patron in self.descriptores_componentes:
                coincidencia = re.search(patron, linea)

                if coincidencia is None:
                    continue

                if not self.es_ignorable(tipo):
                    nuevo_componente = ComponenteLéxico(tipo, coincidencia.group())

                    componentes.append(nuevo_componente)

                linea = linea[coincidencia.end():]

        return componentes

    def es_ignorable(self, tipo_componente):
        return tipo_componente is TipoComponente.BLANCOS or tipo_componente is TipoComponente.COMENTARIO
            
exp = Explorador();
sentence = "funcion bubblesort recibe lista elements inicio_funcion"
componentes = exp.procesar_linea(sentence)

print("Test con: ")
print("\"", sentence, "\"")
print("Resultado Final:")
for (i, componente) in enumerate(componentes):
    print(f'{i:2} {componente}')