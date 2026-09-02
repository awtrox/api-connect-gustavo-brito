from flask import Blueprint, jsonify, request
from controllers.usuarios_controller import escrever_arquivo, listar_usuarios, criar_usuario, validar_usuario, buscar_por_id, validar_dados_atualizacao, atualizar_dados_usuario, delete

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    lista = listar_usuarios()
    return jsonify({"data": lista}), 200

@usuarios_bp.route('/usuarios', methods=['POST'])
def inserir_usuarios():
    dados_requisicao = request.get_json(silent=True)
    lista_usuarios = listar_usuarios()
    erro_validacao = validar_usuario(dados_requisicao)
    if erro_validacao:
        return jsonify(erro_validacao), 400
    usuario_criado = criar_usuario(lista_usuarios, dados_requisicao.get("nome"), dados_requisicao.get("email"), dados_requisicao.get("status"))
    return jsonify({"data": usuario_criado}), 201

@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    lista = listar_usuarios()
    usuario = buscar_por_id(lista, id)
    if usuario is None:
        return jsonify({"error": "usuário não encontrado."}), 404
    return jsonify({"data": usuario}), 200

@usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario_existente(id):
    dados_requisicao = request.get_json(silent=True)
    lista = listar_usuarios()
    usuario = buscar_por_id(lista, id)
    if usuario is None:
        return jsonify({"error": "usuário não encontrado."}), 404
    erro_validacao = validar_dados_atualizacao(dados_requisicao)
    if erro_validacao:
        return jsonify(erro_validacao), 400
    usuario = atualizar_dados_usuario(usuario, dados_requisicao)
    escrever_arquivo(lista)
    return jsonify({"data": usuario}), 200

@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    lista = listar_usuarios()
    usuario_existe = buscar_por_id(lista, id)
    if usuario_existe is None:
        return jsonify({"error": "usuario não encontrado."}), 404
    delete(lista, id)
    return jsonify(), 204