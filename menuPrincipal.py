import questionary
from colorama import Fore, Style, init
from Operador.moduloOperadorGestionUsuarios import gestionarUsuarios as gestionUsuarios
from Operador.moduloOperadorGestionSlices import gestionarSlices as gestionSlices
from Operador.moduloOperadorGestionImagenes import gestorImagenes as gestionImagenes
from Operador.moduloOperadorGestionFlavors import gestorFlavors
from Usuario.moduloUsuarioGestionSlices import gestionarSlicesUsuario as gestionSlicesUsuario
from Operador.moduloOperadorGestionAZ import zonasDisponibilidad
from Usuario.moduloUsuarioCrearSlices import crearSlice

def menu(usuarioLog, endpointBase):
    if(usuarioLog.rol==1):    # ACCIONES OPERADOR
        opcionesMenu = ["1. Gestionar Usuarios", "2. Gestionar Slices","3. Zonas de Disponibilidad","4. Gestión de Imágenes","5. Configurar flavors","Cerrar Sesión"]
    else:                     # ACCIONES USUARIO
        opcionesMenu = ["1. Crear Slice","2. Listar Slices","Cerrar Sesión"]
    nombreRol = "OPERADOR" if usuarioLog.rol==1 else "USUARIO"
    print(Fore.CYAN+"================= MENÚ PRINCIPAL "+nombreRol+" =================")
    opcion = questionary.select("¿Qué acción desea hacer hoy?", choices=opcionesMenu).ask()
    
    if(opcion == "Cerrar Sesión"):
        return
    else:
        if(usuarioLog.rol==1):    # MENÚ OPERADOR
            menuOperador(usuarioLog, opcion, endpointBase)
        elif(usuarioLog.rol==2):  # MENÚ USUARIO
            menuUsuario(usuarioLog, opcion, endpointBase)

def menuOperador(usuarioLog, opcion, endpointBase):
    if(opcion=="1. Gestionar Usuarios"):
        # Módulo gestionar usuarios
        print("Módulo gestionar usuarios")
        while True:
            opt = gestionUsuarios(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="2. Gestionar Slices"):
        # Módulo gestionar slices
        print("Módulo gestionar slices")
        while True:
            opt = gestionSlices(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="3. Zonas de Disponibilidad"):
        # Módulo definir zonas de disponibilidad
        print("Módulo definir zonas de disponibilidad")
        while True:
            opt = zonasDisponibilidad(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="4. Gestión de Imágenes"):
        # Módulo gestionar imágenes
        print("Módulo gestionar imágenes")
        while True:
            opt = gestionImagenes(endpointBase)
            if opt==None: break
    elif(opcion=="5. Configurar flavors"):
        # Módulo configurar flavors
        print("Módulo configurar flavors")
        while True:
            opt = gestorFlavors(endpointBase)
            if opt==None: break
    menu(usuarioLog, endpointBase)
    
def menuUsuario(usuarioLog, opcion, endpointBase):
    if(opcion=="1. Crear Slice"):
        print("Módulo crear Slice")
        while True:
            opt = crearSlice(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="2. Listar Slices"):
        print("Módulo listar/editar/borrar slice")
        while True:
            opt = gestionSlicesUsuario(usuarioLog, endpointBase)
            if opt==None: break
    menu(usuarioLog, endpointBase)