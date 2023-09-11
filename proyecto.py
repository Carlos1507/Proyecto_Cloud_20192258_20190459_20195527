# Definición de librerías y constantes

# Definición de las clases a implementar (elementos):
class virtualMachine:
    pass
class slice:
    pass
class user:
    pass

# Definición de los módulos a implementar:
def autorizacion():
    pass

# Definición de funciones adicionales a implementar:
def conexionBD():
    pass
def menu():
    opcion = ""
    print("What would you like to do today?")
    return opcion
# Función principal
if __name__ == "__main__":    
    print("Welcome to the Cloud Service: CGC (The Cloud Gods Carry)")
    print("Please enter your credentials to log in to the system: ")
    usuario = autorizacion()
    menu(usuario)