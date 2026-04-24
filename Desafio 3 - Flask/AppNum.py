from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/numero-texto', methods=['GET'])
def numero_a_texto():
    num = request.args.get('numero')

    if not num:
        return jsonify({"error": "Falta el número"}), 400

    if not num.isdigit():
        return jsonify({"error": "Debe ser un número entero positivo"}), 400

    num = int(num)

    if num < 0 or num > 999:
        return jsonify({"error": "Solo números entre 0 y 999"}), 400

    unidades = ["cero","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve"]
    especiales = ["diez","once","doce","trece","catorce","quince",
                  "dieciséis","diecisiete","dieciocho","diecinueve"]
    decenas = ["","","veinte","treinta","cuarenta","cincuenta",
               "sesenta","setenta","ochenta","noventa"]
    centenas = ["","ciento","doscientos","trescientos","cuatrocientos",
                "quinientos","seiscientos","setecientos","ochocientos","novecientos"]

    def convertir(n):
        if n < 10:
            return unidades[n]
        elif n < 20:
            return especiales[n-10]
        elif n < 30:
            if n == 20:
                return "veinte"
            return "veinti" + unidades[n-20]
        elif n < 100:
            if n % 10 == 0:
                return decenas[n//10]
            return decenas[n//10] + " y " + unidades[n%10]
        elif n == 100:
            return "cien"
        else:
            if n % 100 == 0:
                return centenas[n//100]
            return centenas[n//100] + " " + convertir(n % 100)

    texto = convertir(num)

    return jsonify({
        "numero": num,
        "texto": texto
    })

if __name__ == '__main__':
    app.run(debug=True)