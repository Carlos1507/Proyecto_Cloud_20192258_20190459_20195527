class virtualMachine:
    pass
class slice:
    pass
class user:
    pass
def conexionBD():
    pass
def autorizacion():
    pass
def menu():
    opcion = ""
    print("What would you like to do today?")
    return opcion

if __name__ == "__main__":    
    print("Welcome to the Cloud Service: CGC (The Cloud Gods Carry)")
    print("Please enter your credentials to log in to the system: ")
    usuario = autorizacion()
    menu(usuario)