from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from bd import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

mysql = MySQL()

mysql.init_app(app)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = "gerencia_projetos"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']

        conn = mysql.connect()
        cursor = conn.cursor()

        login_adm = validar_login_adm(cursor,user_name, password)
        login_gerente = validar_login_gerente(cursor,user_name, password)
        login_funcionario = validar_login_funcionario(cursor,user_name, password)

        cursor.close()
        conn.close()

        if login_adm:
            return redirect(url_for("listar_todos"))
        elif login_gerente:
            id_gerente = login_gerente[1][0]
            return redirect(url_for("listar_projetos", id=id_gerente))
        elif login_funcionario:
            id_funcionario = login_funcionario[1][0]
            return redirect(url_for("listar_atividades_funcionario", id_funcionario=id_funcionario))
        else:
            return redirect(url_for("index"))

##### FUNÇÕES DO ADM ######
@app.route("/adm")
def listar_todos():
    conn = mysql.connect()
    cursor = conn.cursor()

    gerentes = get_gerentes(cursor)
    funcionarios = get_funcionarios(cursor)

    return render_template("listar_pessoas.html", gerentes=gerentes, funcionarios=funcionarios)


# Rota para o formulário de inserção
@app.route("/adm/insert")
def inserir():
    return render_template("form_insert.html")


# Rota para inserir
@app.route("/adm/inserted", methods=["GET", "POST"])
def inserindo():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        nome = request.form["name"]
        email = request.form["email"]
        numero_contato = request.form["number"]
        data_nascimento = request.form["data_nascimento"]
        cpf = request.form["cpf"]
        cargo = request.form["opcao"]

        # Conectando no myslq e criando cursor
        conn = mysql.connect()
        cursor = conn.cursor()

        # Chamando função para inserir
        if cargo == 'Funcionário':
            insert_funcionario(cursor, conn, username, password, nome, email, numero_contato, data_nascimento, cpf)
        else:
            insert_gerente(cursor, conn, username, password, nome, email, numero_contato, data_nascimento, cpf)

        # Fechando a conexão e o cursor
        cursor.close()
        conn.close()

        # return para lista
        return redirect(url_for('listar_todos'))
    else:
        return redirect(url_for("inserir"))


