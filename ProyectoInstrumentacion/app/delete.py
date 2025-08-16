# limpiar_db.py
from db import Database

def limpiar_tabla():
    db = Database()
    
    try:
        # Conecta a la base de datos
        with db.conectar() as conn:
            with conn.cursor() as cur:
                # Borra la tabla si existe
                cur.execute("DROP TABLE IF EXISTS registros CASCADE")
                
                # Recrea la tabla
                cur.execute("""
                    CREATE TABLE registros (
                        id SERIAL PRIMARY KEY,
                        temperatura VARCHAR(10) NOT NULL,
                        caudal VARCHAR(10) NOT NULL,
                        nivel VARCHAR(10) NOT NULL,
                        paro VARCHAR(10),
                        posicion VARCHAR(10),
                        finalizado VARCHAR(10),
                        fecha TIMESTAMP NOT NULL
                    )
                """)
                
                conn.commit()
                print("Tabla 'registros' eliminada y recreada exitosamente")
                
    except Exception as e:
        print(f"Error al limpiar la tabla: {e}")

if __name__ == "__main__":
    limpiar_tabla()
