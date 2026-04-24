from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/edad', methods=['GET'])
def calcular_edad():
    fecha_nacimiento = request.args.get('fecha')

    if not fecha_nacimiento:
        return jsonify({"error": "Falta la fecha"}), 400

    try:
        # Convertir string a fecha
        nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        hoy = datetime.today()

        # Calcular edad
        edad = hoy.year - nacimiento.year

        # Ajustar si todavía no cumplió años este año
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1

        return jsonify({
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad
        })

    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Usar YYYY-MM-DD"}), 400

if __name__ == '__main__':
    app.run(debug=True)