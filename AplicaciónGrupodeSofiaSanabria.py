import matplotlib.pyplot as plt  # en esta línea importamos la librería matplotlib y la renombramos para mayor comodidad como plt
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conexion import *
import random
from collections import deque
# creamos variables globales, como contadores y auxiliares
k = 0

# creamos una paleta de colores de tkinter, de esta forma será más fácil configurar botones que tengan funciones estéticas, o estilizar widgets
lista_colores_tkinter = ["orange", "light salmon", "violet", "red", "purple", "black", "light salmon", "light salmon", "gold", "yellow",
                         "turquoise"]

# Clases generadas para cambiar la presentación de algunos widgets
class Boton_animado:
    def __init__(self, frame, width, height, posx, posy, text, columnspan, bg, fg, command, metodo_de_aparicion,
                 color_cambiar, tipo_letra, padx, pady, relief, anchor):
        self.boton = tk.Button(frame, width=width, height=height, text=text, bg=bg, fg=fg, command=command, bd=0,
                               relief=relief, activeforeground=fg, activebackground=bg,
                               font=tipo_letra, anchor=anchor, disabledforeground = "black") #colorear
                                                                                    #color de los botones animados
                                                                                    #desactivados
        self.frame = frame
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.text = text
        self.columnspan = columnspan
        self.bg = bg
        self.fg = fg
        self.command = command
        self.metodo_de_aparicion = metodo_de_aparicion
        self.color_cambiar = color_cambiar
        self.tipo_letra = tipo_letra
        self.padx = padx
        self.pady = pady
        self.relief = relief
        self.anchor = anchor

    def vincular_raton(self):
        def entrar_rango_boton(event):  # función que realiza una acción cuando pasamos el ratón por encima del botón
            self.boton.config(bg=self.color_cambiar)

        def salir_rango_boton(event):  # función que realiza una acción cuando salimos del rango del botón
            self.boton.config(bg=self.bg)

        self.boton.bind("<Enter>", entrar_rango_boton) #bind es un método de tkinter que liga acciones
                                                        # de los periféricos a funciones
        self.boton.bind("<Leave>", salir_rango_boton) #en estos casos tenemos la entrada(enter) del ratón al rango
                                                        #del widget en pantalla y su salida(leave) del mismo rango

    #métodos de impresión de los botones animados generados
    def place(self):
        self.boton.place(x=self.posx, y=self.posy)

    def grid(self):
        self.boton.grid(column=self.posx, row=self.posy, columnspan=self.columnspan, pady=self.pady)

    def pack(self):
        self.boton.pack()


# Funciones de la aplicación
# destruye el frame de login y deja la ventana para los frames del programa principal.
def logueado():
    global login, e_tiqueta_fondo_login
    #Destruye lo relacionado a la pestaña login
    e_tiqueta_fondo_login.destroy()
    login.destroy()
    ventana.config(bg="misty rose") #colorear
                    #color de la ventana principal después de loguearse

    menu.pack(side=tk.LEFT, fill=tk.Y)

#Funcion para preguntar si estas seguro de salir de la aplicacion
def Cerrar ():
    if messagebox.askyesno(title="Cerrar", message="Seguro que quieres salir de la aplicacion?"):
        ventana.destroy() ## Si apretas "Si" sale de la aplicacion, si apretas "No" no pasa nada

# frames para trabajar con las clases de personas, organigramas, dependencias y generar los informes
def cerrar_ventana(frame, boton): # función que cierra las pestanhas organigramas, personas, dependencias e informes
    #se usa .boton, porque lo que pasamos a la función es el nombre del boton animado que es un objeto de la
    #clase boton animado, donde sí declaramos un botón de tkinter con el nombre de boton
    global organigramas, personas, informes, dependencias
    if messagebox.askyesno(title="Cerrar", message="¿Desea cerrar la pestaña?, podría perder los cambios que no guardó"):
        if frame == "organigramas":
            organigramas.destroy()  ## Si apretas "Si" sale del frame, si apretas "No" no pasa nada
            boton.boton.config(activebackground="light salmon") #colorear
                                #color del botón después de cerrar una pestanha
            boton.boton.config(bg="light salmon") #colorear
                                #color del botón después de cerrar una pestanha
            boton.bg = "light salmon"    #colorear
                        #color del botón después de cerrar una pestanha
            organigramas = tk.LabelFrame(ventana, bg="misty rose", text="Organigramas", font="Arial 12")
            boton.boton["state"] = "normal" #activamos el botón de vuelta
        if frame == "personas":
            personas.destroy()  ## Si apretas "Si" sale del frame, si apretas "No" no pasa nada
            boton.boton.config(activebackground="light salmon") #colorear
                                #estos también deben ser iguales al anterior
            boton.boton.config(bg="light salmon") #colorear
            boton.bg = "light salmon" #colorear
            personas = tk.LabelFrame(ventana, bg="misty rose", text="Personas", font="Arial 12")
            boton.boton["state"] = "normal" #activamos el botón de vuelta
        if frame == "informes":
            informes.destroy()  # Si apretas "Si" sale del frame, si apretas "No" no pasa nada
            boton.boton.config(activebackground="light salmon") #colorear
            boton.boton.config(bg="light salmon") #colorear
            boton.bg = "light salmon" #colorear
            informes = tk.LabelFrame(ventana, bg="misty rose", text="Informes", font="Arial 12")
            boton.boton["state"] = "normal" # activamos el botón de vuelta

# cierra los formularios para crear, agregar y buscar dependencias, personas, y organigramas
def cerrar_formularios(frame, frame2, command):
    frame.destroy()
    frame2.destroy()
    command()

# cierra los formularios para crear, agregar y buscar dependencias, personas, y organigramas
def cerrar_formularios_copia(frame, command):
    frame.destroy()
    command()

# genera los espacios para guardar los datos en la base de datos
def generar_tablas_db():
    tabla_persona()
    tabla_organigrama()

""" Dentro de esta funcion estan todas las funciones de organigrama y dependencias """

