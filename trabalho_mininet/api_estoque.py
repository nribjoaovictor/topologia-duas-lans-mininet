from flask import Flask, request, jsonify

app = Flask(__name__)

produtos = {
    "P001": {
        "id": "P001",
        "quantidade": 10,
        "descricao": "Mouse Gamer",
        "preco": 99.90
    }
}


@app.route("/")
def home():
    return jsonify({"mensagem": "API Estoque-Produtos funcionando"})


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(list(produtos.values()))


@app.route("/produtos/<id>", methods=["GET"])
def buscar_produto(id):
    produto = produtos.get(id)

    if not produto:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    return jsonify(produto)


@app.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.get_json()

    if not dados or "id" not in dados:
        return jsonify({"erro": "Campo id obrigatorio"}), 400

    produtos[dados["id"]] = {
        "id": dados["id"],
        "quantidade": dados.get("quantidade", 0),
        "descricao": dados.get("descricao", ""),
        "preco": dados.get("preco", 0.0)
    }

    return jsonify(produtos[dados["id"]]), 201


@app.route("/produtos/<id>", methods=["PUT"])
def atualizar_produto(id):
    if id not in produtos:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    dados = request.get_json()

    produtos[id]["quantidade"] = dados.get("quantidade", produtos[id]["quantidade"])
    produtos[id]["descricao"] = dados.get("descricao", produtos[id]["descricao"])
    produtos[id]["preco"] = dados.get("preco", produtos[id]["preco"])

    return jsonify(produtos[id])


@app.route("/produtos/<id>", methods=["DELETE"])
def deletar_produto(id):
    if id not in produtos:
        return jsonify({"erro": "Produto nao encontrado"}), 404

    produto = produtos.pop(id)

    return jsonify({
        "mensagem": "Produto removido com sucesso",
        "produto": produto
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)