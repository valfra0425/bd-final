from init_db import *

conexao = criar_banco()
# cadastrando alunos
cadastrar_aluno(conexao, nome_aluno='valmir')
cadastrar_aluno(conexao, 'amanda', '988787787')
cadastrar_aluno(conexao, 'wellyton', '988786788')
# cadastrando professor
cadastrar_professor(conexao, 'josé')
# cadastrando exercício
cadastrar_exercicio(conexao, 'flexão')
cadastrar_exercicio(conexao, 'cadeira flexora')
cadastrar_exercicio(conexao, 'leg press')
cadastrar_exercicio(conexao, 'desenvolvimento')
# cadastrando plano
cadastrar_plano(conexao, 'plano mensal', 40.00, 1)
cadastrar_plano(conexao, 'plano anual', 300.00, 12)
cadastrar_plano(conexao, 'plano trimensal', 75.00, 3)
# cadastrando treino
cadastrar_treino(conexao, 1, 1, 'treino de bicipes', 'segunda-feira')
cadastrar_treino(conexao, 1, 2, 'treino de perna', 'quinta-feira')
cadastrar_treino(conexao, 1, 1, 'treino de costas', 'terça-feira')
cadastrar_treino(conexao, 1, 1, 'treino de peitoral', 'sexta-feira')
# excluindo treino
excluir_treino(conexao, 1)
# matriculando alunos em um plano
criar_matricula(conexao, 1, 1, '2022-12-30')
criar_matricula(conexao, 2, 2, '2022-12-30')
criar_matricula(conexao, 3, 2, '2012-12-30')
# listar treinos de um aluno
listar_treino(conexao, 1)
# listar exercicios de um treino
listar_exercicio(conexao, 2)
# exibe os alunos com matricula atrasada
mensalidade_atrasada(conexao)
# exibe a quantidade de alunos com o plano ativo em cada curso
alunos_por_plano(conexao)
# exibe o plano com maior lucro
maior_lucro(conexao)
# exibe o faturamento mensal da academia
faturamento_mensal(conexao)
