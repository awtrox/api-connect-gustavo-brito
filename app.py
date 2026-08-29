from flask import Flask, jsonify
from routes.usuarios_routes import usuarios_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(usuarios_bp)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "sucesso",
        "mensagem": "Servidor de API iniciado com sucesso",
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)