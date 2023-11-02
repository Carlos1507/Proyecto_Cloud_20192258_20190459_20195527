import pymysql, paramiko
from sshtunnel import SSHTunnelForwarder

# Detalles de la conexión SSH
ssh_host = '10.20.10.221'
ssh_port = 5800
ssh_user = 'ubuntu'
ssh_password = 'ubuntu'
# ssh_key_path = 'venv/headnode'

# Detalles de la conexión MySQL a través del túnel SSH
mysql_port = 4000
mysql_user = 'root'
mysql_password = 'cloud2023'
mysql_database = 'cloud'
mysql_hostname = "127.0.0.1"

def ejecutarSQLRemoto(sql, params):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      #  ssh_client.connect(ssh_host, ssh_port, ssh_user, key_filename=ssh_key_path)
        ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
        with SSHTunnelForwarder((ssh_host, ssh_port), ssh_username=ssh_user,ssh_password=ssh_password,
                                remote_bind_address=(mysql_hostname, mysql_port),) as tunnel:
            mysql_conn = pymysql.connect(
                host=mysql_hostname, port=tunnel.local_bind_port,
                user=mysql_user, password=mysql_password,
                database=mysql_database,
            )
            handlermysql = mysql_conn.cursor()
            if params is not None:
                handlermysql.execute(sql, params)
            else:
                handlermysql.execute(sql)
            if (("select" in sql) or ("SELECT" in sql)):  
                resultados = handlermysql.fetchall()
                return resultados
            else:     
                mysql_conn.commit()
            mysql_conn.close()
        ssh_client.close()
    except Exception as e:
        print(f"Error: {str(e)}")


def ejecutarSQLlocal(sql, params):
    try:
        mysqlConexion = pymysql.connect(host=mysql_hostname, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_database, charset="utf8mb4")
        handlermysql = mysqlConexion.cursor()
        if params is not None:
            handlermysql.execute(sql, params)
        else:
            handlermysql.execute(sql)
        if (("select" in sql) or ("SELECT" in sql)):  
            resultados = handlermysql.fetchall()
            return resultados
        else:     
            mysqlConexion.commit()
        mysqlConexion.close()
    except pymysql.Error as e:
        print("Error al realizar el cambio:", e)
