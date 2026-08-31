# API RESTful de Gestão de Usuários

Esta é uma API REST desenvolvida em Python com o framework Flask para o gerenciamento de usuários. O projeto implementa um CRUD completo e utiliza manipulação em memória com persistência em arquivo JSON, mantendo uma arquitetura modular focada na Separação de Responsabilidades (SoC).

## Funcionalidades

* **Cadastro (POST):** Inserção de novos registros com validação rigorosa de campos obrigatórios (nome, e-mail, status).
* **Listagem e Busca (GET):** Retorno de todos os registros ou busca específica parametrizada por ID na URL.
* **Atualização (PUT):** Modificação de dados de um usuário existente, suportando atualização parcial de campos.
* **Exclusão (DELETE):** Remoção segura de registros do sistema com tratamento de erro para IDs inexistentes.
* **Respostas Padronizadas:** Respostas HTTP determinísticas utilizando os envelopes `"data"` para sucesso e `"error"` para falhas, com status codes apropriados (200, 201, 204, 400, 404).

## Tecnologias e Ferramentas

* **Linguagem:** Python 3
* **Framework Web:** Flask (utilizando Blueprints para roteamento)
* **Persistência:** JSON estático local (`data/database.json`)
* **Testes de API:** Thunder Client

## Arquitetura do Projeto

O código está estruturado para isolar a camada de rede da lógica de negócios:
* `app.py`: Ponto de entrada, configuração do servidor e registro de Blueprints.
* `routes/`: Camada de roteamento responsável por interceptar requisições HTTP e repassar dados extraídos.
* `controllers/`: Núcleo da lógica de negócios, validações estruturais e algoritmos de busca/atualização na memória.
* `data/`: Armazenamento físico do banco de dados simulado.

## Como Executar Localmente

1. Clone o repositório para a sua máquina.
2. Crie e ative um ambiente virtual na raiz do projeto:
   ```bash
   python -m venv .venv
   
   # Para ativar no Windows:
   .venv\Scripts\activate
   
   # Para ativar no Linux/Mac:
   source .venv/bin/activate
   ```
3. Instale o framework Flask:
   ```bash
   pip install flask
   ```
4. Inicie o servidor:
   ```bash
   python app.py
   ```
5. O servidor estará escutando em `http://127.0.0.1:3000`.

##  Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/usuarios` | Retorna a lista de todos os usuários. |
| `GET` | `/usuarios/<id>` | Retorna os detalhes de um usuário específico. |
| `POST` | `/usuarios` | Cadastra um novo usuário. |
| `PUT` | `/usuarios/<id>` | Atualiza os dados de um usuário existente. |
| `DELETE` | `/usuarios/<id>` | Remove um usuário específico. |