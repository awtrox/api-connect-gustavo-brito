import pytest

def test_post_cria_usuario_e_retorna_201(client):
    corpo = {"nome": "Ana", "email": "ana@exemplo.com", "status": "ativo"}

    resp = client.post("/usuarios", json=corpo)

    assert resp.status_code == 201
    criado = resp.get_json()["data"]
    assert criado["id"] == 1
    assert criado["nome"] == "Ana"

@pytest.mark.parametrize("campo_faltando", ["nome", "email", "status"])
def test_post_sem_campo_obrigatorio_retorna_400(client, campo_faltando):
    corpo = {"nome": "Jorge", "email": "jorge@exemplo.com", "status": "ativo"}
    del corpo[campo_faltando]

    resp = client.post("/usuarios", json=corpo)
    assert resp.status_code == 400

def criar_usuario(client, nome, email, status):
    resp = client.post("/usuarios", json={"nome": nome, "email": email, "status": status})
    assert resp.status_code == 201
    return resp.get_json()["data"]

def test_get_lista_vazia_retorna_lista_vazia(client):
    resp = client.get("/usuarios")

    assert resp.status_code == 200
    assert resp.get_json() == {"data": []}

def test_get_lista_retorna_todos_os_produtos_criados(client):
    criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    criar_usuario(client, "Ana", "aninha@example.com", "Ativo")

    resp = client.get("/usuarios")

    assert resp.status_code == 200
    usuarios = resp.get_json()["data"]
    assert len(usuarios) == 2
    assert [n["nome"] for n in usuarios] == ["Jorge", "Ana"] 

def test_get_por_id_existente_retorna_200(client):
    criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    resp = client.get("/usuarios/1")
    assert resp.status_code == 200

def test_get_por_id_inexistente_retorna_404(client):
    resp = client.get("/usuarios/2")
    assert resp.status_code == 404

def test_post_caso_feliz_retorna_201(client):
    corpo = {"nome": "Joao", "email": "joao@example.com", "status": "Ativo"}
    resp = client.post("/usuarios", json = corpo)
    assert resp.status_code == 201

def test_post_nome_null_retorna_400(client):
    corpo = {"nome": None, "email": "joao@example.com", "status": "Ativo"}
    resp = client.post("/usuarios", json = corpo)
    assert resp.status_code == 400
    
def test_post_nome_vazio_retorna_400(client):
    corpo = {"nome": "     ", "email": "joao@example.com", "status": "Ativo"}
    resp = client.post("/usuarios", json = corpo)
    assert resp.status_code == 400

def test_post_nome_numerico_retorna_400(client):
    corpo = {"nome": 123, "email": "email@example.com", "status": "Ativo"}
    resp = client.post("/usuarios", json = corpo)
    assert resp.status_code == 400

def test_post_corpo_nao_json_retorna_400(client):
    resp = client.post("/usuarios", json="texto nao json")
    assert resp.status_code == 400

def test_put_atualiza_e_persiste(client):
    usuario = criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    resp = client.put(f"/usuarios/{usuario['id']}", json={"nome": "João", "email": "joao@example.com", "status": "Ativo"})
    resp = client.get(f"/usuarios/{usuario['id']}")
    assert resp.get_json()["data"] == {"id": usuario['id'], "nome": "João", "email": "joao@example.com", "status": "Ativo"}

def test_put_id_inexistente_retorna_404(client):
    usuario = criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    resp = client.put(f"/usuarios/{usuario['id'] + 1}", json={"nome": "João", "email": "joao@example.com", "status": "Ativo"})
    assert resp.status_code == 404

@pytest.mark.parametrize("campo_faltando", ["nome", "email", "status"])
def test_put_campo_em_branco_retorna_400(client, campo_faltando):
    usuario = criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    corpo = {"nome": "João", "email": "joao@exemplo.com", "status": "ativo"}
    corpo[campo_faltando] = ""
    resp = client.put(f"/usuarios/{usuario['id']}", json=corpo)
    assert resp.status_code == 400

def test_delete_retorna_204_sem_corpo(client):
    usuario = criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    url = f"/usuarios/{usuario['id']}"
    resp = client.delete(url)

    assert resp.status_code == 204
    assert resp.data == b""

def test_delete_e_apos_get_retorna_404(client):
    usuario = criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    client.delete(f"/usuarios/{usuario['id']}")
    resp = client.get(f"/usuarios/{usuario['id']}")

    assert resp.status_code == 404

def test_delete_em_id_inexistente_retorna_404(client):
    usuario = criar_usuario(client, "Jorge", "jorge@example.com", "Ativo")
    resp = client.delete(f"/usuarios/{usuario['id'] + 1}")

    assert resp.status_code == 404
