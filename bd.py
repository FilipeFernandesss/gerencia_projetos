def validar_login_adm(cursor, user_name, password):
    cursor.execute(f'select id_login_adm from login_adm where user_name = "{user_name}" and password = "{password}";')
    id_adm = cursor.fetchone()

    if id_adm == None:
        return False
    else:
        return True


def validar_login_gerente(cursor, user_name, password):
    cursor.execute(f'select id_login_gerente from login_gerente where user_name = "{user_name}" and password = "{password}";')
    id_gerente = cursor.fetchone()

    if id_gerente == None:
        return False
    else:
        return (True, id_gerente)

def validar_login_funcionario(cursor, user_name, password):
    cursor.execute(f'select id_login_funcionario from login_funcionario F, info_funcionario FF where user_name = "{user_name}" and password = "{password}" and F.id_login_funcionario = FF.id_funcionario;')
    id_funcionario = cursor.fetchone()

    if id_funcionario == None:
        return False
    else:
        return (True, id_funcionario)


#Função para recuperar todos os gerentes
def get_gerentes(cursor):
    cursor.execute(f'SELECT Nome, Email, id_gerente FROM gerencia_projetos.info_gerente;')
    gerentes = cursor.fetchall()
    return gerentes


#Função para recuperar todos os funcionarios
def get_funcionarios(cursor):
    cursor.execute(f'SELECT Nome, Email, id_funcionario FROM gerencia_projetos.info_funcionario;')
    funcionarios = cursor.fetchall()
    return funcionarios


#Função para inserir um funcionario
def insert_funcionario(cursor, conn, username ,password, nome, email, numero_contato, data_nascimento, cpf):
    cursor.execute(f'insert into login_funcionario(user_name, password) values ("{username}", "{password}");')
    conn.commit()
    cursor.execute(f'insert into info_funcionario(Nome, Email, Número_Contato, Data_Nascimento, CPF) values ("{nome}", "{email}","{numero_contato}", "{data_nascimento}", "{cpf}");')
    conn.commit()


#Função para inserir um gerente
def insert_gerente(cursor, conn, username ,password, nome, email, numero_contato, data_nascimento, cpf):
    cursor.execute(f'insert into login_gerente(user_name, password) values ("{username}", "{password}");')
    conn.commit()
    cursor.execute(f'insert into info_gerente(Nome, Email, Número_Contato, Data_Nascimento, CPF) values ("{nome}", "{email}","{numero_contato}", "{data_nascimento}", "{cpf}");')
    conn.commit()

#Função para listar os perfis gerentes
def get_perfil_gerente(cursor, id):
    cursor.execute(f'SELECT Nome, Email, Número_Contato, Data_Nascimento, CPF FROM gerencia_projetos.info_gerente where id_gerente = "{id}";')
    perfil = cursor.fetchall()
    return perfil


#Função para listar os perfis funcionario
def get_perfil_funcionario(cursor, id):
    cursor.execute(f'SELECT Nome, Email, Número_Contato, Data_Nascimento, CPF FROM gerencia_projetos.info_funcionario where id_funcionario = "{id}";')
    perfil = cursor.fetchall()
    return perfil


#Função para recuperar os projetos de 1 gerente
def get_projetos(cursor, id):
    cursor.execute(f'Select nome, data_inicio, data_fim, id_projeto from projetos where id_gerente = "{id}";')
    projetos = cursor.fetchall()
    return projetos

#Função para detalhar o projeto
def get_detalhes(cursor, id_projeto):
    cursor.execute(f'SELECT A.nome, A.descricao, A.data_inicio, A.data_fim , F.Nome, A.concluido, A.id_atividade FROM gerencia_projetos.atividades A, gerencia_projetos.info_funcionario F, gerencia_projetos.projetos P where A.id_funcionario = F.id_funcionario and P.id_projeto = "{id_projeto}" and A.id_projeto = P.id_projeto ORDER BY A.id_atividade ASC;')
    detalhes = cursor.fetchall()
    return detalhes

#Função para recuperar o nome de todos os funcionarios.
def get_nome_funcionarios(cursor):
    cursor.execute(f'SELECT Nome FROM gerencia_projetos.info_funcionario;')
    funcionarios = cursor.fetchall()
    return funcionarios

#Função para alter o funcionario
def alter_funcionario(cursor, conn, id_projeto, nome_funcionario, func, id_atividade):
    cursor.execute(f'SELECT id_funcionario from info_funcionario where Nome="{nome_funcionario}";')
    id_func = cursor.fetchone()
    print(id_func[0])
    cursor.execute(f'update atividades set id_funcionario = "{id_func[0]}" where id_projeto = "{id_projeto}" and id_atividade = "{id_atividade}";')
    conn.commit()


#Função apra alter o status da atividade
def alter_status_atividade(cursor, conn, id_projeto, id_atividade):
    cursor.execute(f'update atividades set concluido = 0 where id_projeto = "{id_projeto}" and id_atividade = "{id_atividade}";')
    conn.commit()

#Função para inserir uma nova atividade
def inserir_atividade(cursor, conn,id_projeto, nome_atividade, descricao, nome_funcionario, data_inicio, data_fim):
    cursor.execute(f'SELECT id_funcionario from info_funcionario where Nome="{nome_funcionario}";')
    id_func = cursor.fetchone()
    cursor.execute(f'Insert into atividades (id_projeto, id_funcionario, nome, descricao, data_inicio, data_fim, concluido) values ("{id_projeto}","{id_func[0]}","{nome_atividade}", "{descricao}", "{data_inicio}", "{data_fim}", 0);')
    conn.commit()


#Função para excluir uma atividade
def excluir_atividade1(cursor, conn, id_atividade):
    cursor.execute(f'DELETE FROM `gerencia_projetos`.`atividades` WHERE (`id_atividade` = "{id_atividade}");')
    conn.commit()
    cursor.close()


#Função para recuperar as  atividades de um funcionario
def get_atividades_funcionario(cursor, id_funcionario):
    cursor.execute(f'SELECT F.id_funcionario, A.id_atividade, A.nome, A.descricao,A.data_inicio, A.data_fim, A.concluido'
                   f' from atividades A, info_funcionario F '
                   f'where F.id_funcionario = "{id_funcionario}" and F.id_funcionario = A.id_funcionario;')
    atividades = cursor.fetchall()
    return atividades


#Função para alter o status do funcionario pelo funcionario
def alter_status_atividade_funcionario(cursor, conn, id_funcionario, id_atividade):
    cursor.execute(f'update atividades set concluido = 0 where id_atividade = "{id_atividade}" and id_funcionario = "{id_funcionario}"; ')
    conn.commit()


