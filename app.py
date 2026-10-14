from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
BANCO = "perfil.db"


@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # insert
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        email = request.form["email"]
        profissao = request.form["profissao"]
        hobbies = request.form["hobbies"]
        sobre = request.form["sobre"]
        foto = request.form["foto"]
        cursor.execute(
            """
                     INSERT INTO pessoas
                     (nome, idade, cidade, estado, email, profissao,hobbies, sobre, foto)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, idade, cidade, estado, email, profissao, hobbies, sobre, foto),
        )
        conn.commit()
        conn.close()
        return redirect("/")
    # select
    cursor.execute("select * from pessoas order by nome")
    pessoas = cursor.fetchall()
    conn.close()
    return render_template("index.html", pessoas=pessoas)


# ===== NOVA: rota de EXCLUIR =====
@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()
    # delete
    cursor.execute("delete from pessoas where id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# ===== NOVA: rota de EDITAR =====
# OBS: as rotas de editar/excluir usam a coluna "id" da tabela pessoas.
# <int:id> pega o número que vem na URL, ex: /editar/3
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # update
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        email = request.form["email"]
        profissao = request.form["profissao"]
        hobbies = request.form["hobbies"]
        sobre = request.form["sobre"]
        foto = request.form["foto"]
        cursor.execute(
            """UPDATE pessoas
               SET nome = ?, idade = ?, cidade = ?, estado = ?, email = ?,
               profissao = ?, hobbies = ?, sobre = ?, foto = ?
               WHERE id = ?
            """,
            (nome, idade, cidade, estado, email, profissao, hobbies, sobre, foto, id),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    # select de UMA pessoa só (fetchone em vez de fetchall)
    cursor.execute("select * from pessoas where id = ?", (id,))
    pessoa = cursor.fetchone()
    conn.close()
    # se o id não existir no banco, volta pra página inicial
    if pessoa is None:
        return redirect("/")
    return render_template("editar.html", pessoa=pessoa)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", debug=True)
