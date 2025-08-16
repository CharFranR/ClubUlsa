from flask import Flask, render_template, request, redirect, jsonify
from db_ops import mostrar_registros, init_db
from datetime import datetime
import requests

import subprocess
import time

# Ejecutar comunicacion.py en paralelo
p = subprocess.Popen(['python', 'comunicacion.py'])

# Opcional: esperar unos segundos a que el servidor Flask arranque
time.sleep(2)


app = Flask(__name__)
db = init_db()
db.crear_tablas()

# Guardar los setpoints en variables globales
setTemp = 40
setNivel = 30

@app.route('/', methods=['GET', 'POST'])
def home():
    global setTemp, setNivel
    
    if request.method == 'POST':
        try:
            setTemp = int(request.form['setTemp'])
            setNivel = int(request.form['setNivel'])
            
            # Enviar la configuración a comunicacion.py
            requests.post("http://localhost:5001/config", json={
                'setTemp': setTemp,
                'setNivel': setNivel
            })
        except Exception as e:
            return f"Error al actualizar configuración: {e}", 500

    success, data = mostrar_registros(db)
    if not success:
        return f"Error: {data}", 500
    if data is None:
        return "Sin Data", 500

    return render_template('home.html', registros=data, setTemp=setTemp, setNivel=setNivel)

@app.route('/datos')
def datos():
    success, data = mostrar_registros(db)
    if not success:
        return jsonify({"error": data}), 500
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
