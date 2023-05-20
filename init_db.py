import mysql.connector


def criar_banco():
    # paramentros para à conexão com o banco de dados
    bd_config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": ""
    }

    # criação do cursor
    conexao = mysql.connector.connect(**bd_config)
    cursor = conexao.cursor()

    cursor.execute("drop database if exists final")
    cursor.execute("create database if not exists final")
    cursor.execute("use final")

    # dicionário com as tabelas do banco
    tabelas = {"plano": """
    create table if not exists plano (
        cod_plano integer auto_increment,
        nome varchar(20) not null,
        valor float not null,
        duracao int not null,
        primary key (cod_plano)
    )
    """, "aluno": """
    create table if not exists aluno (
        matricula integer auto_increment,
        nome varchar(20) not null,
        telefone varchar(20),
        cod_plano integer,
        data_inicio date,
        primary key (matricula),
        foreign key (cod_plano) references plano(cod_plano)
    )
    """, "professor": """
    create table if not exists professor (
        cod_professor integer auto_increment,
        nome varchar(20) not null,
        primary key (cod_professor)
    )
    """, "treino": """
    create table if not exists treino (
        cod_treino integer auto_increment,
        cod_professor integer not null,
        matricula_aluno integer not null,
        nome_treino varchar(30) not null,
        dia_semana varchar(20) not null,
        primary key (cod_treino),
        foreign key (cod_professor) references professor(cod_professor),
        foreign key (matricula_aluno) references aluno(matricula)
    )
    """, "exercicio": """
    create table if not exists exercicio (
        cod_exercicio integer auto_increment,
        nome_exercicio varchar(30) not null,
        primary key (cod_exercicio)
    )
    """, "treino_exercicio": """
    create table if not exists treino_exercicio (
        cod_treino int not null,
        cod_exercicio int not null,
        n_series int not null,
        n_repeticoes int not null,
        primary key (cod_treino, cod_exercicio),
        foreign key (cod_treino) references treino(cod_treino),
        foreign key (cod_exercicio) references exercicio(cod_exercicio)
    )
    """}

    # Criação das tabelas no banco
    for i in tabelas:
        print(f"Criando a tabela {i}")
        cursor.execute(tabelas[i])

    return conexao


def cadastrar_aluno(conexao, nome_aluno, telefone='null'):
    cursor = conexao.cursor()
    sql = f'insert into aluno (nome, telefone) values ("{nome_aluno}", {telefone})'
    cursor.execute(sql)
    conexao.commit()
    print(f'Aluno {nome_aluno} cadastrado')


def cadastrar_professor(conexao, nome_professor):
    cursor = conexao.cursor()
    sql = f'insert into professor (nome) values ("{nome_professor}")'
    cursor.execute(sql)
    conexao.commit()
    print(f'Professor {nome_professor} cadastrado')


def cadastrar_exercicio(conexao, nome_exercicio):
    cursor = conexao.cursor()
    sql = f'insert into exercicio (nome_exercicio) values ("{nome_exercicio}")'
    cursor.execute(sql)
    conexao.commit()
    print(f'Exercicio {nome_exercicio} cadastrado')


def cadastrar_plano(conexao, nome_plano, valor, duracao):
    cursor = conexao.cursor()
    sql = f'insert into plano (nome, valor, duracao) values ("{nome_plano}", {valor}, {duracao})'
    cursor.execute(sql)
    conexao.commit()
    print(f'Plano {nome_plano} cadastrado')


