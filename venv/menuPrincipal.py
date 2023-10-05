import questionary
from gestionUsuariosOperador import gestionarUsuarios as gestionUsuarios
from gestionSlicesOperador import gestionarSlices as gestionSlices
from gestionImagenes import gestorImagenes as gestionImagenes
from gestionSlicesUsuario import gestionarSlicesUsuario as gestionSlicesUsuario

def menu(usuarioLog, endpointBase):
    if(usuarioLog.rol==1):    # ACCIONES OPERADOR
        opcionesMenu = ["1. Usuarios", "2. Slices", "3. Cerrar Sesión"]
    else:                     # ACCIONES USUARIO
        opcionesMenu = ["1. Crear Slice","2. Listar Slices","3. Definir zona de disponibilidad","4. Imágenes","5. Cerrar Sesión"]
    opcion = questionary.select("¿Qué acción desea hacer hoy?", choices=opcionesMenu).ask()
    
    if(opcion == "3. Cerrar Sesión" or opcion == "5. Cerrar Sesión"):
        return
    else:    
        if(usuarioLog.rol==1):    # MENÚ OPERADOR
            menuOperador(usuarioLog, opcion, endpointBase)
        elif(usuarioLog.rol==2):  # MENÚ USUARIO
            menuUsuario(usuarioLog, opcion, endpointBase)

def menuOperador(usuarioLog, opcion, endpointBase):
    if(opcion=="1. Usuarios"):
        # Módulo gestionar usuarios
        while True:
            opt = gestionUsuarios(usuarioLog, endpointBase)
            if opt==None:
                break
    else:
        # Módulo gestionar slices
        while True:
            opt = gestionSlices(usuarioLog, endpointBase)
            if opt==None:
                break
    menu(usuarioLog, endpointBase)
def menuUsuario(usuarioLog, opcion, endpointBase):
    if(opcion=="1. Crear Slice"):
        pass
    elif(opcion=="2. Listar Slices"):
        while True:
            opt = gestionSlicesUsuario(usuarioLog, endpointBase)
            if opt==None:
                break
    elif(opcion=="3. Definir zona de disponibilidad"):
        pass
    else:
        while True:
            opt = gestionImagenes(endpointBase)
            if opt==None:
                break
    menu(usuarioLog, endpointBase)