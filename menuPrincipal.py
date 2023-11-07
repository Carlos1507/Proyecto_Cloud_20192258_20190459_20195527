import questionary
from Operador.moduloOperadorGestionUsuarios import gestionarUsuarios as gestionUsuarios
from Operador.moduloOperadorGestionSlices import gestionarSlices as gestionSlices
from Operador.moduloOperadorGestionImagenes import gestorImagenes as gestionImagenes

from Usuario.moduloUsuarioGestionSlices import gestionarSlicesUsuario as gestionSlicesUsuario
from Operador.moduloOperadorPlataforma import seleccionarPlataforma
from Operador.moduloOperadorGestionAZ import zonasDisponibilidad
from Usuario.moduloUsuarioCrearSlices import crearSlice

def menu(usuarioLog, endpointBase):
    if(usuarioLog.rol==1):    # ACCIONES OPERADOR
        opcionesMenu = ["1. Usuarios", "2. Slices","3. Definir zona de disponibilidad", "4. Selección plataforma","5. Imágenes","6. Definir flavors","Cerrar Sesión"]
    else:                     # ACCIONES USUARIO
        opcionesMenu = ["1. Crear Slice","2. Listar Slices","Cerrar Sesión"]
    opcion = questionary.select("¿Qué acción desea hacer hoy?", choices=opcionesMenu).ask()
    
    if(opcion == "Cerrar Sesión"):
        return
    else:
        if(usuarioLog.rol==1):    # MENÚ OPERADOR
            menuOperador(usuarioLog, opcion, endpointBase)
        elif(usuarioLog.rol==2):  # MENÚ USUARIO
            menuUsuario(usuarioLog, opcion, endpointBase)

def menuOperador(usuarioLog, opcion, endpointBase):
    if(opcion=="1. Usuarios"):
        # Módulo gestionar usuarios
        print("Módulo gestionar usuarios")
        while True:
            opt = gestionUsuarios(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="2. Slices"):
        # Módulo gestionar slices
        print("Módulo gestionar slices")
        while True:
            opt = gestionSlices(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="3. Definir zona de disponibilidad"):
        # Módulo definir zonas de disponibilidad
        print("Módulo definir zonas de disponibilidad")
        while True:
            opt = zonasDisponibilidad(usuarioLog, endpointBase)
            if opt==None: break
    elif(opcion=="4. Selección plataforma"):
        # Módulo selección plataforma
        print("Módulo selección plataforma")
        while True:
            opt = seleccionarPlataforma(endpointBase)
            if opt==None: break
    elif(opcion=="5. Imágenes"):
        # Módulo gestionar imágenes
        print("Módulo gestionar imágenes")
        while True:
            opt = gestionImagenes(endpointBase)
            if opt==None: break
    else:
        # Módulo definir flavors
        print("Módulo definir flavors")
        while True:
            opt = None
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