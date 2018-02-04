import psycopg2
from publicacao import Publicacao


class Usuario():
    def __init__(self, nome, email, data_nascimento, profissao=''):
        self.nome=nome
        self.email=email
        self.data_nascimento=data_nascimento
        self.profissao=profissao

    def publicar(self, texto, local='', email_amigo=''):
        publi = Publicacao(self.email, texto)
        return publi

    def set_profissao(self, nova_profissao):
        self.profissao = nova_profissao

    def listar_dados(self):
        return 'Nome: ' + str(self.nome) + ', ' + 'Email: ' + str(self.email) + ', ' + 'Data de Nascimento: '+ str(self.data_nascimento) +', '+ 'Profissão: '+str(self.profissao)


    '''class Minha_conta:
        def __init__(self, email, senha):
            self.email = email
            self.senha = senha

        def set_senha(self, nova_senha):
            self.senha = nova_senha'''


