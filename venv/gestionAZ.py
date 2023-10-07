import questionary
def zonasDisponibilidad(usuarioLog):

    choicesAZ = ["Opción 1: AZ1: Worker1\tAZ2:Worker2\tAZ3:Worker3",
                 "Opción 2: AZ1: Worker1 & Worker2\tAZ2:Worker3",
                 "Opción 3: AZ1: Worker1 & Worker2 & Worker3"]
    opcion = questionary.select("Seleccione la configuración de AZs", choices=choicesAZ).ask()
