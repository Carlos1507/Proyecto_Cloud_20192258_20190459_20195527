import paramiko

def execRemoto(command, host):
    username = "ubuntu"
    password = "ubuntu"
    client = paramiko.SSHClient()
    comandos = [". admin-openrc", command]
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, "5800", username,password
                       , key_filename="venv/headkey"
                       )
        
        _stdin, _stdout, _stderr = client.exec_command(comandos[0]+ " ; "+comandos[1])
        output = _stdout.read().decode().strip()
        error = _stderr.read().decode().strip()
        print(f"Comando ejecutado: {command}")
        print(f"Resultado: {output}")
        print(f"Error: {error}")
    except Exception as e:
        print(f"Error {str(e)}")
    finally:
        client.close()