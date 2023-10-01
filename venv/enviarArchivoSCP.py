import subprocess

def enviarSCP(local_file, remote_username, remote_host, remote_directory, port, private_key):
    command = [
        'scp',
        '-P', str(port),
        '-i', private_key,
        local_file,
        f'{remote_username}@{remote_host}:{remote_directory}'
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Archivo {local_file} enviado con éxito a {remote_host}:{remote_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error al enviar el archivo: {e}")