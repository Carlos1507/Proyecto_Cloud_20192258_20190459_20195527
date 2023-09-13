# Definición de librerías y constantes
from tkinter import *
from tkinter import ttk 
# Definición de las clases a implementar (elementos):
class virtualMachine:
    pass
class slice:
    pass
class user:
    pass

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
frm.Label(frm, text="Welcome to the Cloud Service: CGC (The Cloud Gods Carry)\nPlease enter your credentials to log in to the system: ")
frm.Button(frm,Text="Login", command=root.destroy).grid(column=1, row=0)
root.mainloop()

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
  #  print("Welcome to the Cloud Service: CGC (The Cloud Gods Carry)")
  #  print("Please enter your credentials to log in to the system: ")
  #  usuario = autorizacion()
  #  menu(usuario)
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Welcome to the Cloud Service: CGC (The Cloud Gods Carry)\nPlease enter your credentials to log in to the system: ").grid(column=0, row=0)
    ttk.Button(frm, text="Login", command=root.destroy).grid(column=1, row=0)
    root.mainloop()