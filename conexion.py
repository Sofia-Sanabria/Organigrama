#Este archivo va a hacer ejecutado solamente una vez para crear la base de datos y la tabla de la entidad 'organigrama', 
#así que ve en la parte final del código para ver como generar lo mencionado anteriormente.
import sqlite3 as sql
import re
def creardb():
    conn = sql.connect("datos.db")
    conn.commit()
    conn.close()

def tabla_organigrama():
    conn = sql.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE organigrama (
            COD text,
            ORG text,
            FEC text
        ) """
    )
    conn.commit() #Realizar los cambios
    conn.close()

"""UNA MANERA DE VERIFICAR E INSERTAR DATOS DEL ORGANIGRAMA EN LA BASE"""
def insertar_datos_organigrama(COD, ORG, FEC):
    conn = sql.connect("datos.db")
    cursor = conn.cursor()
    if len(COD) == 5 and len(ORG) <= 20 and len(FEC) == 10:
        numeros = FEC.split("/")
        dia = int(numeros[0])
        mes = int(numeros[1])
        anio = int(numeros[2])

        if anio < 1:
            return False

        # Verificar el rango del mes
        if mes < 1 or mes > 12:
            return False

        # Verificar el rango del día
        if dia < 1 or dia > 31:
            return False

        # Verificar meses con menos de 31 días
        meses_30_dias = [4, 6, 9, 11]
        if mes in meses_30_dias and dia > 30:
            return False

        # Verificar febrero
        if mes == 2:
            # Verificar si es bisiesto
            if (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0:
                if dia > 29:
                    return False
            else:
                if dia > 28:
                    return False

        # Si todas las verificaciones pasan, la fecha es válida
        instruccion = "INSERT INTO organigrama VALUES (?, ?, ?)"
        cursor.execute(instruccion, (COD, ORG, FEC))
        conn.commit()  # Realizar los cambios
        conn.close()

#Creamos la tabla para la entidad dependencia
def tabla_dependencia():
    conn = sql.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE dependencia (
            COD text,
            NOM text,
            CODRES text,
            NOM_ORG text,
            NOM_PAD text
        ) """
    )
    conn.commit() #Realizar los cambios
    conn.close()


"""UNA MANERA DE VERIFICAR E INSERTAR DATOS DE LA DEPENDENCIA EN LA BASE"""
def insertar_datos_dependencia(COD, NOM, CODRES, NOM_ORG, NOM_PAD):
    conn = sql.connect("datos.db")
    cursor = conn.cursor()
    if len(COD) <= 3 and len(NOM) <= 25 and len(CODRES) <= 4:
        # Si todas las verificaciones pasan, los datos son válidas
        instruccion = "INSERT INTO dependencia VALUES (?, ?, ?, ?, ?)"
        cursor.execute(instruccion, (COD, NOM, CODRES, NOM_ORG, NOM_PAD))
        conn.commit()
        conn.close()


#Creamos la tabla para la entidad persona
def tabla_persona():
    conn = sql.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE persona (
            COD text,
            DOC text,
            APE text,
            NOM text,
            TEL text, 
            DIR text,
            DEP text,
            SAL integer
        ) """
    )
    conn.commit() #Realizar los cambios
    conn.close()

"""UNA MANERA DE VERIFICAR E INSERTAR DATOS DE LA PERSONA EN LA BASE"""
def insertar_datos_persona(COD, DOC, APE, NOM, TEL, DIR, DEP, SAL):
    conn = sql.connect("datos.db")
    cursor = conn.cursor()
    datoscadenas = [APE, NOM]
    datosnumericos = [TEL, SAL]
    if len(COD) <= 4 and len(DOC) <= 15 and len(APE) <= 15 and len(NOM) <= 15 and len(TEL) <= 12 and len(DIR) <= 30 and len(DEP) <= 3 and len(SAL) <= 9:

        # Verificar si no se duplica el documento de identidad
        cursor.execute("SELECT DOC FROM persona WHERE DOC = ?", (DOC,))
        resultados = cursor.fetchall()
        # Iterar sobre los resultados
        if DOC in resultados:
            return False

        #Verificar si el apellido y nombre contiene solamente letras
        patronletras = r'^[a-zA-Z]+$'
        for dato in datoscadenas:
            coincidencia = re.match(patronletras, dato)
            if coincidencia is None:
                return False

        #Verificar que el campo teléfonico y salario solo contenga números
        patronnumeros = r'^[0-9]+$'
        for dato in datosnumericos:
            coincidencia = re.match(patronnumeros, dato)
            if coincidencia is None:
                return False

        # Si todas las verificaciones pasan, los datos son válidas
        instruccion = "INSERT INTO persona VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(instruccion, (COD, DOC, APE, NOM, TEL, DIR, DEP, SAL))
        conn.commit()
        conn.close()

"""deben descomentar las funciones """
if __name__ == "__main__":
    creardb()
    tabla_organigrama()
    tabla_dependencia()
    tabla_persona()

