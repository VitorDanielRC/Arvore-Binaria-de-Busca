from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Node:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

def construir_bst_balanceada(valores_ordenados):
    if not valores_ordenados:
        return None
    meio = len(valores_ordenados) // 2
    raiz = Node(valores_ordenados[meio])
    raiz.esquerda = construir_bst_balanceada(valores_ordenados[:meio])
    raiz.direita = construir_bst_balanceada(valores_ordenados[meio + 1 :])
    return raiz

def busca_bst(raiz, alvo):
    atual = raiz
    while atual:
        if alvo == atual.valor:
            return True
        elif alvo < atual.valor:
            atual = atual.esquerda
        else:
            atual = atual.direita
    return False

def node_to_dict(no):
    if no is None:
        return None
    return {
        "valor": no.valor,
        "esquerda": node_to_dict(no.esquerda),
        "direita": node_to_dict(no.direita),
    }

valores_unicos = []
raiz = None

def reconstruir(valores):
    global valores_unicos, raiz
    valores_unicos = sorted(set(valores))
    raiz = construir_bst_balanceada(valores_unicos)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/init", methods=["POST"])
def api_init():
    data = request.get_json(force=True)
    numeros = data.get("numeros", [])
    if not isinstance(numeros, list):
        return jsonify({"ok": False, "msg": "Formato inválido."}), 400
    try:
        nums = [int(x) for x in numeros]
    except ValueError:
        return jsonify({"ok": False, "msg": "Os valores devem ser inteiros."}), 400

    if not nums:
        nums = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]

    reconstruir(nums)
    return jsonify({
        "ok": True,
        "msg": "Árvore inicial construída e balanceada.",
        "valores": valores_unicos,
        "arvore": node_to_dict(raiz)
    })

@app.route("/api/inserir", methods=["POST"])
def api_inserir():
    data = request.get_json(force=True)
    v = data.get("valor", None)
    if v is None:
        return jsonify({"ok": False, "msg": "Informe um valor."}), 400
    try:
        n = int(v)
    except ValueError:
        return jsonify({"ok": False, "msg": "Valor deve ser inteiro."}), 400

    global valores_unicos
    if n in valores_unicos:
        return jsonify({
            "ok": False,
            "msg": "Valor já existe na árvore (não são permitidas duplicatas).",
            "valores": valores_unicos,
            "arvore": node_to_dict(raiz)
        })

    valores_unicos.append(n)
    reconstruir(valores_unicos)
    return jsonify({
        "ok": True,
        "msg": f"Valor {n} inserido. Árvore reconstruída balanceada.",
        "valores": valores_unicos,
        "arvore": node_to_dict(raiz)
    })

@app.route("/api/procurar_remover", methods=["POST"])
def api_procurar_remover():
    data = request.get_json(force=True)
    v = data.get("valor", None)
    if v is None:
        return jsonify({"ok": False, "msg": "Informe um valor."}), 400
    try:
        n = int(v)
    except ValueError:
        return jsonify({"ok": False, "msg": "Valor deve ser inteiro."}), 400

    global valores_unicos, raiz
    if not busca_bst(raiz, n):
        return jsonify({
            "ok": False,
            "msg": f"Valor {n} NÃO foi encontrado na árvore.",
            "valores": valores_unicos,
            "arvore": node_to_dict(raiz)
        })

    valores_unicos = [x for x in valores_unicos if x != n]
    reconstruir(valores_unicos)
    return jsonify({
        "ok": True,
        "msg": f"Valor {n} encontrado e removido. Árvore reequilibrada.",
        "valores": valores_unicos,
        "arvore": node_to_dict(raiz)
    })

@app.route("/api/remover", methods=["POST"])
def api_remover():
    data = request.get_json(force=True)
    v = data.get("valor", None)
    if v is None:
        return jsonify({"ok": False, "msg": "Informe um valor."}), 400
    try:
        n = int(v)
    except ValueError:
        return jsonify({"ok": False, "msg": "Valor deve ser inteiro."}), 400

    global valores_unicos
    if n not in valores_unicos:
        return jsonify({
            "ok": False,
            "msg": f"Valor {n} não pertence ao conjunto atual.",
            "valores": valores_unicos,
            "arvore": node_to_dict(raiz)
        })

    valores_unicos = [x for x in valores_unicos if x != n]
    reconstruir(valores_unicos)
    return jsonify({
        "ok": True,
        "msg": f"Valor {n} removido. Árvore reconstruída e balanceada.",
        "valores": valores_unicos,
        "arvore": node_to_dict(raiz)
    })

if __name__ == "__main__":
    app.run(debug=True)
