from flask import Flask, render_template, request, redirect
from db_ops import init_db, mostrar_registros, insertar_registro, eliminar_tabla_registros
from ops import verificar_ruta, obtener_tamanio, copiar_a_documentos
from datetime import datetime

app = Flask(__name__)
db = init_db()
db.crear_tablas()

@app.route('/', methods=['GET', 'POST'])

def home():
    success, data = mostrar_registros(db)
    
    if not success:
        return f"Error: {data}", 500
    
    if data == None:
        return f"Sin Data", 500
        
    registros = data if isinstance(data, list) else []

    return render_template('home.html', registros=data)

@app.route('/procesar', methods=['GET', 'POST'])
def procesar_formulario():
    direccion = request.form.get('direccion')
    acciones = request.form.getlist('accion') 

    validar = verificar_ruta(direccion)
    if not validar:
        return "Ruta no válida", 400
    
    accion_str = ", ".join(acciones) if acciones else "ninguna"
    
    tamanio = obtener_tamanio(direccion)
    tipo = "archivo"
    nombre = "ImagenPrueba.jpg"

    resultado = insertar_registro(
        db=db,
        nombre=nombre,
        tipo=tipo,
        tamanio=tamanio,
        accion= accion_str,
        direccion=direccion,
        fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    if resultado[0]:  # Si fue exitoso
        realizar_respaldo(direccion)
        return redirect('/')  # Recarga la página principal
    else:
        return f"Error al guardar: {resultado[1]}", 400

def realizar_respaldo(direccion):
    copiar = copiar_a_documentos(direccion, "respaldo")

    if not copiar:
        return f"Error al copiar", 400

@app.route('/borrar_registros',  methods=['GET', 'POST'])
def borrar_registros():
    eliminar = eliminar_tabla_registros(db)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)