# Função para mostrar o perfil gerente
@app.route("/adm/perfilg/<int:id>")
def perfil_gerente(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    perfil = get_perfil_gerente(cursor, id)
    nome = perfil[0][0]

    cursor.close()
    conn.close()

    return render_template("perfil_gerente.html", perfil=perfil, nome=nome)


# Função para mostar o perfil funcionario
@app.route("/adm/perfilf/<int:id>")
def perfil_funcionario(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    perfil = get_perfil_funcionario(cursor, id)
    nome = perfil[0][0]

    cursor.close()
    conn.close()

    return render_template("perfil_funcionario.html", perfil=perfil, nome=nome)


####FIM DAS FUNÇÕES ADM###
####FUNÇÕES DO GERENTE####

# Rota para listar os projetos do gerente
@app.route('/grt/<id>')
def listar_projetos(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    projetos = get_projetos(cursor, id)

    cursor.close()
    conn.close()
    return render_template("listar_projetos.html", projetos=projetos, id=id)


# Rota para listar os detalhes do projeto
@app.route("/grt/dtl/<int:id>/<int:id_projeto>")
def listar_detalhes(id,id_projeto):
    conn = mysql.connect()
    cursor = conn.cursor()
    detalhes = get_detalhes(cursor, id_projeto)
    funcionario = None
    if len(detalhes) == 0:
        pass
    else:
        funcionario = detalhes[0][4]

    cursor.close()
    conn.close()

    return render_template("listar_detalhes.html", detalhes=detalhes, id=id, func=funcionario, id_projeto=id_projeto)


# Rota para alterar o funcionário
@app.route("/grt/alt_func/<id>/<id_projeto>/<func>/<id_atividade>")
def alterar_funcionario(id,id_projeto,func, id_atividade):
    conn = mysql.connect()
    cursor = conn.cursor()

    funcionarios = get_nome_funcionarios(cursor)

    cursor.close()
    conn.close()

    return render_template("form_alt.html", funcionarios=funcionarios, func=func, id_projeto=id_projeto, id=id,
                           id_atividade=id_atividade)


# Rota para aplicar a alteração
@app.route("/grt/alter/<id>/<int:id_projeto>/<func>/<id_atividade>", methods=["GET", "POST"])
def aplicar_alteracao(id, id_projeto,func, id_atividade):
    if request.method == 'POST':
        funcionario = request.form['fun']

        conn = mysql.connect()
        cursor = conn.cursor()

        print(funcionario)

        alter_funcionario(cursor, conn, id_projeto, funcionario, func, id_atividade)

        cursor.close()
        conn.close()

        return redirect(url_for("listar_detalhes", id=id, id_projeto=id_projeto))


# Rota para mudar o status da atividade
@app.route("/grt/<id>/<int:id_projeto>/<id_atividade>")
def alter_status(id,id_projeto, id_atividade):
    print(id, id_projeto, id_atividade)
    conn = mysql.connect()
    cursor = conn.cursor()

    alter_status_atividade(cursor, conn, id_projeto, id_atividade)

    cursor.close()
    conn.close()

    return redirect(url_for("listar_detalhes", id=id, id_projeto=id_projeto))


# Rota para formulario de inserir atividade
@app.route("/grt/form_ativ/<id_gerente>/<id_projeto>")
def form_atividade(id_gerente ,id_projeto):
    conn = mysql.connect()
    cursor = conn.cursor()

    funcionarios = get_nome_funcionarios(cursor)

    cursor.close()
    conn.close()

    return render_template("form_atividade.html", funcionarios=funcionarios, id_projeto=id_projeto, id_gerente=id_gerente)


# Rota para inserir uma nova atividade
@app.route("/grt/insert_ativ/<id_gerente>/<id_projeto>", methods=['GET', 'POST'])
def insert_atividade(id_gerente,id_projeto):
    if request.method == 'POST':
        nome_atividade = request.form['nome_atividade']
        descricao = request.form['descricao']
        funcionario = request.form['fun']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']

        print(nome_atividade, '-',descricao, '-', funcionario, '-', data_inicio , '-', data_fim)

        conn = mysql.connect()
        cursor = conn.cursor()

        inserir_atividade(cursor, conn, id_projeto, nome_atividade, descricao, funcionario, data_inicio, data_fim)

        cursor.close()
        conn.close()

        return redirect(url_for("listar_detalhes", id=id_gerente, id_projeto=id_projeto))


# Rota para excluir uma atividade
@app.route("/grt/excluir_ativ/<id_gerente>/<id_projeto>/<id_atividade>")
def excluir_atividade(id_gerente,id_projeto,id_atividade):

    conn = mysql.connect()
    cursor = conn.cursor()

    excluir_atividade1(cursor, conn, id_atividade)

    cursor.close()
    conn.close()

    return redirect(url_for("listar_detalhes", id=id_gerente, id_projeto=id_projeto))


# Rota para o form de inserir projeto
@app.route("/grt/formProj/<id_gerente>")
def form_insert_projeto(id_gerente):
    return render_template("inserir_projeto.html", id_gerente=id_gerente)

# Rota para inserir um projeto
@app.route("/grt/insert_projeto/<id_gerente>", methods=['GET', 'POST'])
def inserir_projeto(id_gerente):
    if request.method == 'POST':
        nome_projeto = request.form['name_project']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']

        conn = mysql.connect()
        cursor = conn.cursor()

        inserir_projeto1(cursor, conn, id_gerente, nome_projeto, data_inicio, data_fim)

        projetos = get_projetos(cursor, id_gerente)

        return redirect(url_for("listar_projetos", projetos=projetos, id=id_gerente))


#######Fim das funções do gerente#######
######Início das funções do funcionário########


# Rota para listar as atividades do funcionário
@app.route("/func/<id_funcionario>")
def listar_atividades_funcionario(id_funcionario):
    conn = mysql.connect()
    cursor = conn.cursor()

    atividades = get_atividades_funcionario(cursor, id_funcionario)

    cursor.close()
    conn.close()

    return render_template("listar_atividades_funcionario.html", atividades=atividades)


# Rota para alterar o status da atividade
@app.route("/func/alter_status/<id_atividade>/<id_funcionario>")
def alterar_status_funcionario(id_atividade, id_funcionario):
    conn = mysql.connect()
    cursor = conn.cursor()

    alter_status_atividade_funcionario(cursor, conn, id_funcionario, id_atividade)

    return redirect(url_for("listar_atividades_funcionario", id_funcionario=id_funcionario))


if __name__ == "__main__":
    app.run(debug=True)
