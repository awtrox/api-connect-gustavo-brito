import json
lista_usuarios = []
def abrir_arquivo():
    try:
        with open("data/database.json", "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Banco de dados inexistente ou corrompido, criando um novo")
        return []
    return usuarios

def recebe_dados(id, nome, email, status):
    return {"id": id, "nome": nome, "email": email, "status": status}

def escrever_arquivo(dados):
    with open("data/database.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def atualizar_arquivo(dados, usuario):
    dados.append(usuario)
    escrever_arquivo(dados)

def id_incremental(tabela):
    if not tabela:
        return 1
    else:
        return tabela[-1].get("id") + 1

def listar_usuarios():
    todos_usuarios = abrir_arquivo()
    if not todos_usuarios:
        return []
    return todos_usuarios if isinstance(todos_usuarios, list) else []

def criar_usuario(tabela, nome, email, status):
    if not nome or not email or not status:
        return 
    novo_usuario = recebe_dados(id_incremental(tabela), nome, email, status)
    atualizar_arquivo(tabela, novo_usuario)
    return novo_usuario

def validar_usuario(requisicao):
    if not requisicao or not isinstance(requisicao, dict):
        return {"error": "O corpo da requisição deve conter um json válido."}
    erros_encontrados = []
    if not requisicao.get("nome"):
        erros_encontrados.append("nome")
    if not requisicao.get("email"):
        erros_encontrados.append("email")
    if not requisicao.get("status"):
        erros_encontrados.append("status")
    if erros_encontrados:
        campos = ", ".join(erros_encontrados)
        return {"error": f"Campos obrigatorios ausentes: {campos}"}
    return None

def buscar_por_id(tabela, id_procurado):
    for i in tabela:
        if i.get("id") == id_procurado:
            return i
    return None
    
def atualizar_dados_usuario(usuario, requisicao):
    if requisicao.get("nome"):
        if usuario.get("nome") != requisicao.get("nome"):
            usuario["nome"] = requisicao.get("nome")
    if requisicao.get("email"):
        if usuario.get("email") != requisicao.get("email"):
            usuario["email"] = requisicao.get("email")
    if requisicao.get("status"):
        if usuario.get("status") != requisicao.get("status"):
            usuario["status"] = requisicao.get("status")
    return usuario

def delete(lista, id_procurado):
    for i in lista:
        if i.get("id") == id_procurado:
            lista.remove(i)
            break
    escrever_arquivo(lista)