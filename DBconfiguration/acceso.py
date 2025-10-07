import psycopg2
import getpass

# Configuración de conexión a la base de datos en Docker
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = 'Admin'
DB_PASSWORD = "p4ssw0rdDB"

def conectar_db():
    """Conecta a la base de datos PostgreSQL y retorna la conexión."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None


def obtener_datos_usuario(username, password):
    #Consulta la base de datos para obtener los datos de un usuario a partir de sus credenciales.
    conn = conectar_db()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return
    try:
        cursor = conn.cursor()
        # Verificar si el usuario y contraseña existen en la tabla credenciales
        query = """
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
        FROM credenciales c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
        else:
            print("\nUsuario o contraseña incorrectos.")
            # Cerrar la conexión
            cursor.close()
            conn.close()
    except Exception as e:
        print("Error al consultar la base de datos:", e)

#función de insersión de usuario.
def insertar_usaurio(nombre, correo, telefono, fecha_nacimiento, username, password_hash):
    #Inserta un nuevo usuario en la base de datos.
    conn = conectar_db()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return #terminarnos la función si no hay conexión.
    
    #manejamos la excepción en caso de error.
    try:
        cursor = conn.cursor() #inicializamos el cursor.

        # Crear una nueva entrada en la tabla usuarios mediante una query externa ya que se me hace más sencillo modificar así en caso de que me equivoque.
        insertar_usuario = """
        INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
        VALUES (%s, %s, %s, %s) RETURNING id_usuario;
        """
        cursor.execute(insertar_usuario, (nombre, correo, telefono, fecha_nacimiento))
        id_usuario = cursor.fetchone()[0] # Obtener el id_usuario generado, primer elemento de la tupla.

        # Insertar en la tabla credenciales

        # Query externa para insertar en la tabla credenciales.
        insertar_credenciales = """
        INSERT INTO credenciales (id_usuario, username, password_hash)
        VALUES (%s, %s, %s);
        """

        #pasamos el id del usuario recien creado, el nombre y la contraseña.
        cursor.execute(insertar_credenciales, (id_usuario, username, password_hash))

        # Confirmar los cambios
        conn.commit()
        print("\nUsuario insertado correctamente :)")

    except Exception as e:
        print("Error al insertar en la base de datos:", e)
        #deshacemos lo que hicimos
        conn.rollback()
    finally:
        #cerramos todo si no está hecho ya.
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
def actualizar_correo(id_usuario, nuevo_correo):
    #Actualiza el correo de un usuario solicitnado ID.
    conn = conectar_db()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return
    try:
        cursor = conn.cursor()
        # Query para actualizar el correo del usuario, gusto personal ponerla afuera.
        actualizar_query = """
        UPDATE usuarios
        SET correo = %s
        WHERE id_usuario = %s;
        """
        cursor.execute(actualizar_query, (nuevo_correo, id_usuario))
        conn.commit()
        print("\nCorreo actualizado correctamente.")
    except Exception as e:
        print("Error al actualizar el correo:", e)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def borrar_usuario(id_usuario):
    #Borra un usuario de la base de datos a partir de su ID.
    conn = conectar_db()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return
    try:
        cursor = conn.cursor()
        # Primero borrar las credenciales asociadas al usuario.
        borrar_credenciales_query = """
        DELETE FROM credenciales
        WHERE id_usuario = %s;
        """
        cursor.execute(borrar_credenciales_query, (id_usuario,))
        
        # Luego borrar el usuario.
        borrar_usuario_query = """
        DELETE FROM usuarios
        WHERE id_usuario = %s;
        """
        cursor.execute(borrar_usuario_query, (id_usuario,))
        
        conn.commit()
        print("\nUsuario borrado correctamente.")
    except Exception as e:
        print("Error al borrar el usuario:", e)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def menu_inicial():
    print("\nSeleccione una opción:")
    print("1. Iniciar sesión")
    print("2. Insertar nuevo usuario")
    print("3. Actualizar correo de usuario")
    print("4. Borrar usuario.")
    print("5. Salir")
    opcion = input("Ingrese el número de la opción deseada: ")
    return opcion



if __name__ == "__main__":
    #print("Inicio de sesión en la base de datos")
    # Solicitar credenciales al usuario
    #user = input("Ingrese su usuario: ")
    #pwd = getpass.getpass("Ingrese su contraseña: ")#No muestra la contraseña a escribir
    #Consultar base de datos
    #obtener_datos_usuario(user, pwd)
    #TODO: Implementar insertar usuario mediante una función.
    #TODO: actualizar correo.
    #TODO: borrar usuario.
    while True:
        opcion = menu_inicial()
        if opcion == '1':
            # Inicio de sesión, primer opción
            user = input("Ingrese su usuario: ")
            pwd = getpass.getpass("Ingrese su contraseña: ")
            obtener_datos_usuario(user, pwd)
        elif opcion == '2':
            #segunda, insertar nuevo usuario.
            print("\nInsertar nuevo usuario:")
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")
            fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD): ")
            usuario = input("Usuario: ")
            password = getpass.getpass("Contraseña: ")
            insertar_usaurio(nombre, correo, telefono, fecha_nacimiento, usuario, password)
        elif opcion == '3':
            #opción tres, actualizar correo.
            print("\nActualizar correo de usuario:")
            try:
                id_usuario = int(input("Ingrese el ID del usuario: "))
                nuevo_correo = input("Ingrese el nuevo correo: ")
                actualizar_correo(id_usuario, nuevo_correo)
            except ValueError:
                print("ID inválido. Debe ser un número entero.")
        elif opcion == '4':
            #opción cuatro, borrar usuario.
            print("\nBorrar usuario:")
            try:
                id_usuario = int(input("Ingrese el ID del usuario a borrar: "))
                #TODO: pedir confirmación.
                confirmacion = input("¿Está seguro de que desea borrar el usuario? (s/n): ")
                if confirmacion.lower() == 's':
                    borrar_usuario(id_usuario)
            except ValueError:
                #TODO: validar que solo ingrese números enteros.
                print("ID inválido. Debe ser un número entero.")
        elif opcion == '5':
            #bye bye
            print("Saliendo del programa.")
            break
        else:
            #TODO: mejorar solo insertar opciones validas.
            print("Opción no válida. Intente de nuevo.")