def cadastrar_treino(conexao, cod_professor, matricula_aluno, nome_treino, dia_semana):
    cursor = conexao.cursor(buffered=True)
    sql = f"""insert into treino (cod_professor, matricula_aluno, nome_treino, dia_semana) values 
    ({cod_professor}, {matricula_aluno}, '{nome_treino}', '{dia_semana}')"""
    cursor.execute(sql)
    print(f'treino {nome_treino} cadastrado')
    id_treino = cursor.lastrowid
    print('agora adicione os exercicios ao seu treino!')
    while True:
        cursor.execute('select * from exercicio')
        print('esses são seus exercicios com o seu determinado id, digite o id para adicionar o exercicio, caso '
              'contrario informe 0 para sair')
        print(cursor.fetchall())
        n = int(input('infome o id do exercicio que vc deseja: '))
        if n == 0:
            break
        else:
            repeticoes = int(input('informe o número de repetições: '))
            series = int(input('informe o número de series: '))
            sql2 = f"""insert into treino_exercicio (cod_treino, cod_exercicio, n_series, n_repeticoes)
            values ({id_treino}, {n}, {series}, {repeticoes})"""
            cursor.execute(sql2)
            print('exercicio adicionado!')
    conexao.commit()


def excluir_treino(conexao, cod_treino):
    cursor = conexao.cursor()
    sql2 = f'delete from treino_exercicio where cod_treino={cod_treino}'
    sql = f'delete from treino where cod_treino={cod_treino}'
    cursor.execute(sql2)
    cursor.execute(sql)
    conexao.commit()
    print('treino excluido')


def criar_matricula(conexao, matricula, cod_plano, data_inicio):
    cursor = conexao.cursor()
    sql = f'update aluno set cod_plano={cod_plano}, data_inicio="{data_inicio}" where matricula={matricula}'
    cursor.execute(sql)
    conexao.commit()
    print('matricula executada')


def listar_treino(conexao, matricula):
    cursor = conexao.cursor(buffered=True)
    sql = f'select nome_treino from treino where matricula_aluno = {matricula}'
    cursor.execute(sql)
    print(cursor.fetchall())


def listar_exercicio(conexao, cod_treino):
    cursor = conexao.cursor(buffered=True)
    sql = f"""select nome_exercicio, n_series, n_repeticoes from exercicio
    join treino_exercicio on exercicio.cod_exercicio = treino_exercicio.cod_exercicio
    join treino on treino.cod_treino = treino_exercicio.cod_treino where treino.cod_treino={cod_treino}"""
    cursor.execute(sql)
    print(cursor.fetchall())


def mensalidade_atrasada(conexao):
    cursor = conexao.cursor(buffered=True)
    sql = """select aluno.nome from aluno join plano on aluno.cod_plano = plano.cod_plano where CURRENT_TIMESTAMP >
    DATE_ADD(aluno.data_inicio, INTERVAL plano.duracao DAY)"""
    cursor.execute(sql)
    print(cursor.fetchall())


def alunos_por_plano(conexao):
    cursor = conexao.cursor(buffered=True)
    sql = """select plano.nome, count(aluno.matricula) from plano join aluno on aluno.cod_plano = plano.cod_plano
    where CURRENT_TIMESTAMP < DATE_ADD(aluno.data_inicio, INTERVAL plano.duracao DAY) group by plano.cod_plano;"""
    cursor.execute(sql)
    print(cursor.fetchall())


def maior_lucro(conexao):
    cursor = conexao.cursor(buffered=True)
    sql = """select plano.nome, (count(aluno.matricula)*plano.valor) as faturamento from plano join aluno on 
    aluno.cod_plano = plano.cod_plano where CURRENT_TIMESTAMP < DATE_ADD(aluno.data_inicio, INTERVAL plano.duracao DAY) 
    group by plano.cod_plano order by faturamento desc;"""
    cursor.execute(sql)
    print(cursor.fetchone())


def faturamento_mensal(conexao):
    cursor = conexao.cursor(buffered=True)
    sql = """select sum(valor) from plano join aluno on aluno.cod_plano = plano.cod_plano 
    where CURRENT_TIMESTAMP < DATE_ADD(aluno.data_inicio, INTERVAL plano.duracao DAY);"""
    cursor.execute(sql)
    print(cursor.fetchone())
