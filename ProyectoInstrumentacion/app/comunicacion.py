from flask import Flask, request, jsonify
from db_ops import init_db, insertar_registro
from datetime import datetime

db = init_db()
app = Flask(__name__)

# Variables globales para setpoints
setTemp = 40
setNivel = 30

@app.route('/insertar', methods=['POST'])
def insertar():
    try:
        data = request.json
        temperatura = str(data['temperatura'])
        caudal = str(data['caudal'])
        nivel = str(data['nivel'])
        posicion = str(data['posicion'])
        paro = str(data['paro'])
        finalizado = str(data['finalizado'])
        fecha = data.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        success, registro_id = insertar_registro(
            db, temperatura, caudal, nivel, posicion, paro, finalizado, fecha
        )

        return jsonify({'success': success, 'id': registro_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Nueva ruta para recibir config desde main.py
@app.route('/config', methods=['POST'])
def actualizar_config():
    global setTemp, setNivel
    try:
        data = request.json
        setTemp = int(data['setTemp'])
        setNivel = int(data['setNivel'])
        return jsonify({'success': True, 'setTemp': setTemp, 'setNivel': setNivel})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Ruta para que esp32.py consulte la config
@app.route('/config', methods=['GET'])
def obtener_config():
    return jsonify({'setTemp': setTemp, 'setNivel': setNivel})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
