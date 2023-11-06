import paramiko

def execRemoto(command, host):
    username = "ubuntu"
    password = "ubuntu"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, "5800", username,password
                       #, key_filename="headnode"
                       )
        _stdin, _stdout, _stderr = client.exec_command(command)
        output = _stdout.read().decode().strip()
        print(f"Comando ejecutado: {command}")
        print(f"Resultado: {output}")
    except Exception as e:
        print(f"Error {str(e)}")
    finally:
        client.close()