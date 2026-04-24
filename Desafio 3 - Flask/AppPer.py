from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

personas = []
contador_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gestión de Personas</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
        button { padding: 5px 10px; margin: 2px; }
        .edit { background: orange; }
        .delete { background: red; color: white; }
        .add { background: green; color: white; }
    </style>
</head>
<body>

<h2>Personas</h2>

<input id="dni" placeholder="DNI">
<input id="nombre" placeholder="Nombre">
<button class="add" onclick="agregar()">Agregar Nuevo</button>

<br><br>

<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>DNI</th>
            <th>NOMBRES</th>
            <th>ACCIONES</th>
        </tr>
    </thead>
    <tbody id="tabla"></tbody>
</table>

<script>
function cargar() {
    fetch('/personas')
    .then(res => res.json())
    .then(data => {
        let tabla = document.getElementById('tabla');
        tabla.innerHTML = '';
        data.forEach(p => {
            tabla.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.dni}</td>
                <td>${p.nombre}</td>
                <td>
                    <button class="edit" onclick="editar(${p.id})">Editar</button>
                    <button class="delete" onclick="eliminar(${p.id})">Remove</button>
                </td>
            </tr>`;
        });
    });
}

function agregar() {
    fetch('/personas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            dni: document.getElementById('dni').value,
            nombre: document.getElementById('nombre').value
        })
    }).then(() => cargar());
}

function eliminar(id) {
    fetch('/personas/' + id, {
        method: 'DELETE'
    }).then(() => cargar());
}

function editar(id) {
    let nuevoNombre = prompt("Nuevo nombre:");
    let nuevoDni = prompt("Nuevo DNI:");

    fetch('/personas/' + id, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            dni: nuevoDni,
            nombre: nuevoNombre
        })
    }).then(() => cargar());
}

cargar();
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/personas', methods=['GET'])
def listar():
    return jsonify(personas)

@app.route('/personas', methods=['POST'])
def agregar():
    global contador_id
    data = request.get_json()

    persona = {
        "id": contador_id,
        "dni": data.get('dni'),
        "nombre": data.get('nombre')
    }

    personas.append(persona)
    contador_id += 1

    return jsonify({"mensaje": "Agregado"})

@app.route('/personas/<int:id>', methods=['DELETE'])
def eliminar(id):
    global personas
    personas = [p for p in personas if p['id'] != id]
    return jsonify({"mensaje": "Eliminado"})

@app.route('/personas/<int:id>', methods=['PUT'])
def editar(id):
    data = request.get_json()
    for p in personas:
        if p['id'] == id:
            p['dni'] = data.get('dni')
            p['nombre'] = data.get('nombre')
    return jsonify({"mensaje": "Editado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)