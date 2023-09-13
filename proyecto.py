# Definición de librerías y constantes
import tkinter as tk
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
  #  print("Welcome to the Cloud Service: CGC (The Cloud Gods Carry)")
  #  print("Please enter your credentials to log in to the system: ")
  #  usuario = autorizacion()
  #  menu(usuario)
    root = tk.Tk()
    root.title("Cloud Service")

    # Mensajes iniciales
    mensaje_inicial = tk.Label(root, text="Welcome to the Cloud Service: CGC (The Cloud Gods Carry)", background="#80FF80")
    mensaje_inicial.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    mensaje_inicial_2 = tk.Label(root, text="Please enter your credentials to log in to the system:")
    mensaje_inicial_2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Usuario
    user_label = tk.Label(root, text="User:")
    user_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)

    username = tk.Entry(root)
    username.grid(row=4, column=1, padx=10, pady=10)

    # Contraseña
    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)

    password = tk.Entry(root, show="*")
    password.grid(row=5, column=1, padx=10, pady=10)

    # Botón de inicio de sesión
    login_button = tk.Button(root, text="Login", command=autorizacion)
    login_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()