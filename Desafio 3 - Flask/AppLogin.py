from flask import Flask, request, jsonify

app = Flask(__name__)

# Usuario de prueba
USUARIO = "admin"
PASSWORD = "1234"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"error": "Completar usuario y contraseña"}), 400

    if usuario == USUARIO and password == PASSWORD:
        return jsonify({
            "mensaje": "Login exitoso ✅"
        })
    else:
        return jsonify({
            "error": "Usuario o contraseña incorrectos ❌"
        }), 401


@app.route('/')
def inicio():
    return "API Login funcionando 🚀"


if __name__ == '__main__':
    app.run(debug=True)