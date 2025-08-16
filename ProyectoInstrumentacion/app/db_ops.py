from db import Database
from datetime import datetime

def init_db():
    """Inicializa la conexión a la base de datos"""
    return Database()

def insertar_registro(db, temperatura, caudal,  nivel, posicion, paro,finalizado, fecha):
    try:
        query = """
        INSERT INTO registros (temperatura, caudal, nivel, posicion, paro, finalizado, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        # Convertimos fecha a datetime si es string
        fecha_parsed = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S') if fecha else None
        
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (temperatura, caudal, nivel, posicion, paro, finalizado, fecha_parsed))
                registro_id = cur.fetchone()[0]  # ya debería devolver el ID correctamente
                conn.commit()
                
        return (True, registro_id)
        
    except Exception as e:
        print(f"Error al insertar registro: {e}")
        return (False, None)
    
def eliminar_registro(db, registro_id):
    try:
        query = "DELETE FROM registros WHERE id = %s RETURNING nombre"
        
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (registro_id,))
                resultado = cur.fetchone()
                conn.commit()
                
                if resultado:
                    return (True, f"Registro '{resultado[0]}' (ID: {registro_id}) eliminado")
                return (False, "El registro no existe")
                
    except Exception as e:
        error_msg = f"Error al eliminar registro: {e}"
        print(error_msg)
        return (False, error_msg)

 
def eliminar_tabla_registros(db):
    try:
        with db.conectar() as conn:
            with conn.cursor() as cur:
                
                cur.execute("DROP TABLE IF EXISTS registros CASCADE")
                conn.commit()
                
        return (True, "Tabla 'registros' eliminada exitosamente")
        
    except Exception as e:
        error_msg = f"Error al eliminar tabla: {e}"
        print(error_msg)
        return (False, error_msg)


def mostrar_registros(db, filtro_id=None):
   
    try:
        query = """
        SELECT id, temperatura, caudal, nivel, posicion, paro, finalizado, fecha
        FROM registros
        ORDER BY fecha DESC
        """
        params = ()
            
        with db.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                registros = cur.fetchall()

                if not registros:
                    return (True, []) 

                column_names = [desc[0] for desc in cur.description]
                
                if not registros:
                    return (True, "No hay registros encontrados")
                
                resultados = []
                for reg in registros:
                    resultados.append(dict(zip(column_names, reg)))
                
                return (True, resultados)
                
    except Exception as e:
        return (False, f"Error al leer registros: {e}")