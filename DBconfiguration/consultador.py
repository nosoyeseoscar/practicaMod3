import psycopg2

#se crea la conexion a la base de datos
conexion = psycopg2.connect(
    host ="localhost",
    port = "5432",
    database = "credenciales",
    user = "Admin",
    password = "p4ssw0rdDB"
)

#creamos el cursor.
cursor = conexion.cursor()


#Creamos una consulta
cursor.execute("SELECT * FROM usuarios")
#sacamos todo
registros = cursor.fetchall()

for fila in registros:
    print(fila)

cursor.close()
conexion.close()