def ventana_organigrama(): # despliega la pestanha de organigramas
    global boton_organigramas_menu, ventana, organigramas, lista_colores_tkinter, dependencias
    boton_organigramas_menu.bg = "salmon"
    boton_organigramas_menu.boton["state"] = "disabled"# desactivamos el boton de abrir esta ventana para
                                                        # que no genere problemas con los frames generados en el

    # Genera un codigo interno de 5 digitos para organigrama
    def generar_codigo_interno_organigrama():
        codigo_interno = random.randint(0, 99999)  # Genera un número aleatorio de 0 a 99999
        codigo_interno = str(codigo_interno).zfill(5)  # Ajusta el código a 5 dígitos rellenando con ceros a la izquierda si es necesario
        return codigo_interno

    def crear_organigrama():
        organigramasbotones.destroy()  # ocultamos el frame que contiene los botones principales de la pestaña organigramas
        barra_opciones_organigramas.destroy()

        def buscar_org(nom_ord):  # Para buscar un organigrama en especifico en la base de datos
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM organigrama WHERE ORG = ?""", (nom_ord,))
            datos = cursor.fetchone()
            conn.close()
            if datos == None:
                return False
            else:
                return True

        def guardar(): # Guarda un organigrama en la base de datos y agrega en la tabla
            conn = sql.connect("datos.db")
            # Lógica para guardar los datos
            ORG = entry_ORG.get()
            FEC = entry_FEC.get()

            COD = generar_codigo_interno_organigrama()

            if buscar_org(ORG):  # Este if pregunta si ya existe un organigrama con el mismo nombre
                messagebox.showwarning(message="El organigrama ya existe.")
                buscar()

            else:  # Si no existe se agrega
                if insertar_datos_organigrama(COD, ORG, FEC) != False:
                    tabla.insert("", tk.END, values=(ORG, FEC))
                    conn.commit()
                    conn.close()
                    entry_ORG.delete(0, tk.END)
                    entry_FEC.delete(0, tk.END)
                else:
                    messagebox.showwarning(title="❗Alerta Formato de Atributos❗", message="ORG)  Cadena, 20 caracteres\n\n"
                                                                                      + "FEC)  Formato Fecha: DD/MM/AAAA \n")
            conn.close()

        def eliminar(): #Elimina un organigrama de la base de datos y de la tabla
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            # Obtener el elemento seleccionado en la tabla
            seleccionado = tabla.focus()
            if seleccionado:
                ORG = tabla.set(seleccionado, "ORG")
                FEC = tabla.set(seleccionado, "FEC")

                messagebox.showwarning(title="❗Organigrama❗",
                                       message="Esta seguro de eliminar el organigrama y sus dependencias   \n")

                # Eliminar la fila seleccionada de la tabla
                tabla.delete(seleccionado)

                # Eliminar la fila correspondiente en la base de datos
                instruccion = "DELETE FROM organigrama WHERE ORG = ? AND FEC = ?"
                cursor.execute(instruccion, (ORG, FEC))
                conn.commit()

                # Eliminar las dependendencias del organigrama seleccionado
                instruccion = "DELETE FROM dependencia WHERE  NOM_ORG = ?"
                cursor.execute(instruccion, (ORG,))
                conn.commit()
            conn.close()

        def modificar(): #Modifica el nombre y la fecha de un organigrama seleccionando desde la tabla
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            seleccionado = tabla.focus()
            ORG_anterior = tabla.set(seleccionado, "ORG")
            if seleccionado:
                ORG = entry_ORG.get()
                FEC = entry_FEC.get()
                tabla.item(seleccionado, values=(ORG, FEC))
                entry_ORG.delete(0, tk.END)
                entry_FEC.delete(0, tk.END)

                cursor.execute("SELECT * FROM organigrama WHERE ORG = ? AND FEC = ?", (ORG, FEC, ))
                datos = cursor.fetchone()

                if datos:
                    instruccion = "UPDATE organigrama SET ORG = ?, FEC = ? WHERE COD = ?"
                    cursor.execute(instruccion, (ORG, FEC, datos[0]))
                    conn.commit()  # Realizar los cambios en organigramas

                    cursor.execute("UPDATE dependencia SET NOM_ORG = ? WHERE NOM_ORG = ?", (ORG, ORG_anterior, ))
                    conn.commit() # Realizar los cambios en dependencias
                    visualizar_datos()
            conn.close()

        def visualizar_datos(): # Para ver los atributos de todos los organigramas en la tabla
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            # Obtener los datos de la base de datos
            cursor.execute("SELECT * FROM organigrama")
            datos = cursor.fetchall()

            # Limpiar la tabla existente, si es necesario
            tabla.delete(*tabla.get_children())

            # Agregar los datos a la tabla
            for dato in datos:
                tabla.insert("", "end", values=(dato[1], dato[2]))

            conn.close()

        def buscar(): # Busca un organigrama y lo muestra en la tabla
            ORG = entry_ORG.get()
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            instruccion = "SELECT * FROM organigrama WHERE ORG = ?"
            cursor.execute(instruccion, (ORG,))
            datos = cursor.fetchall()
            # Limpiar la tabla existente, si es necesario
            tabla.delete(*tabla.get_children())

            # Agregar los datos a la tabla
            for dato in datos:
                tabla.insert("", "end", values=(dato[1], dato[2]))

            conn.close()

        """"Controles para crear organigrama"""

        # Crear un marco para los controles
        marco_controles = tk.Frame(organigramas, padx=10, pady=10)
        marco_controles.pack(side = tk.LEFT, fill= tk.BOTH, expand= True)

        # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a organigramas
        marco_formulario_organigrama = tk.Frame(marco_controles)
        marco_formulario_organigrama.pack(fill= tk.BOTH, expand= True)

        label_ORG = tk.Label(marco_formulario_organigrama, text="ORGANIGRAMA:")
        label_ORG.grid(row=1, column=0, sticky=tk.E)
        entry_ORG = tk.Entry(marco_formulario_organigrama)
        entry_ORG.grid(row=1, column=1, pady=10)

        label_FEC = tk.Label(marco_formulario_organigrama, text="FECHA:")
        label_FEC.grid(row=2, column=0, sticky=tk.E)
        entry_FEC = tk.Entry(marco_formulario_organigrama)
        entry_FEC.grid(row=2, column=1, pady=10)

        # Crear un marco para el recuadro de los botones
        marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
        marco_recuadro.pack(fill= tk.BOTH, expand=True)

        # Crear una etiqueta encima del recuadro de botones
        label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
        label_recuadro.pack(pady=5)

        # Crear un marco para los botones
        marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
        marco_botones.pack(padx=5, pady=5, fill= tk.Y, expand= True)

        # Crear los botones
        boton_guardar = ctk.CTkButton(marco_botones, text="Guardar", bg_color="lightgray", command=guardar)
        boton_guardar.grid(row=0, column=0, padx=5, pady=5)

        boton_modificar = ctk.CTkButton(marco_botones, text="Modificar", bg_color="lightgray", command=modificar)
        boton_modificar.grid(row=0, column=1, padx=5, pady=5)

        boton_eliminar = ctk.CTkButton(marco_botones, text="Eliminar", bg_color="lightgray", command=eliminar)
        boton_eliminar.grid(row=1, column=0, padx=5, pady=5)

        boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=buscar)
        boton_buscar.grid(row=1, column=1, padx=5, pady=5)

        boton_actualizar = ctk.CTkButton(marco_botones, text="Actualizar tabla", bg_color="lightgray", command=visualizar_datos)
        boton_actualizar.grid(row=2, column=0, padx=5, pady=5)

        # Crear la tabla organigrama
        tabla = ttk.Treeview(organigramas, columns=("ORG", "FEC"))
        tabla.column("#0", width=0, stretch=tk.NO)
        tabla.heading("ORG", text="ORGANIZACIÓN")
        tabla.heading("FEC", text="FECHA")
        tabla.pack(fill = tk.BOTH, expand= True)

        # boton que activa una función para eliminar los frames y botones para crear un organigrama
        boton_Volver_marcocontroles = ctk.CTkButton(marco_controles, text="Volver", bg_color="lightgray",
              command=lambda: cerrar_formularios(marco_controles, tabla, ventana_organigrama))
        boton_Volver_marcocontroles.pack(side=tk.BOTTOM)

    """Dentro de esta funcion estan las funciones de crear dependencias y copiar organigrama"""

    def abrir_organigrama():
        organigramasbotones.destroy()
        barra_opciones_organigramas.destroy()

        # Genera un codigo interno de 3 digitos para dependencias
        def generar_codigo_interno_dependencia():
            codigo_interno = random.randint(0, 999)
            codigo_interno = str(codigo_interno).zfill(3)
            return codigo_interno

        # Funcion para desplegar el formulario de dependencias
        def crear_dependencia():
            if variableDep_nombredelorganigrama == "":
                messagebox.showwarning(title="❗Seleccionar organigrama a editar❗", message= "Seleccione el organigrama del cual \n" + "va a crear la dependencia\n")

            else:
                # Destruir marcos de controles y tabla de organigramas para poder usar el de dependencias
                marco_controles.destroy()
                tabla.destroy()

                def buscar_dep(nom_dep): # Para buscar una dependencia en especifico en la base de datos
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Busca los datos en la base de datos
                    cursor.execute("SELECT * FROM dependencia WHERE NOM = ?", (nom_dep,))
                    datos = cursor.fetchone()
                    conn.close()
                    if datos == None:
                        return False
                    else:
                        return True

                def buscar_depORG(nom_org): #Para buscar una dependencia en cierto organigrama
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Busca los datos en la base de datos
                    cursor.execute("SELECT * FROM dependencia WHERE NOM_ORG = ?", (nom_org,))
                    datos = cursor.fetchone()
                    conn.close()
                    if datos == None:
                        return False
                    else:
                        return True



                def buscar_persona(NOM_PER): # Para buscar una persona en la base de datos
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Busca los datos en la base de datos
                    cursor.execute("SELECT * FROM persona WHERE NOM = ?", (NOM_PER,))
                    datos = cursor.fetchone()
                    conn.close()
                    if datos == None:
                        return False
                    else:
                        return True

                def cargar_codigo_persona(NOM_JEFE): # Funcion para cargar el codigo de una persona a la base de datos
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    cursor.execute("""SELECT COD FROM persona WHERE NOM = ?""", (NOM_JEFE,))
                    datos = cursor.fetchone()[0] # Posicion del codigo
                    return datos

                def guardar():
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()

                    # Lógica para guardar los datos
                    COD = generar_codigo_interno_dependencia()
                    NOM = entry_NOM.get()
                    NOM_JEFE = entry_JEFE.get()  # Se carga el nombre de la persona jefe
                    NOM_ORG = entry_NOM_ORG.get()

                    cursor.execute("""SELECT * FROM persona WHERE NOM = ?""", (NOM_JEFE,))
                    datos = cursor.fetchone()  # Posicion del codigo

                    if buscar_persona(NOM_JEFE):  # Para asignar personas como jefes de dependencia
                        # Eliminar la fila correspondiente en la base de datos
                        instruccion = "DELETE FROM persona WHERE COD = ? AND DOC = ? AND APE = ? AND NOM = ? AND TEL = ? AND DIR = ? AND DEP = ? AND SAL = ?"
                        cursor.execute(instruccion, (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7]))
                        conn.commit()

                        insertar_datos_persona(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], COD, str(datos[7]))

                        if buscar_depORG(NOM_ORG) == False:  # Si no se ha creado ninguna dependencia a cierto organigrama, se establece una dependencia raiz
                            NOM_PAD = None
                            CODRES = cargar_codigo_persona(NOM_JEFE)  # Variable para cargar el codigo de persona
                            if insertar_datos_dependencia(COD, NOM, CODRES, NOM_ORG, NOM_PAD) != False:
                                tabla_dependencia.insert("", tk.END, values=(NOM, NOM_JEFE, NOM_ORG, NOM_PAD))
                                entry_NOM.delete(0, tk.END)
                                entry_JEFE.delete(0, tk.END)
                                # Despues de guardar el entry de dependencia padre vuelve a la normalidad
                                entry_NOM_PAD["state"] = "normal"
                                entry_NOM_PAD.grid(row=4, column=1, pady=10)
                                conn.commit()
                                cursor.close()
                                conn.close()
                            else:
                                messagebox.showwarning(title="❗Alerta Formato de Atributos❗",
                                                       message="NOM)  Cadena, 25 caracteres\n"
                                                               + "CODRES)  Cadena, 4 digitos\n"
                                                               + "NOM_ORG)  Cadena, 20 caracteres\n")

                        else:  ## Si ya existe una dependencia o varias se le asigna un padre
                            NOM_PAD = entry_NOM_PAD.get()
                            if buscar_dep(NOM_PAD):# Si se encuentra la dependencia padre elegida por el usuario
                                CODRES = cargar_codigo_persona(NOM_JEFE)
                                if insertar_datos_dependencia(COD, NOM, CODRES, NOM_ORG, NOM_PAD) != False:
                                    tabla_dependencia.insert("", tk.END, values=(NOM, NOM_JEFE, NOM_ORG, NOM_PAD))
                                    entry_NOM.delete(0, tk.END)
                                    entry_JEFE.delete(0, tk.END)
                                    entry_NOM_PAD.delete(0, tk.END)
                                    conn.commit()
                                    conn.close()

                                else:
                                    messagebox.showwarning(title="❗Alerta Formato de Atributos❗",message="NOM)  Cadena, 25 caracteres\n"
                                                                                                        + "CODRES)  Cadena, 4 digitos\n"
                                                                                                        + "NOM_ORG)  Cadena, 20 caracteres\n"
                                                                                                        + "NOM_PAD)  Cadena, 20 caracteres\n")

                            else:  ## Si no se encuentra sale este mensaje
                                messagebox.showwarning(message="No se encontro la dependencia padre")

                    else:
                        messagebox.showwarning(title="❗Alerta Persona NO encontrada❗", message="Ingrese una persona Jefe")

                def extraer_nombre(COD_PER): # Funcion para traer el nombre de la persona segun su codigo
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    cursor.execute("""SELECT * FROM persona WHERE COD = ?""", (COD_PER,))
                    datos = cursor.fetchone()
                    conn.close()
                    if datos:
                        return datos[3]
                    else:
                        return ""

                def visualizar_datosdep(): #Muestra en la tabla todas la dependencias
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()

                    NOM_ORG = entry_NOM_ORG.get()

                    if buscar_depORG(NOM_ORG): #Pregunta si en tal organigrama hay dependencias

                        # Obtener los datos de la base de datos
                        instruccion = "SELECT * FROM dependencia WHERE NOM_ORG = ?"
                        cursor.execute(instruccion, (NOM_ORG,))
                        datosdep = cursor.fetchall()

                        # Limpiar la tabla existente, si es necesario
                        tabla_dependencia.delete(*tabla_dependencia.get_children())

                        # Agregar los datos a la tabla
                        for dato in datosdep:
                            tabla_dependencia.insert("", "end", values=(dato[1], extraer_nombre(dato[2]), dato[3], dato[4]))
                    else:
                        messagebox.showwarning(title="❗Organigrama sin Dependencias❗",
                                               message="Este organigrama no tiene ninguna dependencia\n"
                                                       + "Crea sus dependencias")

                        tabla_dependencia.delete(*tabla_dependencia.get_children())
                        #Si no hay dependencias creada se anula el entry de dependencia padre
                        entry_NOM_PAD["state"] = "readonly"
                        entry_NOM_PAD.grid(row=4, column=1, pady=10)

                    conn.close()
                    #Se activa el entry de organigrama para elegir con que organigrama trabajar
                    entry_NOM_ORG["state"] = "normal"
                    entry_NOM_ORG.grid(row=1, column=1, pady=10)

                def buscar(): #Busca una dependencia entre todas y muestra en la tabla
                    NOM = entry_NOM.get()
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Busca los datos en la base de datos
                    instruccion = "SELECT * FROM dependencia WHERE NOM = ?"
                    cursor.execute(instruccion, (NOM,))
                    datos = cursor.fetchall()
                    # Limpiar la tabla existente, si es necesario
                    tabla_dependencia.delete(*tabla_dependencia.get_children())

                    # Agregar los datos a la tabla
                    for dato in datos:
                        tabla_dependencia.insert("", "end", values=(dato[1], extraer_nombre(dato[2]), dato[3], dato[4]))

                    conn.close()

                def eliminar():  # Elimina una dependencia y sus sucesoras de la base de datos y de la tabla
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Obtener el elemento seleccionado en la tabla
                    seleccionado = tabla_dependencia.focus()
                    if seleccionado:
                        NOM = tabla_dependencia.set(seleccionado, "NOM")
                        CODRES = tabla_dependencia.set(seleccionado, "CODRES")
                        NOM_ORG = tabla_dependencia.set(seleccionado, "NOM_ORG")

                        # Eliminar la fila seleccionada de la tabla
                        tabla_dependencia.delete(seleccionado)

                        cursor.execute( "SELECT * FROM dependencia WHERE NOM = ?", (NOM, ))
                        datos = cursor.fetchone()

                        # Eliminar la fila correspondiente en la base de datos
                        instruccion = "DELETE FROM dependencia WHERE NOM = ? AND CODRES = ? AND NOM_ORG = ? "
                        cursor.execute(instruccion, (NOM, CODRES, NOM_ORG))
                        conn.commit()

                        # Eliminar los hijos de esa dependencia elegida
                        instruccion = "DELETE FROM dependencia WHERE NOM_PAD = ?  AND NOM_ORG = ? "
                        cursor.execute(instruccion, (NOM, NOM_ORG))
                        conn.commit()

                        if datos:
                            # Eliminar las personas que pertenecen a esa dependencia
                            instruccion = "DELETE FROM persona WHERE DEP = ?"
                            cursor.execute(instruccion, (datos[0],))
                            conn.commit()

                        visualizar_datosdep()
                    conn.close()

                """Controles para Crear Dependencias"""

                # Crear un marco para los controles
                marco_controles_dependencias = tk.Frame(organigramas, padx=10, pady=10)
                marco_controles_dependencias.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a dependencias
                marco_formulario_dependencia = tk.Frame(marco_controles_dependencias)
                marco_formulario_dependencia.pack(fill=tk.BOTH, expand=True)

                label_NOM_ORG = tk.Label(marco_formulario_dependencia, text="ORGANIZACIÓN SELECCIONADA:", anchor= "w")
                label_NOM_ORG.grid(row=1, column=0, sticky=tk.W)
                entry_NOM_ORG = tk.Entry(marco_formulario_dependencia)
                #CARGAMOS EN LA CAJA DE TEXTO EL NOMBRE DE LA ORGANIZACIÓN SELECCIONADA ANTERIORMENTE
                entry_NOM_ORG.insert(0, variableDep_nombredelorganigrama)
                entry_NOM_ORG["state"] = "readonly"
                entry_NOM_ORG.grid(row=1, column=1, pady=10)

                label_NOM = tk.Label(marco_formulario_dependencia, text="NOMBRE DE LA DEPENDENCIA:", anchor= "w")
                label_NOM.grid(row=2, column=0, sticky=tk.W)
                entry_NOM = tk.Entry(marco_formulario_dependencia)
                entry_NOM.grid(row=2, column=1, pady=10)

                label_JEFE = tk.Label(marco_formulario_dependencia, text="NOMBRE DE PERSONA JEFE:", anchor= "w")
                label_JEFE.grid(row=3, column=0, sticky=tk.W)
                entry_JEFE = tk.Entry(marco_formulario_dependencia)
                entry_JEFE.grid(row=3, column=1, pady=10)

                label_NOM_PAD = tk.Label(marco_formulario_dependencia, text="NOMBRE DE DEPENDENCIA JEFE:", anchor= "w")
                label_NOM_PAD.grid(row=4, column=0, sticky=tk.W)
                entry_NOM_PAD = tk.Entry(marco_formulario_dependencia)
                entry_NOM_PAD.grid(row=4, column=1, pady=10)

                # Crear un marco para el recuadro de los botones
                marco_recuadro = tk.Frame(marco_controles_dependencias, bd=1, relief=tk.RAISED, bg="lightgray")
                marco_recuadro.pack(fill=tk.BOTH, expand=True)

                # Crear una etiqueta encima del recuadro de botones
                label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
                label_recuadro.pack(pady=5)

                # Crear un marco para los botones
                marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
                marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

                # Crear los botones
                boton_guardar = ctk.CTkButton(marco_botones, text="Guardar", bg_color="lightgray", command=guardar)
                boton_guardar.grid(row=0, column=0, padx=5, pady=5)

                boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=buscar)
                boton_buscar.grid(row=0, column=1, padx=5, pady=5)

                boton_eliminar = ctk.CTkButton(marco_botones, text="Eliminar", bg_color="lightgray", command=eliminar)
                boton_eliminar.grid(row=2, column=1, padx=5, pady=5)

                boton_actualizar = ctk.CTkButton(marco_botones, text="Actualizar tabla", bg_color="lightgray", command=visualizar_datosdep)
                boton_actualizar.grid(row=2, column=0, padx=5, pady=5)

                # Crear la tabla de dependencias
                tabla_dependencia = ttk.Treeview(organigramas, columns=("NOM", "CODRES", "NOM_ORG", "NOM_PAD"))
                tabla_dependencia.column("#0", width=0, stretch=tk.NO)
                tabla_dependencia.heading("NOM", text="NOMBRE DEPENDENCIA")
                tabla_dependencia.heading("CODRES", text="PERSONA JEFE")
                tabla_dependencia.heading("NOM_ORG", text="ORGANIGRAMA")
                tabla_dependencia.heading("NOM_PAD", text="DEPENDENCIA PADRE")
                tabla_dependencia.pack()


                # boton que activa una función para eliminar los frames y botones para crear un organigrama
                boton_Volver_marcocontroles = ctk.CTkButton(marco_controles_dependencias, text="Volver", bg_color="lightgray",
                         command=lambda: cerrar_formularios(marco_controles_dependencias, tabla_dependencia, abrir_organigrama))
                boton_Volver_marcocontroles.pack(side=tk.BOTTOM)

        # Funcion para desplegar el formulario de copiar organigramas
        def copiar_organigrama():
            if variableCopia_nombredelorganigrama == "":
                messagebox.showwarning(title="❗Seleccionar organigrama a editar❗",
                                       message="Seleccione el organigrama del cual \n" + "va a crear una copia\n")
            else:
                ##Destruir marcos de controles y tabla de organigramas para poder usar el de dependencias
                marco_controles.destroy()
                tabla.destroy()

                def buscar_depORG(nom_org):  # Para buscar una dependencia en cierto organigrama
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Busca los datos en la base de datos
                    cursor.execute("SELECT * FROM dependencia WHERE NOM_ORG = ?", (nom_org,))
                    datos = cursor.fetchone()
                    conn.close()
                    if datos == None:
                        return False
                    else:
                        return True

                def guardar_copiaOrg(): #Guardar una copia de cierto organigrama en la base de datos y aparece en la tabla
                    conn = sql.connect("datos.db")
                    # Lógica para guardar los datos
                    ORG = entry_NOM_ORG.get()
                    FEC = entry_FEC.get()
                    COD = generar_codigo_interno_organigrama()

                    if buscar_org(ORG):  ## Este if pregunta si existe un organigrama en la base de datos
                        messagebox.showwarning(message="El organigrama ya existe.")

                    else:  ## Si no existe se agrega
                        if insertar_datos_organigrama(COD, ORG, FEC) != False:
                            conn.commit()
                            conn.close()
                            guardar_depen_copiaOrg()
                            entry_ORIGEN.insert(0, entry_NOM_ORG.get()) # Actualiza el nuevo organigrama al cual se creo la copia
                            entry_ORIGEN.grid(row=0, column=1, pady=10)
                            entry_NOM_ORG.delete(0, tk.END)
                            entry_FEC.delete(0, tk.END)
                        else:
                            messagebox.showwarning(title="❗Alerta Formato de Atributos❗",
                                                   message="ORG)  Cadena, 20 caracteres\n\n"
                                                          + "FEC)  Formato Fecha: \ \ \n")

                def extraer_nombre_persona(COD_PER): # Funcion para traer el nombre de la persona segun su codigo
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    cursor.execute("""SELECT * FROM persona WHERE COD = ?""", (COD_PER,))
                    datos = cursor.fetchone()
                    conn.close()
                    if datos:
                        return datos[3]
                    else:
                        return ""

                def guardar_depen_copiaOrg(): # Guarda una copia de las dependencias del organigrama seleccionado y muestra en la tabla
                    ORIGEN = entry_ORIGEN.get()
                    NOM_ORG = entry_NOM_ORG.get()

                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Busca los datos en la base de datos
                    instruccion = "SELECT * FROM dependencia WHERE NOM_ORG = ?"
                    cursor.execute(instruccion, (ORIGEN,))
                    datos = cursor.fetchall()

                    # Agregar los datos de la copia a la Base de datos de dependencias cambiando el nombre del organigrama
                    for dato in datos:
                        insertar_datos_dependencia(dato[0], dato[1], dato[2], NOM_ORG, dato[4])
                        tabla_copia.insert("", tk.END, values=(dato[1], extraer_nombre_persona(dato[2]), NOM_ORG, dato[4]))
                    entry_ORIGEN.delete(0, tk.END)
                    conn.close()

                def visualizar_datos_copia(): # Muesta todas las dependencias en la tabla de la copia
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    ORIGEN = entry_ORIGEN.get()

                    if buscar_depORG(ORIGEN):
                        # Obtener los datos de la base de datos
                        instruccion = ("SELECT * FROM dependencia WHERE NOM_ORG = ?")
                        cursor.execute(instruccion, (ORIGEN,))
                        datoscopia = cursor.fetchall()

                        # Limpiar la tabla existente, si es necesario
                        tabla_copia.delete(*tabla_copia.get_children())

                        # Agregar los datos a la tabla
                        for dato in datoscopia:
                            tabla_copia.insert("", "end", values=(dato[1], extraer_nombre_persona(dato[2]), dato[3], dato[4]))
                    else:
                        messagebox.showwarning(title="❗Organigrama sin Dependencias❗",
                                               message="Este organigrama no tiene ninguna dependencia\n"
                                                       + "Vuelve para crear sus dependencias")
                    conn.close()
                    # Se activa el entry de organigrama original para elegir con cual organigrama trabajar
                    entry_ORIGEN["state"] = "normal"
                    entry_ORIGEN.grid(row=0, column=1, pady=10)

                def eliminar_dependencia():  # Elimina una dependencia, sus dependencias sucesoras de la base de datos y de la tabla
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    # Obtener el elemento seleccionado en la tabla
                    seleccionado = tabla_copia.focus()
                    if seleccionado:
                        NOM = tabla_copia.set(seleccionado, "NOM")
                        CODRES = tabla_copia.set(seleccionado, "CODRES")
                        NOM_ORG = tabla_copia.set(seleccionado, "NOM_ORG")

                        # Eliminar la fila seleccionada de la tabla
                        tabla_copia.delete(seleccionado)

                        # extraemos el código de la dependencia a eliminar
                        cursor.execute("SELECT * FROM dependencia WHERE NOM = ? AND NOM_ORG = ?", (NOM, NOM_ORG,))
                        datos = cursor.fetchone()

                        if datos:
                            # Eliminar la fila correspondiente en la base de datos
                            instruccion = "DELETE FROM dependencia WHERE COD = ? AND NOM = ? AND CODRES = ? AND NOM_ORG = ? "
                            cursor.execute(instruccion, (datos[0], NOM, CODRES, NOM_ORG))
                            conn.commit()

                            # Eliminar los hijos de esa dependencia elegida
                            instruccion = "DELETE FROM dependencia WHERE NOM_PAD = ?  AND NOM_ORG = ? "
                            cursor.execute(instruccion, (NOM, NOM_ORG))
                            conn.commit()

                            # Eliminar las personas que pertenecen a esa dependencia
                            instruccion = "DELETE FROM personas WHERE DEP = ?"
                            cursor.execute(instruccion, (datos[0],))
                            conn.commit()
                            visualizar_datos_copia()
                    conn.close()

                def editar_dependencia():  # Modifica el nombre y el codigo de jefe de la dependencia seleccionada
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    seleccionado = tabla_copia.focus()
                    if seleccionado:
                        NOM_antiguo = tabla_copia.set(seleccionado, "NOM")
                        NOM = entry_Nuevo_NOM.get()
                        CODRES = entry_Nuevo_JEFE.get()
                        NOM_ORG = tabla_copia.set(seleccionado, "NOM_ORG")

                        # Busca los datos en la base de datos
                        instruccion = "UPDATE dependencia SET NOM = ?, CODRES = ? WHERE NOM_ORG = ? AND NOM = ?"
                        cursor.execute(instruccion, ( NOM, CODRES, NOM_ORG, NOM_antiguo))
                        conn.commit()  # Realizar los cambios
                        entry_Nuevo_NOM.delete(0, tk.END)
                        entry_Nuevo_JEFE.delete(0, tk.END)
                    conn.close()
                    visualizar_datos_copia()

                def editar_ubicacion():  # Modifica la ubicacion de una dependencia seleccionada
                    conn = sql.connect("datos.db")
                    cursor = conn.cursor()
                    seleccionado = tabla_copia.focus()
                    if seleccionado:
                        NOM = tabla_copia.set(seleccionado, "NOM")
                        CODRES = tabla_copia.set(seleccionado, "CODRES")
                        NOM_ORG = tabla_copia.set(seleccionado, "NOM_ORG")
                        NOM_PAD = entry_Nuevo_Padre.get()

                        # Busca los datos en la base de datos
                        instruccion = "UPDATE dependencia SET NOM_PAD = ? WHERE NOM = ? AND CODRES = ? AND NOM_ORG = ?"
                        cursor.execute(instruccion, (NOM_PAD, NOM, CODRES, NOM_ORG))
                        conn.commit()  # Realizar los cambios
                        entry_Nuevo_Padre.delete(0, tk.END)
                    conn.close()
                    visualizar_datos_copia()

                """Controles para copiar un organigrama y editar sus dependencias"""

                # Crear un marco para los controles
                marco_controles_copia = tk.Frame(organigramas, padx=10, pady=10)
                marco_controles_copia.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                # Crear un marco para el recuadro de los botones
                marco_recuadro = tk.Frame(marco_controles_copia, bd=1, relief=tk.RAISED, bg="lightgray")
                marco_recuadro.pack(fill=tk.BOTH, expand=True)

                # Crear un marco para los botones
                marco_formulario = tk.Frame(marco_recuadro, bg="lightgray")
                marco_formulario.pack(padx=5, pady=5, fill=tk.Y, expand=True)

                label_ORIGEN = tk.Label(marco_formulario, text="ORGANIGRAMA ORIGINAL:", anchor= "w")
                label_ORIGEN.grid(row=0, column=0, sticky=tk.W)
                entry_ORIGEN = tk.Entry(marco_formulario)
                # CARGAMOS EN LA CAJA DE TEXTO EL NOMBRE DE LA ORGANIZACIÓN SELECCIONADA ANTERIORMENTE
                entry_ORIGEN.insert(0, variableCopia_nombredelorganigrama)
                entry_ORIGEN["state"] = "readonly"
                entry_ORIGEN.grid(row=0, column=1, pady=10)

                label_NOM_ORG = tk.Label(marco_formulario, text="NUEVO ORGANIGRAMA:", anchor= "w")
                label_NOM_ORG.grid(row=1, column=0, sticky=tk.W)
                entry_NOM_ORG = tk.Entry(marco_formulario)
                entry_NOM_ORG.grid(row=1, column=1, pady=10)

                label_FEC = tk.Label(marco_formulario, text="FECHA:", anchor= "w")
                label_FEC.grid(row=2, column=0, sticky=tk.W)
                entry_FEC = tk.Entry(marco_formulario)
                entry_FEC.grid(row=2, column=1, pady=10)

                boton_guarda = ctk.CTkButton(marco_formulario, text="Copiar", bg_color="lightgray", command=guardar_copiaOrg)
                boton_guarda.grid(row=2, column=2, padx=5, pady=5)

                # Crear una etiqueta encima del recuadro de botones
                label_recuadro = tk.Label(marco_formulario, text="Editar Dependencias", font=("Helvetica", 10, "bold"), bg="lightgray")
                label_recuadro.grid(row=5, column=0, sticky=tk.W)

                label_editar = tk.Label(marco_formulario, text="SELECCIONE EN LA TABLA", anchor= "w")
                label_editar.grid(row=5, column=1, sticky=tk.W)

                label_Nuevo_NOM = tk.Label(marco_formulario, text="NUEVO NOMBRE:", anchor= "w")
                label_Nuevo_NOM.grid(row=7, column=0, sticky=tk.W)
                entry_Nuevo_NOM = tk.Entry(marco_formulario)
                entry_Nuevo_NOM.grid(row=7, column=1, pady=10)

                label_Nuevo_JEFE = tk.Label(marco_formulario, text="NUEVO JEFE:", anchor= "w")
                label_Nuevo_JEFE.grid(row=8, column=0, sticky=tk.W)
                entry_Nuevo_JEFE = tk.Entry(marco_formulario)
                entry_Nuevo_JEFE.grid(row=8, column=1, pady=10)

                boton_modificar = ctk.CTkButton(marco_formulario, text="Editar", bg_color="lightgray", command=editar_dependencia)
                boton_modificar.grid(row=8, column=2, padx=5, pady=5)

                # Crear una etiqueta encima del recuadro de botones
                label_recuadro = tk.Label(marco_formulario, text="Ubicacion Dependencias", font=("Helvetica", 10, "bold"), bg="lightgray")
                label_recuadro.grid(row=9, column=0, sticky=tk.W)

                label_Nuevo_Padre = tk.Label(marco_formulario, text="NUEVO PADRE:", anchor= "w")
                label_Nuevo_Padre.grid(row=11, column=0, sticky=tk.W)
                entry_Nuevo_Padre = tk.Entry(marco_formulario)
                entry_Nuevo_Padre.grid(row=11, column=1, pady=10)

                boton_guardar = ctk.CTkButton(marco_formulario, text="Editar Ubicacion", bg_color="lightgray", command=editar_ubicacion)
                boton_guardar.grid(row=11, column=2, padx=5, pady=5)

                label_Actualizar = tk.Label(marco_formulario, text="Actualiza antes de realizar cambios",  font=("Helvetica", 10, "bold"), bg="lightgray")
                label_Actualizar.grid(row=15, column=0, sticky=tk.W)

                boton_actualizar = ctk.CTkButton(marco_formulario, text="Actualizar tabla", bg_color="lightgray", command=visualizar_datos_copia)
                boton_actualizar.grid(row=16, column=0, padx=5, pady=5)

                boton_eliminar = ctk.CTkButton(marco_formulario, text="Eliminar", bg_color="lightgray", command=eliminar_dependencia)
                boton_eliminar.grid(row=16, column=1, padx=5, pady=5)

                # Crear la tabla
                tabla_copia = ttk.Treeview(organigramas, columns=("NOM", "CODRES", "NOM_ORG", "NOM_PAD"))
                tabla_copia.column("#0", width=0, stretch=tk.NO)
                tabla_copia.heading("NOM", text="NOMBRE")
                tabla_copia.heading("CODRES", text="PERSONA JEFE")
                tabla_copia.heading("NOM_ORG", text="ORGANIGRAMA")
                tabla_copia.heading("NOM_PAD", text="DEPENDENCIA PADRE")
                tabla_copia.pack(fill=tk.BOTH, expand=True)

                # boton que activa una función para eliminar los frames y botones para crear un organigrama
                boton_Volver_marcocontroles = ctk.CTkButton(marco_controles_copia, text="Volver", bg_color="lightgray",
                         command=lambda: cerrar_formularios(marco_controles_copia, tabla_copia, abrir_organigrama))
                boton_Volver_marcocontroles.pack(side=tk.BOTTOM)

        """Aqui estan las funciones de abrir organigrama"""

        def visualizar_datos(): # Muestra todos los organigramas en la tabla para establecer con cual se trabajara
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            # Obtener los datos de la base de datos
            cursor.execute("SELECT * FROM organigrama")
            datos = cursor.fetchall()

            # Limpiar la tabla existente, si es necesario
            tabla.delete(*tabla.get_children())

            # Agregar los datos a la tabla
            for dato in datos:
                tabla.insert("", "end", values=(dato[1], dato[2]))

            conn.close()

        """Sujeto a cambios esta parte, si quieren hacer que se pueda seleccionar desde la tabla y asi ya aparezca
            el nombre del organigrama en crear dependencias y crear copia """

        def buscar(): # Con esta funcion se selecciona el organigramas, el usuario busca y si encuentra empieza a trabajar
            nonlocal variableDep_nombredelorganigrama
            nonlocal variableCopia_nombredelorganigrama
            ORG = entry_ORG.get()
            variableDep_nombredelorganigrama = ORG
            variableCopia_nombredelorganigrama = ORG
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            instruccion = "SELECT * FROM organigrama WHERE ORG = ?"
            cursor.execute(instruccion, (ORG,))
            datos = cursor.fetchall()
            # Limpiar la tabla existente, si es necesario
            tabla.delete(*tabla.get_children())

            ORG = entry_ORG.get()

            if buscar_org(ORG) == True:  ## Este if pregunta si existe el organigrama en la base de datos
                # Agregar los datos a la tabla
                for dato in datos:
                    tabla.insert("", "end", values=(dato[1], dato[2]))
            else:
                messagebox.showwarning(message="Organigrama no encontrado.")

            conn.close()

        def buscar_org(nom_ord): # Busca un organigrama en especifico
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("SELECT * FROM organigrama WHERE ORG = ?", (nom_ord,))
            datos = cursor.fetchone()
            conn.close()
            if datos == None:
                return False
            else:
                return True

        """Controles para Abrir Organigrama"""

        # Crear un marco para los controles
        marco_controles = tk.Frame(organigramas, padx=10, pady=10)
        marco_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a organigramas
        marco_formulario_organigrama = tk.Frame(marco_controles)
        marco_formulario_organigrama.pack(fill=tk.BOTH, expand=True)

        label_ORG = tk.Label(marco_formulario_organigrama, text="ORGANIGRAMA:")
        label_ORG.grid(row=1, column=0, sticky=tk.E)
        entry_ORG = tk.Entry(marco_formulario_organigrama)
        entry_ORG.grid(row=1, column=1, pady=10)

        # El botón para buscar organigramas también guardará en una variable el organigrama con el que se trabajara
        variableDep_nombredelorganigrama = "" # variable que contendrá el nombre del organigrama para crear una dependencia en el
        variableCopia_nombredelorganigrama = ""  # variable que contendrá el nombre del organigrama para crear una copia de el
        boton_buscar = ctk.CTkButton(marco_formulario_organigrama, text="Buscar", bg_color="lightgray", command =buscar)
        boton_buscar.grid(row=1, column=2, padx=5, pady=5)

        # Crear un marco para el recuadro de los botones
        marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
        marco_recuadro.pack(fill=tk.BOTH, expand=True)

        # Crear una etiqueta encima del recuadro de botones
        label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
        label_recuadro.pack(pady=5)

        # Crear un marco para los botones
        marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
        marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

        # Crear los botones
        boton_crear_dependencias = ctk.CTkButton(marco_botones, text="Crear Dependencias", bg_color="lightgray", command=crear_dependencia)
        boton_crear_dependencias.grid(row=1, column=0, padx=5, pady=5)

        boton_copia = ctk.CTkButton(marco_botones, text="Crear Copia", bg_color="lightgray", command=copiar_organigrama)
        boton_copia.grid(row=1, column=1, padx=5, pady=5)

        # Crear los botones
        boton_actualizar = ctk.CTkButton(marco_botones, text="Organigramas Disponibles", bg_color="lightgray", command=visualizar_datos)
        boton_actualizar.grid(row=2, column=0, padx=5, pady=5)

        # Crear la tabla
        tabla = ttk.Treeview(organigramas, columns=("ORG", "FEC"))
        tabla.column("#0", width=0, stretch=tk.NO)
        tabla.heading("ORG", text="ORGANIZACIÓN")
        tabla.heading("FEC", text="FECHA")
        tabla.pack(fill=tk.BOTH, expand=True)

        #boton que activa una función para eliminar los frames y botones para crear un organigrama
        boton_Volver_marcocontroles = ctk.CTkButton(marco_controles, text="Volver",  bg_color="lightgray",
              command= lambda : cerrar_formularios(marco_controles, tabla, ventana_organigrama))
        boton_Volver_marcocontroles.pack(side = tk.BOTTOM)

    """Desde aqui se trabaja con la ventana de organigramas"""

    #Pestaña principal del apartado organigramas
    organigramas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    #barra de opciones de la pestaña organigrama
    #y botón para cerrar la pestaña de organigramas
    barra_opciones_organigramas = tk.Frame(organigramas, bg = "misty rose")
    barra_opciones_organigramas.pack(fill = tk.X)
    boton_cerrar_organigramas = tk.Button(barra_opciones_organigramas,
                                          command=lambda: cerrar_ventana("organigramas", boton_organigramas_menu),
                                          text="x", bg="red", bd = 0, width= 4)
    boton_cerrar_organigramas.grid(row = 0, column=0)

    #Botones que habitan la ventana organigramas y que están dentro de otro frame
    # creamos un frame donde vivirán los botones de organigramas
    organigramasbotones = tk.Frame(organigramas)
    organigramasbotones.pack()

    #Declaramos botones de la clace Boton_animado
    boton_crear_organigrama = Boton_animado(organigramasbotones, 0, 2, 0, 20, "Crear Organigrama", 4, "light salmon", "black",
            crear_organigrama, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")

    boton_crear_organigrama.boton.config(anchor = "center")
    boton_crear_organigrama.vincular_raton()
    boton_crear_organigrama.boton.pack(fill= tk.X, expand=True)

    boton_abrir_organigrama = Boton_animado(organigramasbotones, 0, 2, -37, 100, "Abrir Organigrama", 4, "light salmon", "black",
           abrir_organigrama, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")
    boton_abrir_organigrama.boton.config(anchor = "center")
    boton_abrir_organigrama.vincular_raton()
    boton_abrir_organigrama.boton.pack(fill= tk.X, expand=True)

    boton_graficar_completo = Boton_animado(organigramasbotones, 0, 2, -45, 180, "Graficar Organigrama", 4, "light salmon", "black",
             "Comando", "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")
    boton_graficar_completo.boton.config(anchor = "center")
    boton_graficar_completo.vincular_raton()
    boton_graficar_completo.boton.pack(fill= tk.X, expand=True)

    boton_graficar_dependencia = Boton_animado(organigramasbotones, 0, 2, -50, 220, "Graficar Dependencia", 4, "light salmon", "black",
              "Comando", "pack", "salmon", "Roboto 13", 0, 0, "flat","w")
    boton_graficar_dependencia.boton.config(anchor="center")
    boton_graficar_dependencia.vincular_raton()
    boton_graficar_dependencia.boton.pack(fill=tk.X, expand=True)

def ventana_personas():
    global boton_personas_menu, personas
    boton_personas_menu.bg = "salmon"
    boton_personas_menu.boton["state"] = "disabled"# desactivamos el boton de abrir esta ventana para
                                                   # que no genere problemas con los frames generados en el

    # Funcion para ingresar personas a la base de datos, eliminar, modificar y asignar persona a una dependencia
    def generar_codigo_interno_persona():
        codigo_interno = random.randint(0, 9999)
        codigo_interno = str(codigo_interno).zfill(4)
        return codigo_interno

    def buscar_ID(DOC):  # Para buscar una persona en especifico segun su ID en la base de datos
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        # Busca los datos en la base de datos
        cursor.execute("""SELECT * FROM persona WHERE DOC = ?""", (DOC,))
        datos = cursor.fetchone()
        conn.close()
        if datos == None:
            return False
        else:
            return True

    def buscar_dependencia(NOM_DEP):  # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        # Busca los datos en la base de datos
        cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
        datos = cursor.fetchone()
        conn.close()
        if datos == None:
            return False
        else:
            return True

    def cargar_codigo_DEP(NOM_DEP): # Para cargar el codigo de dependencia segun el nombre ingresado en la tabla de personas
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT COD FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
        datos = cursor.fetchone() # Pocision del codigo de dependencia
        conn.close()
        #si datos != None está cargado, sino retornar vacío
        if datos:
            return datos[0]
        else:
            return ""

    def guardar_personas(): # Guardar y asignar a las personas a una dependencia en la base de datos y tabla de personas
        conn = sql.connect("datos.db")
        COD = generar_codigo_interno_persona()
        DOC = entry_DOC.get()
        APE = entry_APE.get()
        NOM = entry_NOM.get()
        TEL = entry_TEL.get()
        DIR = entry_DIR.get()
        DEP = entry_DEP.get()
        SAL = entry_SAL.get()

        if buscar_ID(DOC): # Verifica que el que no se repitan los ID de las personas
            messagebox.showwarning(title="❗️Documento de identidad❗️", message="Proporcione un documento distinto a los demas")

        else:
            if buscar_dependencia(DEP) or DEP == "Jefe" or DEP == "jefe": # Verifica que no se repitan las personas jefes de dependencia
                if DEP != "Jefe" and DEP != "jefe":
                    CODIGO_DEP = cargar_codigo_DEP(DEP)  # Variable que contiene el codigo de dependencia
                else:
                    CODIGO_DEP = "000"
                ##Condicion para cargar segun lo que pide el pdf.
                if insertar_datos_persona(COD, DOC, APE, NOM, TEL, DIR, CODIGO_DEP, SAL) != False:
                    tabla.insert("", tk.END, values=(DOC, APE, NOM, TEL, DIR, DEP, SAL))
                    conn.commit()
                    conn.close()
                    entry_DOC.delete(0, tk.END)
                    entry_APE.delete(0, tk.END)
                    entry_NOM.delete(0, tk.END)
                    entry_TEL.delete(0, tk.END)
                    entry_DIR.delete(0, tk.END)
                    entry_DEP.delete(0, tk.END)
                    entry_SAL.delete(0, tk.END)
                    messagebox.showinfo(message="Se ha registrado correctamente los datos")

                else:
                    messagebox.showwarning(title="❗️Alerta Formato de Atributos❗️", message="COD) Cadena, 4 digitos\n"
                                                                                            + "DOC) Cadena, 15 caracteres\n"
                                                                                            + "APE) Cadena, 15 letras\n"
                                                                                            + "NOM) Cadena, 15 letras\n"
                                                                                            + "TEL) Cadena, 12 digitos\n"
                                                                                            + "DIR) Cadena, 30 caracteres\n"
                                                                                            + "DEP) Cadena, 3 digitos\n"
                                                                                            + "SAL) Entero, hasta 9 digitos\n")
            else:
                messagebox.showinfo(title="Cargar Dependencia", message="NO se encontro la dependencia\n"
                                                                        + "Verifique si escribio correctamente\n"
                                                                        + "Verifique si existe la dependencia")
        conn.close()

    def eliminar():  # Elimina una persona de la base de datos y de la tabla
        conn = sql.connect("datos.db")
        cursor = conn.cursor()

        # Obtener el elemento seleccionado en la tabla
        seleccionado = tabla.focus()
        if seleccionado:
            DOC = tabla.set(seleccionado, "DOC")
            APE = tabla.set(seleccionado, "APE")
            NOM = tabla.set(seleccionado, "NOM")
            TEL = tabla.set(seleccionado, "TEL")
            DIR = tabla.set(seleccionado, "DIR")
            DEP = tabla.set(seleccionado, "DEP")
            SAL = tabla.set(seleccionado, "SAL")

            COD_DEP = cargar_codigo_DEP(DEP)

            # Eliminar la fila seleccionada de la tabla
            tabla.delete(seleccionado)

            # Eliminar la fila correspondiente en la base de datos
            instruccion = "DELETE FROM persona WHERE DOC = ? AND APE = ? AND NOM = ? AND TEL = ? AND DIR = ? AND DEP = ? AND SAL = ?"
            cursor.execute(instruccion, (DOC, APE, NOM, TEL, DIR, COD_DEP, SAL))
            conn.commit()
        conn.close()

    def modificar():  # Modifica los atributos de una persona seleccionanda desde la tabla
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        seleccionado = tabla.focus()
        if seleccionado:
            DOC = entry_DOC.get()
            APE = entry_APE.get()
            NOM = entry_NOM.get()
            TEL = entry_TEL.get()
            DIR = entry_DIR.get()
            SAL = entry_SAL.get()

            DOC_antiguo = tabla.set(seleccionado, "DOC")

            tabla.item(seleccionado, values=(DOC, APE, NOM, TEL, DIR, SAL))
            entry_DOC.delete(0, tk.END)
            entry_APE.delete(0, tk.END)
            entry_NOM.delete(0, tk.END)
            entry_TEL.delete(0, tk.END)
            entry_DIR.delete(0, tk.END)
            entry_SAL.delete(0, tk.END)
            instruccion = "UPDATE persona SET DOC = ?, APE = ?, NOM = ?, TEL = ?, DIR = ?, SAL = ? WHERE DOC = ?"
            cursor.execute(instruccion, (DOC, APE, NOM, TEL, DIR, SAL, DOC_antiguo))
            conn.commit()  # Realizar los cambios en organigramas
            visualizar_datos()
        conn.close()

    def extraer_nombre(COD_DEP): # Extrae el nombre de dependencia para que aparezca en la tabla
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        if COD_DEP != "000":
            cursor.execute("""SELECT * FROM dependencia WHERE COD = ?""", (COD_DEP,))
            datos = cursor.fetchone()
            if datos is not None:
                datos = datos[1]
            else:
                datos = ""
        else:
            datos = "Jefe sin asignar"
        conn.close()
        return datos

    def buscar_personaDEP(COD_DEP):  # Para buscar una dependencia en cierto organigrama
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        # Busca los datos en la base de datos
        cursor.execute("SELECT * FROM persona WHERE DEP = ?", (COD_DEP,))
        datos = cursor.fetchone()
        conn.close()
        if datos == None:
            return False
        else:
            return True

    def visualizar_datos():  # Para ver los atributos de todas las personas en la tabla
        conn = sql.connect("datos.db")
        cursor = conn.cursor()

        """NOM_DEP = entry_DEP.get()

        if buscar_dependencia(NOM_DEP):
            COD_DEP = cargar_codigo_DEP(NOM_DEP)

            if buscar_personaDEP(COD_DEP):"""

        # Obtener los datos de la base de datos
        instruccion = "SELECT * FROM persona"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        # Limpiar la tabla existente, si es necesario
        tabla.delete(*tabla.get_children())

        # Agregar los datos a la tabla
        for dato in datos:
            tabla.insert("", tk.END, values=(dato[1], dato[2], dato[3], dato[4], dato[5], extraer_nombre(dato[6]), dato[7]))

            """else:
                messagebox.showwarning(title="❗Depenencia sin Personas❗",
                                       message="Esta dependencia no tiene ninguna persona\n"
                                               + "Crea las personas")
        else:
            messagebox.showwarning(title="❗Depenencia no encontrado❗",
                                   message="Verifique si existe la dependencia seleccionada\n")"""
        conn.close()

    def buscar():  # Busca una persona y lo muestra en la tabla
        NOM = entry_NOM.get()
        conn = sql.connect("datos.db")
        cursor = conn.cursor()
        # Busca los datos en la base de datos
        instruccion = "SELECT * FROM persona WHERE NOM = ?"
        cursor.execute(instruccion, (NOM,))
        datos = cursor.fetchall()
        # Limpiar la tabla existente, si es necesario
        tabla.delete(*tabla.get_children())

        # Agregar los datos a la tabla
        for dato in datos:
            tabla.insert("", "end", values=(dato[1], dato[2], dato[3], dato[4], dato[5], extraer_nombre(dato[6]), dato[7]))

        conn.close()

    """"Controles para personas"""

    #barra de opciones de la pestaña organigrama
    #y botón para cerrar la pestaña de organigramas
    barra_opciones_personas = tk.Frame(personas, bg = "misty rose")
    barra_opciones_personas.pack(fill = tk.X)
    boton_cerrar_personas = tk.Button(barra_opciones_personas,
                                          command=lambda: cerrar_ventana("personas", boton_personas_menu),
                                          text="x", bg="red", bd = 0, width= 4)
    boton_cerrar_personas.grid(row = 0, column=0)

    # Crear un marco para los controles
    marco_controles = tk.Frame(personas, padx=10, pady=10)
    marco_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a organigramas
    marco_formulario_organigrama = tk.Frame(marco_controles)
    marco_formulario_organigrama.pack(fill=tk.BOTH, expand=True)

    # Crear una etiqueta encima del recuadro de botones
    label_recuadro = tk.Label(marco_formulario_organigrama, text="Proporcione la dependecia en el cual desea asignar Personas", font=("Helvetica", 10, "bold"))
    label_recuadro.grid(row=1, column=1, sticky=tk.N)

    label_recuadro = tk.Label(marco_formulario_organigrama, text="Si desea que la persona sea jefe ponga 'Jefe' ", font=("Helvetica", 10, "bold"))
    label_recuadro.grid(row=2, column=1, sticky=tk.N)

    label_DEP = tk.Label(marco_formulario_organigrama, text="DEPENDENCIA:")
    label_DEP.grid(row=3, column=0, sticky=tk.E)
    entry_DEP = tk.Entry(marco_formulario_organigrama)
    entry_DEP.grid(row=3, column=1, pady=10)

    label_DOC = tk.Label(marco_formulario_organigrama, text="DOCUMENTO:")
    label_DOC.grid(row=4, column=0, sticky=tk.E)
    entry_DOC = tk.Entry(marco_formulario_organigrama)
    entry_DOC.grid(row=4, column=1, pady=10)

    label_APE = tk.Label(marco_formulario_organigrama, text="APELLIDO:")
    label_APE.grid(row=5, column=0, sticky=tk.E)
    entry_APE = tk.Entry(marco_formulario_organigrama)
    entry_APE.grid(row=5, column=1, pady=10)

    label_NOM = tk.Label(marco_formulario_organigrama, text="NOMBRE:")
    label_NOM.grid(row=6, column=0, sticky=tk.E)
    entry_NOM = tk.Entry(marco_formulario_organigrama)
    entry_NOM.grid(row=6, column=1, pady=10)

    label_TEL = tk.Label(marco_formulario_organigrama, text="TELEFONO:")
    label_TEL.grid(row=7, column=0, sticky=tk.E)
    entry_TEL = tk.Entry(marco_formulario_organigrama)
    entry_TEL.grid(row=7, column=1, pady=10)

    label_DIR = tk.Label(marco_formulario_organigrama, text="DIRECCION:")
    label_DIR.grid(row=8, column=0, sticky=tk.E)
    entry_DIR = tk.Entry(marco_formulario_organigrama)
    entry_DIR.grid(row=8, column=1, pady=10)

    label_SAL = tk.Label(marco_formulario_organigrama, text="SALARIO:")
    label_SAL.grid(row=9, column=0, sticky=tk.E)
    entry_SAL = tk.Entry(marco_formulario_organigrama)
    entry_SAL.grid(row=9, column=1, pady=10)

    # Crear un marco para el recuadro de los botones
    marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
    marco_recuadro.pack(fill=tk.BOTH, expand=True)

    # Crear una etiqueta encima del recuadro de botones
    label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
    label_recuadro.pack(pady=5)

    # Crear un marco para los botones
    marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
    marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

    # Crear los botones
    boton_guardar = ctk.CTkButton(marco_botones, text="Ingresar", bg_color="lightgray", command=guardar_personas)
    boton_guardar.grid(row=0, column=0, padx=5, pady=5)

    boton_modificar = ctk.CTkButton(marco_botones, text="Modificar", bg_color="lightgray", command=modificar)
    boton_modificar.grid(row=0, column=1, padx=5, pady=5)

    boton_eliminar = ctk.CTkButton(marco_botones, text="Eliminar", bg_color="lightgray", command=eliminar)
    boton_eliminar.grid(row=1, column=0, padx=5, pady=5)

    boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=buscar)
    boton_buscar.grid(row=1, column=1, padx=5, pady=5)

    boton_actualizar = ctk.CTkButton(marco_botones, text="Actualizar tabla", bg_color="lightgray",
                                     command=visualizar_datos)
    boton_actualizar.grid(row=2, column=0, padx=5, pady=5)

    # Crear la tabla para mostrar al usuario las informaciones de las personas ya cargadas
    tabla = ttk.Treeview(personas, columns=("DOC", "APE", "NOM", "TEL", "DIR", "DEP", "SAL"))
    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.heading("DOC", text="DOCUMENTO")
    tabla.heading("APE", text="APELLIDO")
    tabla.heading("NOM", text="NOMBRE")
    tabla.heading("TEL", text="TELEFONO")
    tabla.heading("DIR", text="DIRECCION")
    tabla.heading("DEP", text="DEPENDENCIA")
    tabla.heading("SAL", text="SALARIO")
    tabla.pack(fill=tk.BOTH, expand=True)

    personas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

def ventana_informes():
    global boton_informes_menu, informes
    boton_informes_menu.bg = "salmon"
    boton_informes_menu.boton["state"] = "disable"#desactivamos el boton de abrir esta ventana para
                                                        #que no genere problemas con los frames generados en el

    def personal_por_dependencia():
        #limpiamos el frame para mostrar el formulario de informes por dependencia
        informesbotones.destroy()
        barra_opciones_informes.destroy()

        def cerrar_formularios(widget, widget2, widget3, widget4, widget5, command):
            widget.destroy()
            widget2.destroy()
            widget3.destroy()
            widget4.destroy()
            widget5.destroy()
            command()

        def buscar_dependencia(NOM_DEP):  # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()[0]
            conn.close()
            return datos

        def buscar_existencia_dep(NOM_DEP): # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()
            conn.close()
            if datos == None:
                return False
            else:
                return True


        def ordenar_apellidos_nombres(datos): #función que ordena por nombre y apellido la matriz con datos de personas
            # Definir función de clave personalizada para ordenar por nombre y apellido
            def clave_personalizada(elemento):
                nombre = elemento[3]
                apellido = elemento[2]
                return (apellido, nombre)

            # Ordenar la matriz utilizando la función de clave personalizada
            matriz_ordenada = sorted(datos, key=clave_personalizada)

            return matriz_ordenada

        def mostrar_personas():
            NOM_DEP = entry_dep.get()
            if NOM_DEP != "" and buscar_existencia_dep(NOM_DEP) != False:
                conn = sql.connect("datos.db")
                cursor = conn.cursor()
                tabla_informe.delete(*tabla_informe.get_children())
                #buscamos el código de la dependencia para buscar a las personas
                COD_DEP = buscar_dependencia(NOM_DEP)

                cursor.execute("SELECT * FROM persona WHERE DEP = ?", (COD_DEP, ))
                #extraemos los datos a una matriz
                datos = cursor.fetchall()
                datos = ordenar_apellidos_nombres(datos)
                #lo mostramos en la tabla de informes, con un ciclo cargamos las celdas
                for dato in datos:
                    tabla_informe.insert("", "end", values =(dato[1], dato[2], dato[3], dato[4], dato[5], NOM_DEP, dato[7]))

                #cerramos el acceso a la base de datos
                conn.close()
            else:
                messagebox.showwarning(title="❗️Alerta búsqueda incorrecta❗️",
                                       message=" No se ingresó correctamente el nombre de la dependencia "
                                               + "        a la que pertenecen las personas buscadas")

        #función que nos permite extraer todas las depencencias disponibles y mostrarselas al usuario
        def ver_dependencias_disponibles():
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dependencia")
            datos = cursor.fetchall()

            #especificamos que traemos una variable que no pertenece a la función
            nonlocal tabla_DEPENDENCIA

            for dato in datos:
                tabla_DEPENDENCIA.insert("", "end", values=(dato[1], dato[3]))

            conn.close()

        #creamos el formulario a completar para poder realizar la búsqueda
        # Crear un marco para los controles
        marco_controles = tk.Frame(informes, padx=10, pady=10)
        marco_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a informes
        marco_formulario_organigrama = tk.Frame(marco_controles)
        marco_formulario_organigrama.pack(fill=tk.BOTH, expand=True)

        label_titulo = tk.Label(marco_formulario_organigrama, text="BÚSQUEDA DE PERSONAS POR DEPENDENCIAS", fg = "orangered",
                                font = "Calibri 15")
        label_titulo.grid(row=1, column=0, columnspan= 2)

        label_dep = tk.Label(marco_formulario_organigrama, text="NOMBRE DE LA DEPENDENCIA: ")
        label_dep.grid(row=2, column=0, sticky=tk.E)
        entry_dep = tk.Entry(marco_formulario_organigrama)
        entry_dep.grid(row=2, column=1, pady=10)

        # Crear un marco para el recuadro de los botones
        marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
        marco_recuadro.pack(fill=tk.BOTH, expand=True)

        # Crear una etiqueta encima del recuadro de botones
        label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
        label_recuadro.pack(pady=5)

        # Crear un marco para los botones
        marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
        marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

        # Crear los botones
        boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=mostrar_personas)
        boton_buscar.grid(row=1, column=0, padx=5, pady=5)

        boton_ver_dependencias = ctk.CTkButton(marco_botones, text="DEPENDENCIAS DISPONIBLES", bg_color="lightgray", command=ver_dependencias_disponibles)
        boton_ver_dependencias.grid(row=2, column=0, padx=5, pady=5)

        #etiqueta para comunicar al usuario que la tabla muestra las personas disponibles por dependencias
        e_tiqueta_informes_personasdependencias = tk.Label(informes, text = "INFORME", anchor = "center", bg = "salmon")
        e_tiqueta_informes_personasdependencias.pack(fill = tk.X, expand= True, padx = 0, pady = 0)

        # Crear la tabla informes por dependencia
        tabla_informe = ttk.Treeview(informes, columns=("DOC", "APE", "NOM", "TEL", "DIR", "DEP", "SAL"))
        tabla_informe.column("#0", width=0, stretch=tk.NO)
        tabla_informe.heading("DOC", text="DOCUMENTO")
        tabla_informe.heading("APE", text="APELLIDO")
        tabla_informe.heading("NOM", text="NOMBRE")
        tabla_informe.heading("TEL", text="TELEFONO")
        tabla_informe.heading("DIR", text="DIRECCION")
        tabla_informe.heading("DEP", text="DEPENDENCIA")
        tabla_informe.heading("SAL", text="SALARIO")
        tabla_informe.pack(fill = tk.BOTH, expand= True)

        #etiqueta para comunicar al usuario que lo que está viendo es sobre las dependencias disponibles
        e_tiqueta_informes_dependencias = tk.Label(informes, text = "DEPENDENCIAS DISPONIBLES", bg = "salmon")
        e_tiqueta_informes_dependencias.pack(fill = tk.X, expand = True, padx = 0, pady= 0)

        # Crear la tabla que nos muestra las depencencias disponibles con su respectiva organización
        tabla_DEPENDENCIA = ttk.Treeview(informes, columns=("DEPENDENCIAS DISPONIBLES", "ORGANIZACIÓN"))
        tabla_DEPENDENCIA.column("#0", width=0, stretch=tk.NO)
        tabla_DEPENDENCIA.heading("DEPENDENCIAS DISPONIBLES", text="DEPENDENCIAS DISPONIBLES")
        tabla_DEPENDENCIA.heading("ORGANIZACIÓN", text="ORGANIZACIÓN")
        tabla_DEPENDENCIA.pack(fill = tk.BOTH, expand= True)

        #boton que activa una función para eliminar los frames y botones para crear un organigrama
        boton_Volver_marcocontroles = ctk.CTkButton(marco_controles, text="Volver",  bg_color="lightgray",
              command= lambda : cerrar_formularios(marco_controles, tabla_informe, tabla_DEPENDENCIA,
                e_tiqueta_informes_dependencias, e_tiqueta_informes_personasdependencias, ventana_informes))
        boton_Volver_marcocontroles.pack(side = tk.BOTTOM)


    def personal_por_dep_ext():
        # limpiamos el frame para mostrar el formulario de informes por dependencia
        informesbotones.destroy()
        barra_opciones_informes.destroy()

        def cerrar_formularios(widget, widget2, widget3, widget4, widget5, command): #cierra el formulario para volver
            widget.destroy()                                                         #a la pestaña anterior
            widget2.destroy()
            widget3.destroy()
            widget4.destroy()
            widget5.destroy()
            command()

        def buscar_descendencia_dependencia(NOM_DEP):
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dependencia WHERE NOM_PAD = ?", (NOM_DEP,))
            datos = cursor.fetchall()
            #inicializamos una lista que contendrá los códigos de las descencencias de la dependencia que se le pasó a la función
            codigos_descendencias = []

            #lo cargamos con los códigos utilizando un ciclo que se repite tantas filas tenga la matriz de datos
            #extraídos de la base de datos
            for dato in datos:
                codigos_descendencias.append(dato[0]) #el código para identificar a cada matriz se encuentra en la primera columna
            if datos:
                return codigos_descendencias  # retorna el código de la descendencia
            else:
                return None # retorna una lista vacía si no se encontró descendencia

        def buscar_dependencia(NOM_DEP):  # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()[0]
            conn.close()
            #retorna el código de la dependencia ubicado en la tabla de la base de datos en primera posición
            return datos

        def buscar_existencia_dep(NOM_DEP): # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()
            conn.close()
            if datos == None:
                return False
            else:
                return True

        def ordenar_apellidos_nombres(
                datos):  # función que ordena por nombre y apellido la matriz con datos de personas
            # Definir función de clave personalizada para ordenar por nombre y apellido
            def clave_personalizada(elemento):
                nombre = elemento[3]
                apellido = elemento[2]
                return (apellido, nombre)

            # Ordenar la matriz utilizando la función de clave personalizada
            matriz_ordenada = sorted(datos, key=clave_personalizada)

            return matriz_ordenada

        def mostrar_personas():
            # declaramos la variable que contiene el nombre de la dependencia padre como una cola con la clase deque de la librería estandar colecctions que luego va
            # a contener el nombre de las dependencias sucesoras
            NOM_DEP = deque([entry_dep.get()])
            if NOM_DEP[0] != "" and buscar_existencia_dep(NOM_DEP[0]) != False:
                tabla_informe.delete(*tabla_informe.get_children())
                conn = sql.connect("datos.db")
                cursor = conn.cursor()
                # para la primera vez
                COD_DEP = buscar_dependencia(NOM_DEP[0])
                cursor.execute("SELECT * FROM persona WHERE DEP = ?", (COD_DEP,))
                # extraemos los datos a una matriz
                datos = cursor.fetchall()
                if datos == None:
                    messagebox.showwarning(title="❗️Alerta búsqueda incorrecta❗️",
                                           message=" La dependencia seleccionada no tiene personas asociadas ")
                #luego en el ciclo usamos la búsqueda del código de la descendencia y este para de realizarse cuando
                #ya no hayan sucesoras
                while len(NOM_DEP) != 0:
                    if NOM_DEP[0] != None:
                        COD_DEP = buscar_descendencia_dependencia(NOM_DEP[0])
                        if COD_DEP != None:
                            for cod_dep in COD_DEP:
                                #cargamos en la cola deque los nombres de las dependencia sucesoras de nuestra dependencia
                                #que ahora estamos utilizando como dependencia padre
                                cursor.execute("SELECT * FROM dependencia WHERE COD = ?", (cod_dep, ))
                                nombre_dependencia = cursor.fetchone()
                                NOM_DEP.append(nombre_dependencia[1])
                                #buscamos las personas que pertenecen a la dependencia hija
                                cursor.execute("SELECT * FROM persona WHERE DEP = ?", (cod_dep,))
                                # extraemos los datos a una matriz
                                datos.extend(cursor.fetchall())
                    #eliminamos el nombre de la dependencia utizada
                    NOM_DEP.popleft()

                #ordenamos la matriz por nombre y apellido en otra función con el método sorted
                datos = ordenar_apellidos_nombres(datos)
                # lo mostramos en la tabla de informes, con un ciclo cargamos las celdas
                for dato in datos:
                    cursor.execute("SELECT * FROM dependencia WHERE COD = ?", (dato[6], ))
                    NOM_DEP = cursor.fetchone()[1]
                    tabla_informe.insert("", "end", values=(dato[1], dato[2], dato[3], dato[4], dato[5], NOM_DEP, dato[7]))

                # cerramos el acceso a la base de datos
                conn.close()
            else:
                messagebox.showwarning(title="❗️Alerta búsqueda incorrecta❗️",
                                       message=" No se ingresó correctamente el nombre de la dependencia "
                                               + "        a la que pertenecen las personas buscadas")

        # función que nos permite extraer todas las depencencias disponibles y mostrarselas al usuario
        def ver_dependencias_disponibles():
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dependencia")
            datos = cursor.fetchall()

            # especificamos que traemos una variable que no pertenece a la función
            nonlocal tabla_DEPENDENCIA

            for dato in datos:
                tabla_DEPENDENCIA.insert("", "end", values=(dato[1], dato[3]))

            conn.close()

        # creamos el formulario a completar para poder realizar la búsqueda
        # Crear un marco para los controles
        marco_controles = tk.Frame(informes, padx=10, pady=10)
        marco_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a informes
        marco_formulario_organigrama = tk.Frame(marco_controles)
        marco_formulario_organigrama.pack(fill=tk.BOTH, expand=True)

        label_titulo = tk.Label(marco_formulario_organigrama, text="BÚSQUEDA EXTENDIDA POR DEPENDENCIAS",
                                fg="orangered", font = "Calibri 15")
        label_titulo.grid(row=1, column=0, columnspan=2)

        label_dep = tk.Label(marco_formulario_organigrama, text="DEPENDENCIA JEFE: ")
        label_dep.grid(row=2, column=0, sticky=tk.E)
        entry_dep = tk.Entry(marco_formulario_organigrama)
        entry_dep.grid(row=2, column=1, pady=10)

        # Crear un marco para el recuadro de los botones
        marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
        marco_recuadro.pack(fill=tk.BOTH, expand=True)

        # Crear una etiqueta encima del recuadro de botones
        label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
        label_recuadro.pack(pady=5)

        # Crear un marco para los botones
        marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
        marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

        # Crear los botones
        boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=mostrar_personas)
        boton_buscar.grid(row=1, column=0, padx=5, pady=5)

        boton_ver_dependencias = ctk.CTkButton(marco_botones, text="DEPENDENCIAS DISPONIBLES", bg_color="lightgray",
                                               command=ver_dependencias_disponibles)
        boton_ver_dependencias.grid(row=2, column=0, padx=5, pady=5)

        # etiqueta para comunicar al usuario que la tabla muestra las personas disponibles por dependencias
        e_tiqueta_informes_personasdependencias = tk.Label(informes, text="INFORME COMPLETO", anchor="center", bg="salmon")
        e_tiqueta_informes_personasdependencias.pack(fill=tk.X, expand=True, padx=0, pady=0)

        # Crear la tabla informes por dependencia
        tabla_informe = ttk.Treeview(informes, columns=("DOC", "APE", "NOM", "TEL", "DIR", "DEP", "SAL"))
        tabla_informe.column("#0", width=0, stretch=tk.NO)
        tabla_informe.heading("DOC", text="DOCUMENTO")
        tabla_informe.heading("APE", text="APELLIDO")
        tabla_informe.heading("NOM", text="NOMBRE")
        tabla_informe.heading("TEL", text="TELEFONO")
        tabla_informe.heading("DIR", text="DIRECCION")
        tabla_informe.heading("DEP", text="DEPENDENCIA")
        tabla_informe.heading("SAL", text="SALARIO")
        tabla_informe.pack(fill=tk.BOTH, expand=True)

        # etiqueta para comunicar al usuario que lo que está viendo es sobre las dependencias disponibles
        e_tiqueta_informes_dependencias = tk.Label(informes, text="DEPENDENCIAS DISPONIBLES", bg="salmon")
        e_tiqueta_informes_dependencias.pack(fill=tk.X, expand=True, padx=0, pady=0)

        # Crear la tabla que nos muestra las depencencias disponibles con su respectiva organización
        tabla_DEPENDENCIA = ttk.Treeview(informes, columns=("DEPENDENCIAS DISPONIBLES", "ORGANIZACIÓN"))
        tabla_DEPENDENCIA.column("#0", width=0, stretch=tk.NO)
        tabla_DEPENDENCIA.heading("DEPENDENCIAS DISPONIBLES", text="DEPENDENCIAS DISPONIBLES")
        tabla_DEPENDENCIA.heading("ORGANIZACIÓN", text="ORGANIZACIÓN")
        tabla_DEPENDENCIA.pack(fill=tk.BOTH, expand=True)

        # boton que activa una función para eliminar los frames y botones para crear un organigrama
        boton_Volver_marcocontroles = ctk.CTkButton(marco_controles, text="Volver", bg_color="lightgray",
                                                    command=lambda: cerrar_formularios(marco_controles, tabla_informe,
                                                                                       tabla_DEPENDENCIA,
                                                                                       e_tiqueta_informes_dependencias,
                                                                                       e_tiqueta_informes_personasdependencias,
                                                                                       ventana_informes))
        boton_Volver_marcocontroles.pack(side=tk.BOTTOM)

    def salario_por_dependencia():
        # limpiamos el frame para mostrar el formulario de salarios por dependencia
        informesbotones.destroy()
        barra_opciones_informes.destroy()

        def cerrar_formularios(widget, widget2, widget3, widget4, widget5, widget6, command): #cierra el formulario para volver
            widget.destroy()                                                         #a la pestaña anterior
            widget2.destroy()
            widget3.destroy()
            widget4.destroy()
            widget5.destroy()
            widget6.destroy()
            command()

        def buscar_dependencia(NOM_DEP):  # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()[0]
            conn.close()
            #retorna el código de la dependencia ubicado en la tabla de la base de datos en primera posición
            return datos

        def buscar_existencia_dep(NOM_DEP): # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()
            conn.close()
            if datos == None:
                return False
            else:
                return True

        def ordenar_apellidos_nombres(datos):  # función que ordena por nombre y apellido la matriz con datos de personas
            # Definir función de clave personalizada para ordenar por nombre y apellido
            def clave_personalizada(elemento):
                nombre = elemento[3]
                apellido = elemento[2]
                return (apellido, nombre)

            # Ordenar la matriz utilizando la función de clave personalizada
            matriz_ordenada = sorted(datos, key=clave_personalizada)

            return matriz_ordenada

        def mostrar_salarios(): #muestra en la tabla al usuario el salario del personal y la cantidad de personas de una dependencia
            NOM_DEP = entry_dep.get() #nombre de la dependencia de la cual vamos a buscar las personas
            if NOM_DEP != "" and buscar_existencia_dep(NOM_DEP) != False:
                conn = sql.connect("datos.db")
                cursor = conn.cursor()
                tabla_salario.delete(*tabla_salario.get_children())
                # buscamos el código de la dependencia para buscar a las personas
                COD_DEP = buscar_dependencia(NOM_DEP)

                cursor.execute("SELECT * FROM persona WHERE DEP = ?", (COD_DEP,))
                # extraemos los datos a una matriz
                datos = cursor.fetchall()
                if datos == [] or datos == "":
                    messagebox.showwarning(title="❗️Alerta no se cargaron personas❗️",
                                           message=" No hay personas relacionadas a esta dependencia"
                                                   + "              por favor ingrese personal en personas")
                datos = ordenar_apellidos_nombres(datos)

                cont = 0#contador que nos ayudará a ver cuantas personas posee una dependencia
                suma = 0#acumulador de la suma de los salarios
                # lo mostramos en la tabla de informes, con un ciclo cargamos las celdas
                for dato in datos:
                    cont = cont+1
                    suma = suma + int(dato[7])
                    tabla_salario.insert("", "end", values=(cont, dato[2], dato[3], dato[7], NOM_DEP))

                # cerramos el acceso a la base de datos
                conn.close()

                #editamos la etiqueta que guarda los resultados del total de salarios y total de personal
                entry_total_salario.config(state= "normal")
                entry_total_salario.insert(0, "                       |TOTAL SALARIO = " + str(suma) + "|       |CANTIDAD DE PERSONAL DE LA DEPENDENCIA = " + str(cont) + "|")
                entry_total_salario.config(state= "readonly")
            else:
                messagebox.showwarning(title="❗️Alerta búsqueda incorrecta❗️",
                                       message=" No se ingresó correctamente el nombre de la dependencia "
                                               + "        a la que pertenecen las personas buscadas")

        # función que nos permite extraer todas las depencencias disponibles y mostrarselas al usuario
        def ver_dependencias_disponibles():
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dependencia")
            datos = cursor.fetchall()

            # especificamos que traemos una variable que no pertenece a la función
            nonlocal tabla_DEPENDENCIA

            for dato in datos:
                tabla_DEPENDENCIA.insert("", "end", values=(dato[1], dato[3]))

            conn.close()


        # creamos el formulario a completar para poder realizar la búsqueda
        # Crear un marco para los controles
        marco_controles = tk.Frame(informes, padx=10, pady=10)
        marco_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a informes
        marco_formulario_organigrama = tk.Frame(marco_controles)
        marco_formulario_organigrama.pack(fill=tk.BOTH, expand=True)

        label_titulo = tk.Label(marco_formulario_organigrama, text = "SALARIOS Y TOTAL DE PERSONAL",
                                fg="orangered", font = "Calibri 15", anchor = "center")
        label_titulo.grid(row=1, column=0, columnspan=2)

        label_dep = tk.Label(marco_formulario_organigrama, text="NOMBRE DE LA DEPENDENCIA: ")
        label_dep.grid(row=2, column=0, sticky=tk.E)
        entry_dep = tk.Entry(marco_formulario_organigrama)
        entry_dep.grid(row=2, column=1, pady = 10)

        # Crear un marco para el recuadro de los botones
        marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
        marco_recuadro.pack(fill=tk.BOTH, expand=True)

        # Crear una etiqueta encima del recuadro de botones
        label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
        label_recuadro.pack(pady=5)

        # Crear un marco para los botones
        marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
        marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

        # Crear los botones
        boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=mostrar_salarios)
        boton_buscar.grid(row=1, column=0, padx=5, pady=5)

        boton_ver_dependencias = ctk.CTkButton(marco_botones, text="DEPENDENCIAS DISPONIBLES", bg_color="lightgray",
                                               command=ver_dependencias_disponibles)
        boton_ver_dependencias.grid(row=2, column=0, padx=5, pady=5)

        # etiqueta para comunicar al usuario que la tabla muestra las personas disponibles por dependencias
        e_tiqueta_informes_personasdependencias = tk.Label(informes, text="SALARIOS, NOMBRES Y CANTIDAD DE PERSONAL",
                                                           anchor="center", bg="salmon")
        e_tiqueta_informes_personasdependencias.pack(fill=tk.X, expand=True, padx=0, pady=0)

        # Crear la tabla de salarios por dependencia
        tabla_salario = ttk.Treeview(informes, columns=("#", "APELLIDO", "NOMBRE", "SALARIO", "DEPENDENCIA"))
        tabla_salario.column("#0", width=0, stretch=tk.NO)
        tabla_salario.heading("#", text= "#")
        tabla_salario.column("#", width= 3)
        tabla_salario.heading("APELLIDO", text = "APELLIDO")
        tabla_salario.column("APELLIDO", width= 300)
        tabla_salario.heading("NOMBRE", text = "NOMBRE")
        tabla_salario.column("NOMBRE", width= 300)
        tabla_salario.heading("SALARIO", text = "SALARIO")
        tabla_salario.column("SALARIO", width= 300)
        tabla_salario.heading("DEPENDENCIA", text = "DEPENDENCIA")
        tabla_salario.column("DEPENDENCIA", width= 300)
        tabla_salario.pack(fill=tk.BOTH, expand=True)

        entry_total_salario = tk.Entry(informes, state = "readonly", font = "Calibri 20") #etiqueta que mostrará la suma de los salarios y la cantidad de personal
                                                    #en síntesis el resumen de lo ya puesto en la tabla
        entry_total_salario.pack(fill = tk.BOTH, expand= True)


        # etiqueta para comunicar al usuario que lo que está viendo es sobre las dependencias disponibles
        e_tiqueta_informes_dependencias = tk.Label(informes, text="DEPENDENCIAS DISPONIBLES", bg="salmon")
        e_tiqueta_informes_dependencias.pack(fill=tk.X, expand=True, padx=0, pady=0)

        # Crear la tabla que nos muestra las depencencias disponibles con su respectiva organización
        tabla_DEPENDENCIA = ttk.Treeview(informes, columns=("DEPENDENCIAS DISPONIBLES", "ORGANIZACIÓN"))
        tabla_DEPENDENCIA.column("#0", width=0, stretch=tk.NO)
        tabla_DEPENDENCIA.heading("DEPENDENCIAS DISPONIBLES", text="DEPENDENCIAS DISPONIBLES")
        tabla_DEPENDENCIA.heading("ORGANIZACIÓN", text="ORGANIZACIÓN")
        tabla_DEPENDENCIA.pack(fill=tk.BOTH, expand=True)

        # boton que activa una función para eliminar los frames y botones para crear un organigrama
        boton_Volver_marcocontroles = ctk.CTkButton(marco_controles, text="Volver", bg_color="lightgray",
                                                    command=lambda: cerrar_formularios(marco_controles, tabla_salario,
                                                                                       tabla_DEPENDENCIA,
                                                                                       e_tiqueta_informes_dependencias,
                                                                                       e_tiqueta_informes_personasdependencias,
                                                                                       entry_total_salario,
                                                                                       ventana_informes))
        boton_Volver_marcocontroles.pack(side=tk.BOTTOM)

    def salario_extendido():
        # limpiamos el frame para mostrar el formulario de informes por dependencia
        informesbotones.destroy()
        barra_opciones_informes.destroy()

        def cerrar_formularios(widget, widget2, widget3, widget4, widget5, command):  # cierra el formulario para volver
            widget.destroy()  # a la pestaña anterior
            widget2.destroy()
            widget3.destroy()
            widget4.destroy()
            widget5.destroy()
            command()

        def buscar_descendencia_dependencia(NOM_DEP):
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dependencia WHERE NOM_PAD = ?", (NOM_DEP,))
            datos = cursor.fetchall()
            # inicializamos una lista que contendrá los códigos de las descencencias de la dependencia que se le pasó a la función
            codigos_descendencias = []

            # lo cargamos con los códigos utilizando un ciclo que se repite tantas filas tenga la matriz de datos
            # extraídos de la base de datos
            for dato in datos:
                codigos_descendencias.append(
                    dato[0])  # el código para identificar a cada matriz se encuentra en la primera columna
            if datos:
                return codigos_descendencias  # retorna el código de la descendencia
            else:
                return None  # retorna una lista vacía si no se encontró descendencia

        def buscar_dependencia(
                NOM_DEP):  # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()[0]
            conn.close()
            # retorna el código de la dependencia ubicado en la tabla de la base de datos en primera posición
            return datos

        def buscar_existencia_dep(
                NOM_DEP):  # Para buscar una dependencia en especifico en la base de datos para asignarle una persona
            conn = sql.connect("datos.db")
            cursor = conn.cursor()
            # Busca los datos en la base de datos
            cursor.execute("""SELECT * FROM dependencia WHERE NOM = ?""", (NOM_DEP,))
            datos = cursor.fetchone()
            conn.close()
            if datos == None:
                return False
            else:
                return True

        def mostrar_salarios(NOM_DEP): #muestra en la tabla al usuario el salario del personal y la cantidad de personas de una dependencia
            if NOM_DEP != "" and buscar_existencia_dep(NOM_DEP) != False:
                conn = sql.connect("datos.db")
                cursor = conn.cursor()
                # buscamos el código de la dependencia para buscar a las personas
                COD_DEP = buscar_dependencia(NOM_DEP)

                cursor.execute("SELECT * FROM persona WHERE DEP = ?", (COD_DEP,))
                # extraemos los datos a una matriz
                datos = cursor.fetchall()
                if datos == [] or datos == "":
                    messagebox.showwarning(title="❗️Alerta no se cargaron personas❗️",
                                           message=" No hay personas relacionadas a esta dependencia"
                                                   + "              por favor ingrese personal en personas")

                cont = 0#contador que nos ayudará a ver cuantas personas posee una dependencia
                suma = 0#acumulador de la suma de los salarios
                # lo mostramos en la tabla de informes, con un ciclo cargamos las celdas
                for dato in datos:
                    cont = cont+1
                    suma = suma + int(dato[7])

                tabla_informe.insert("", "end", values=(suma, cont, NOM_DEP))

                # cerramos el acceso a la base de datos
                conn.close()

        def mostrar_salarios_extendido():
            # declaramos la variable que contiene el nombre de la dependencia padre como una cola con la clase deque de la librería estandar colecctions que luego va
            # a contener el nombre de las dependencias sucesoras
            NOM_DEP = deque([entry_dep.get()])
            if NOM_DEP[0] != "" and buscar_existencia_dep(NOM_DEP[0]) != False:
                tabla_informe.delete(*tabla_informe.get_children())
                conn = sql.connect("datos.db")
                cursor = conn.cursor()
                # para la primera vez
                COD_DEP = buscar_dependencia(NOM_DEP[0])
                cursor.execute("SELECT * FROM persona WHERE DEP = ?", (COD_DEP,))
                # extraemos los datos a una matriz
                datos = cursor.fetchall()
                if datos == None:
                    messagebox.showwarning(title="❗️Alerta búsqueda incorrecta❗️",
                                           message=" La dependencia seleccionada no tiene personas asociadas ")
                # luego en el ciclo usamos la búsqueda del código de la descendencia y este para de realizarse cuando
                # ya no hayan sucesoras
                while len(NOM_DEP) != 0:
                    if NOM_DEP[0] != None:
                        COD_DEP = buscar_descendencia_dependencia(NOM_DEP[0])
                        if COD_DEP != None:
                            for cod_dep in COD_DEP:
                                # cargamos en la cola deque los nombres de las dependencia sucesoras de nuestra dependencia
                                # que ahora estamos utilizando como dependencia padre
                                cursor.execute("SELECT * FROM dependencia WHERE COD = ?", (cod_dep,))
                                nombre_dependencia = cursor.fetchone()
                                NOM_DEP.append(nombre_dependencia[1])
                                mostrar_salarios(NOM_DEP[0])
                    # eliminamos el nombre de la dependencia utizada
                    NOM_DEP.popleft()

                # cerramos el acceso a la base de datos
                conn.close()
            else:
                messagebox.showwarning(title="❗️Alerta búsqueda incorrecta❗️",
                                       message=" No se ingresó correctamente el nombre de la dependencia "
                                               + "        a la que pertenecen las personas buscadas")

        # función que nos permite extraer todas las depencencias disponibles y mostrarselas al usuario
        def ver_dependencias_disponibles():
            conn = sql.connect("datos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM dependencia")
            datos = cursor.fetchall()

            # especificamos que traemos una variable que no pertenece a la función
            nonlocal tabla_DEPENDENCIA

            for dato in datos:
                tabla_DEPENDENCIA.insert("", "end", values=(dato[1], dato[3]))

            conn.close()

        # creamos el formulario a completar para poder realizar la búsqueda
        # Crear un marco para los controles
        marco_controles = tk.Frame(informes, padx=10, pady=10)
        marco_controles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Marco que contiene los cuadros de texto para ingresar datos a nuestra base de datos con respecto a informes
        marco_formulario_organigrama = tk.Frame(marco_controles)
        marco_formulario_organigrama.pack(fill=tk.BOTH, expand=True)

        label_titulo = tk.Label(marco_formulario_organigrama, text="SALARIOS TOTALES INFORME EXTENDIDO",
                                fg="orangered", font="Calibri 15")
        label_titulo.grid(row=1, column=0, columnspan=2)

        label_dep = tk.Label(marco_formulario_organigrama, text="DEPENDENCIA JEFE: ")
        label_dep.grid(row=2, column=0, sticky=tk.E)
        entry_dep = tk.Entry(marco_formulario_organigrama)
        entry_dep.grid(row=2, column=1, pady=10)

        # Crear un marco para el recuadro de los botones
        marco_recuadro = tk.Frame(marco_controles, bd=1, relief=tk.RAISED, bg="lightgray")
        marco_recuadro.pack(fill=tk.BOTH, expand=True)

        # Crear una etiqueta encima del recuadro de botones
        label_recuadro = tk.Label(marco_recuadro, text="Controles", font=("Helvetica", 10, "bold"), bg="lightgray")
        label_recuadro.pack(pady=5)

        # Crear un marco para los botones
        marco_botones = tk.Frame(marco_recuadro, bg="lightgray")
        marco_botones.pack(padx=5, pady=5, fill=tk.Y, expand=True)

        # Crear los botones
        boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", bg_color="lightgray", command=mostrar_salarios_extendido())
        boton_buscar.grid(row=1, column=0, padx=5, pady=5)

        boton_ver_dependencias = ctk.CTkButton(marco_botones, text="DEPENDENCIAS DISPONIBLES", bg_color="lightgray",
                                               command=ver_dependencias_disponibles)
        boton_ver_dependencias.grid(row=2, column=0, padx=5, pady=5)

        # etiqueta para comunicar al usuario que la tabla muestra las personas disponibles por dependencias
        e_tiqueta_informes_personasdependencias = tk.Label(informes, text="INFORME COMPLETO", anchor="center",
                                                           bg="salmon")
        e_tiqueta_informes_personasdependencias.pack(fill=tk.X, expand=True, padx=0, pady=0)

        # Crear la tabla informes por dependencia
        tabla_informe = ttk.Treeview(informes, columns=("TOT_SAL", "CANT_PERSONAL", "DEPENDENCIA"))
        tabla_informe.column("#0", width=0, stretch=tk.NO)
        tabla_informe.heading("TOT_SAL", text = "TOTAL DE SALARIO")
        tabla_informe.column("TOT_SAL",width= 500)
        tabla_informe.heading("CANT_PERSONAL", text = "CANTIDAD DE PERSONAL")
        tabla_informe.column("CANT_PERSONAL", width= 500)
        tabla_informe.heading("DEPENDENCIA", text = "DEPENDENCIA")
        tabla_informe.column("DEPENDENCIA", width= 500)
        tabla_informe.pack(fill=tk.BOTH, expand=True)

        # etiqueta para comunicar al usuario que lo que está viendo es sobre las dependencias disponibles
        e_tiqueta_informes_dependencias = tk.Label(informes, text="DEPENDENCIAS DISPONIBLES", bg="salmon")
        e_tiqueta_informes_dependencias.pack(fill=tk.X, expand=True, padx=0, pady=0)

        # Crear la tabla que nos muestra las depencencias disponibles con su respectiva organización
        tabla_DEPENDENCIA = ttk.Treeview(informes, columns=("DEPENDENCIAS DISPONIBLES", "ORGANIZACIÓN"))
        tabla_DEPENDENCIA.column("#0", width=0, stretch=tk.NO)
        tabla_DEPENDENCIA.heading("DEPENDENCIAS DISPONIBLES", text="DEPENDENCIAS DISPONIBLES")
        tabla_DEPENDENCIA.heading("ORGANIZACIÓN", text="ORGANIZACIÓN")
        tabla_DEPENDENCIA.pack(fill=tk.BOTH, expand=True)

        # boton que activa una función para eliminar los frames y botones para crear un organigrama
        boton_Volver_marcocontroles = ctk.CTkButton(marco_controles, text="Volver", bg_color="lightgray",
                                                    command=lambda: cerrar_formularios(marco_controles, tabla_informe,
                                                                                       tabla_DEPENDENCIA,
                                                                                       e_tiqueta_informes_dependencias,
                                                                                       e_tiqueta_informes_personasdependencias,
                                                                                       ventana_informes))
        boton_Volver_marcocontroles.pack(side=tk.BOTTOM)

    informes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # declaramos una barra de opciones horizontal en la parte más alta de esta
    # en esa barra de opciones mostramos un boton que cierra la pestaña
    barra_opciones_informes = tk.Frame(informes, bg="misty rose")
    barra_opciones_informes.pack(fill=tk.X)
    boton_cerrar_informes = tk.Button(barra_opciones_informes, text="x", bg="red",
                                      command=lambda: cerrar_ventana("informes", boton_informes_menu), bd = 0, width= 4)
    boton_cerrar_informes.grid(row = 0, column= 0)


    # creamos un frame donde vivirán los botones de informes
    informesbotones = tk.Frame(informes)
    informesbotones.pack()

    boton_personal_dependencia = Boton_animado(informesbotones, 0, 2, 0, 20, "Personal por Dependencia", 4, "light salmon", "black",
        personal_por_dependencia, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")  # colorear
                # frame, width, height, posx, posy, text, columnspan, bg, fg, command, metodo_de_aparicion,
                 #color_cambiar, tipo_letra, padx, pady, relief, anchor):
    boton_personal_dependencia.boton.config(anchor = "center")
    boton_personal_dependencia.vincular_raton()
    boton_personal_dependencia.boton.pack(fill= tk.X, expand=True)

    boton_personalDep_extendido = Boton_animado(informesbotones, 0, 2, -33, 60, "Personal por Dependencia Extendido", 4, "light salmon", "black",
         personal_por_dep_ext, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")  # colorear
    boton_personalDep_extendido.boton.config(anchor = "center")
    boton_personalDep_extendido.vincular_raton()
    boton_personalDep_extendido.boton.pack(fill= tk.X, expand=True)

    boton_salario_dependencia = Boton_animado(informesbotones, 0, 2, -37, 100, "Salario por Dependencia", 4, "light salmon", "black",
           salario_por_dependencia, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")  # colorear
    boton_salario_dependencia.boton.config(anchor = "center")
    boton_salario_dependencia.vincular_raton()
    boton_salario_dependencia.boton.pack(fill= tk.X, expand=True)

    boton_salarioDep_extendido = Boton_animado(informesbotones, 0, 2, -45, 180, " Salario por Dependencia extendido", 4, "light salmon", "black",
                                               salario_extendido, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")  # colorear
    boton_salarioDep_extendido.boton.config(anchor = "center")
    boton_salarioDep_extendido.vincular_raton()
    boton_salarioDep_extendido.boton.pack(fill= tk.X, expand=True)

    boton_organigrama = Boton_animado(informesbotones, 0, 2, -50, 220, "Organigrama", 4, "light salmon", "black",
              "Comando", "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")  # colorear
    boton_organigrama.boton.config(anchor = "center")
    boton_organigrama.vincular_raton()
    boton_organigrama.boton.pack(fill= tk.X, expand=True)

def none():
    print("none")
# desde aquí empezamos con nuestro main
ventana = tk.Tk()  # generamos la ventana principal
ventana.geometry("1000x600")  # le damos un tamaño base
ventana.title("Editor de Organigramas")  # le agregamos un título a la ventana
ventana.config(bg="gray")  # primer color de la ventana               #colorear
                #color de la parte trasera del login

# Frames principales que van a aparecer en la ventana
organigramas = tk.LabelFrame(ventana, bg="misty rose", text="Organigramas", font="Arial 12") #colorear
                                        #color de la pestaña de organigramas
personas = tk.LabelFrame(ventana, bg="misty rose", text="Personas", font="Arial 12") #colorear
                                    #color de la pestanha de personas
informes = tk.LabelFrame(ventana, bg="misty rose", text="Informes", font="Arial 12") #colorear
                                    #color de la pestanha de informes

#Frame principal del login
login = tk.Frame(ventana, bg="light salmon", relief= "flat", bd = 5) #colorear
                                #color del fondo del frame login y de la letra de su título

"""Etiquetas que viven en el labelframe login"""
e_tiqueta_login_login = ttk.Label(login, text = "BIENVENIDOS A EL EDITOR DE ORGANIGRAMAS", font= "Roboto 18", foreground = "orange red", background="light salmon")
e_tiqueta_login_login.grid(row = 0, column= 0, columnspan= 2, pady = 20)

"""Etiqueta con el fondo de la pestaña de loguearse"""
logo = tk.PhotoImage(file = "The Valley.png") # imagen que se descarga en el paquete de descarga
logo.subsample(1,1)
e_tiqueta_fondo_login = tk.Label(ventana, image = logo, bd = 0)
e_tiqueta_fondo_login.place(x = 0, y = 0, relheight= 1.0, relwidth= 1.0)
e_tiqueta_fondo_login.lower()

"""Botón para acceder a las funcionalidades después de logearse"""
                                    # frame, width, height, posx, posy, text, columspan, bg, fg, command,
                                    # metodo_de_aparicion, color_cambiar, tipo_letra, padx, pady, relief
#frame en donde van a estar los botones de login
botones_login = tk.Frame(login, bg = "light salmon")
botones_login.grid(row = 3, column=0, columnspan= 2)

boton_accederapp_login = Boton_animado(botones_login, 20, 1, 0, 0, "ACCEDER", 1, "light salmon", "white", logueado,
                                       2, "salmon", "Roboto 12", 6, 10, "flat", "center") #colorear
boton_accederapp_login.vincular_raton()
boton_accederapp_login.grid()


login.pack(pady=50, expand=True)  # muestra el frame login en la ventana

"""Frame del menú"""
menu = tk.LabelFrame(ventana, bg="light salmon")  # declaramos un nuevo frame en donde van a vivir las opciones del menú
alto_ventana = ventana.winfo_height()  # esta variable nos va a ayudar a hacer más interactivo el tamaño de nuestro menú,
# es decir que se adapte a la ampliación de pantalla

menu.config(width=185, height=alto_ventana)  # configuramos el tamaño de nuestro menú

"""Etiquetas dentro del menú"""
e_tiqueta_nombremenu_menu = tk.Label(menu, text="Menú", font="Arial 17", bg="light salmon", fg="black",
                                     anchor="center", width=13, height=1)
e_tiqueta_nombremenu_menu.place(x=3, y=10)
"""Botones de acceso que se alojan en el menú"""
# creamos un frame donde vivirán estos botones, meramente por estética
menubotones = tk.Frame(menu)
menubotones.place(x=3, y=50)

# los botones del menú son especiales, así como este son parte de la clase         #colorear
# boton animado, para establecer su color base debes tener en cuenta los colores
# puestos en anteriores funciones
boton_organigramas_menu = Boton_animado(menubotones, 17, 2, 0, 20, "  ❑  Organigramas", 2, "light salmon", "black",
                                        ventana_organigrama, "pack", "salmon", "Roboto 13", 0, 0, "flat", "w")
                                        # frame, width, height, posx, posy, text, columspan, bg, fg, command,
                                        # metodo_de_aparicion, color_cambiar, tipo_letra, padx, pady, relief
                                        #los colores que vas a cambiar son bg, es el fondo por defecto, color_cambiar
                                        #es el color que adquiere cuando le pasamos el mouse por encima y fg es el color
                                        #de la letra
boton_organigramas_menu.vincular_raton()
boton_organigramas_menu.pack()

boton_personas_menu = Boton_animado(menubotones, 17, 2, -37, 100, "  👤   Personas", 2, "light salmon", "black",     #colorear
                                    ventana_personas, "place", "salmon", "Roboto 13", 0, 0, "flat", "w")
boton_personas_menu.vincular_raton()
boton_personas_menu.pack()

boton_informes_menu = Boton_animado(menubotones, 17, 2, -41, 140, "  📄   Informes", 2, "light salmon", "black",    #colorear
                                    ventana_informes, "place", "salmon", "Roboto 13", 0, 0, "flat", "w")
boton_informes_menu.vincular_raton()
boton_informes_menu.pack()

##Para el cuadro que aparece al cerrar la aplicacion (crear el evento)
ventana.protocol("WM_DELETE_WINDOW", Cerrar)

ventana.mainloop()  # método de tkinter para que la ventana no se cierre