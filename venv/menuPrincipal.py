import questionary
from gestionUsuariosOperador import gestionarUsuarios as gestionUsuarios
from gestionSlicesOperador import gestionarSlices as gestionSlices

def menu(usuarioLog):
    if(usuarioLog.rol==1):    # ACCIONES OPERADOR
        opcionesMenu = ["1. Usuarios", "2. Slices", "3. Cerrar Sesión"]
    else:                     # ACCIONES USUARIO
        opcionesMenu = ["1. Crear Slice","2. Listar Slices","3. Definir zona de disponibilidad","4. Imágenes","5. Cerrar Sesión"]
    opcion = questionary.select("¿Qué acción desea hacer hoy?", choices=opcionesMenu).ask()
    
    if(opcion == "3. Cerrar Sesión" or opcion == "5. Cerrar Sesión"):
        return
    else:    
        if(usuarioLog.rol==1):    # MENÚ OPERADOR
            menuOperador(usuarioLog, opcion)
        elif(usuarioLog.rol==2):  # MENÚ USUARIO
            menuUsuario(usuarioLog, opcion)

def menuOperador(usuarioLog, opcion):
    if(opcion=="1. Usuarios"):
        # Módulo gestionar usuarios
        while True:
            opt = gestionUsuarios(usuarioLog)
            if opt==None:
                break
    else:
        # Módulo gestionar slices
        while True:
            opt = gestionSlices(usuarioLog)
            if opt==None:
                break
    menu(usuarioLog)
def menuUsuario(usuarioLog, opcion):
    if(opcion=="1. Crear Slice"):
        pass
    elif(opcion=="2. Listar Slices"):
        pass
    elif(opcion=="3. Definir zona de disponibilidad"):
        pass
    else:
        pass