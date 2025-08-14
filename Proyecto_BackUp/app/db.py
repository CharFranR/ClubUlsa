import psycopg2
from psycopg2 import OperationalError

class Database:

    def __init__(self):
        self.conn_params = {
            'host': 'db',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'mydatabase',
            'port': '5432'
        }



    def conectar (self):
        try:
            return psycopg2.connect(**self.conn_params) 
        except OperationalError as e:
            print(f"Error de conexión: {e}") 
            return None
        



    def crear_tablas (self):
        """Crea la tabla registros si no existe"""
        command = """
        CREATE TABLE IF NOT EXISTS registros (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            tamanio VARCHAR(100) NOT NULL,
            accion VARCHAR(13) NOT NULL CHECK (accion IN ('respaldo', 'recuperacion')),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            direccion VARCHAR (50)
        )
        """
    
        try:
            conn = self.conectar()
            if conn:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(command)
                        print("Tabla 'registros' creada exitosamente")
                        return True
            return False
        except Exception as e:
            print(f"Error al crear tabla: {e}")
            return False
