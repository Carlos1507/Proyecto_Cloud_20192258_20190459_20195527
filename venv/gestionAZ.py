import questionary, requests, json

def zonasDisponibilidad(usuarioLog, endpointBase):
    opcion1 = "Plan 1: AZ1: Worker1  AZ2:Worker2  AZ3:Worker3"
    opcion2 = "Plan 2: Worker1 & Worker2 AZ2:Worker3"
    opcion3 = "Plan 3: AZ1: Worker1 & Worker2 & Worker3"
    choicesAZ = [opcion1, opcion2, opcion3]
    opcion = questionary.select("Seleccione la configuración de AZs", choices=choicesAZ).ask()
    if(opcion==opcion1):
        AZs = ["Worker1", "Worker2", "Worker3"]
        payload = {"azs": AZs}
        response = requests.post(url = endpointBase+"/guardarAZs", 
                                headers = {"Content-Type": "application/json"}, 
                                data= json.dumps(payload))
    elif(opcion==opcion2):
        AZs = ["Worker1 & Worker2", "Worker3"]
        payload = {"azs": AZs}
        response = requests.post(url = endpointBase+"/guardarAZs", 
                                headers = {"Content-Type": "application/json"}, 
                                data= json.dumps(payload))
    else:
        AZs = ["Worker1 & Worker2 & Worker3"]
        payload = {"azs": AZs}
        response = requests.post(url = endpointBase+"/guardarAZs", 
                                headers = {"Content-Type": "application/json"}, 
                                data= json.dumps(payload))