from logger import bcolors
# define Python user-defined exceptions
class BuhoError(Exception):
    linea : str
    columna : str
    tipoError : str
    error : str
    recomendacion : str

    def __int__(self, linea, columna, error, recomendacion, tipoError):
        self.linea = linea
        self.columna = columna
        self.tipoError = tipoError
        self.error = error
        self.recomendacion = recomendacion

    def __str__(self):
        msj = self.tipoError + f"""
                ******************************************** {bcolors.FAIL}Error encontrado{bcolors.ENDC} ****************************************************** 
                {bcolors.WARNING}\tUbicado en : """ + ("linea: " + self.linea) + (", columna: " + self.columna) + (", " + self.error) + """\n\t\t...""" + " posee un error" + "..." + f"""{bcolors.ENDC}        
                ********************************************************************************************************************
                """
        return msj

    def getRecomendacion(self):
        return self.recomendacion

#==============================================ERRORES SINTACTICOS=========================================
class BuhoErrorSintactico(BuhoError):
    def __int__(self, linea, columna, error, recomendacion, tipoError = "Error sintáctico detectado en: "):
        super().__int__(linea, columna, tipoError, error, recomendacion)

    def __str__(self):
        msj = self.tipoError + f"""
                ******************************************** {bcolors.FAIL}Error encontrado{bcolors.ENDC} ****************************************************** 
                {bcolors.WARNING}\tUbicado en : """ + ("linea: " + self.linea) + (", columna: " + self.columna) + (", " + self.error) + """\n\t\t...""" + " mientras se analizaba" + "..." + f"""{bcolors.ENDC}        
                ********************************************************************************************************************
                """
        return msj

class BuhoErrorComponenteFaltante(BuhoErrorSintactico):
    def __int__(self, linea, columna, componenteFaltante, recomendacion, tipoError = "Error sintáctico detectado en: "):
        super().__int__(linea, columna, ("falta el componente " + componenteFaltante), recomendacion)

class BuhoErrorFuncionNoDefinida(BuhoErrorSintactico):
    def __int__(self, linea, columna, componente, recomendacion, tipoError = "Error sintáctico detectado en: "):
        super().__int__(linea, columna, ("la funcion "+ componente + " no esta definida"), recomendacion)
