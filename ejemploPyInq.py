import questionary
import pymysql, paramiko

# Configura los detalles de la conexión MySQL a través del túnel SSH
mysql_port = 3306
mysql_user = 'grupo2'
mysql_password = 'cloud2023'
mysql_database = 'cloud'
mysql_hostname = "127.0.0.1"


questionary.text("What's your first name").ask()
passwd = questionary.password("What's your secret?").ask()
print("The password is", passwd)
responseConfirm = questionary.confirm("Are you amazed?").ask()
print("The confirmation is", responseConfirm)
questionary.select(
    "What do you want to do?",
    choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
).ask()

questionary.rawselect(
    "What do you want to do?",
    choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
).ask()

opcionesSelected = questionary.checkbox(
    "Select toppings", choices=["foo", "bar", "bazz"]
).ask()

questionary.path("Path to the projects version file").ask()



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
