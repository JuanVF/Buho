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
