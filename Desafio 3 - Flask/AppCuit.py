from flask import Flask, request, jsonify

app = Flask(__name__)

def calcular_cuil(dni, tipo=20):
    dni_str = str(dni)
    base = str(tipo) + dni_str

    multiplicadores = [5,4,3,2,7,6,5,4,3,2]

    suma = 0
    for i in range(10):
        suma += int(base[i]) * multiplicadores[i]

    resto = suma % 11

    if resto == 0:
        verificador = 0
    elif resto == 1:
        verificador = 9
    else:
        verificador = 11 - resto

    return f"{tipo}-{dni}-{verificador}"

@app.route('/cuil', methods=['GET'])
def obtener_cuil():
    dni = request.args.get('dni')

    if not dni:
        return jsonify({"error": "Falta el DNI"}), 400

    if not dni.isdigit():
        return jsonify({"error": "DNI inválido"}), 400

    cuil = calcular_cuil(dni)

    return jsonify({
        "dni": dni,
        "cuil": cuil
    })

if __name__ == '__main__':
    app.run(debug=True)