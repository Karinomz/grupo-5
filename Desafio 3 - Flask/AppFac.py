from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

TOPE_DOC = 10000

# =========================
# 🎨 INTERFAZ SIMPLE
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Facturador</title>
</head>
<body>
    <h2>Facturador</h2>

    <input id="monto" placeholder="Monto"><br><br>
    <input id="tipo_doc" placeholder="Tipo Doc"><br><br>
    <input id="nro_doc" placeholder="Nro Doc"><br><br>

    <button onclick="facturar()">Generar Factura</button>

    <pre id="resultado"></pre>
    <img id="qr" width="200">

<script>
function facturar() {
    fetch('/facturar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            monto: document.getElementById('monto').value,
            tipo_doc: document.getElementById('tipo_doc').value,
            nro_doc: document.getElementById('nro_doc').value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('resultado').innerText = data.error;
        } else {
            document.getElementById('resultado').innerText = data.ticket;
            document.getElementById('qr').src = "data:image/png;base64," + data.qr;
        }
    });
}
</script>
</body>
</html>
"""

# =========================
# 🏠 HOME
# =========================
@app.route('/')
def home():
    return render_template_string(HTML)

# =========================
# 🧾 FACTURAR
# =========================
@app.route('/facturar', methods=['POST'])
def facturar():
    data = request.get_json()

    try:
        monto = float(data.get('monto', 0))
    except:
        return jsonify({"error": "Monto inválido"}), 400

    tipo_doc = data.get('tipo_doc')
    nro_doc = data.get('nro_doc')

    if monto > TOPE_DOC and (not tipo_doc or not nro_doc):
        return jsonify({"error": "Se requiere documento para montos mayores a 10000"}), 400

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ticket = f"Factura\\nMonto: ${monto}\\nFecha: {fecha}\\nDoc: {nro_doc if nro_doc else 'N/A'}"

    # QR
    qr_data = f"{monto}|{fecha}|{nro_doc}"
    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return jsonify({
        "ticket": ticket,
        "qr": qr_base64
    })

# =========================
# ▶️ RUN
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)