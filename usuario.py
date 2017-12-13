import psycopg2
from publicacao import Publicacao


class Usuario():
    def __init__(self, nome, email, data_nascimento, profissao=''):
        self.nome=nome
        self.email=email
        self.data_nascimento=data_nascimento
        self.profissao=profissao
        self.list_amigos=list()
        self.publicacoes=dict()

    def publicar(self, texto, local='', email_amigo=''):
        publis = self.publicacoes.keys()
        cod_publi = len(publis) + 1
        publi = Publicacao(self.email, texto, local='', email_amigo='')
        publi.dados_publi[cod_publi]=['Código: ' + str(cod_publi), 'Texto: ' + str(texto), 'Local: ' + str(local),
                                      'Amigo: ' + str(email_amigo)]
        self.publicacoes[cod_publi] = [publi.dados_publi]

    def set_profissao(self, nova_profissao):
        self.profissao = nova_profissao

    def listar_dados(self):
        return 'Nome: ' + str(self.nome) + ', ' + 'Email: ' + str(self.email) + ', ' + 'Data de Nascimento: '+ str(self.data_nascimento) +', '+ 'Profissão: '+str(self.profissao)

    def desfazer_amizade(self, email_amigo):
        for amigo in self.list_amigos:
            if amigo.email == email_amigo:
                self.list_amigos.remove(amigo)

    def listar_amigos(self):
        for amigo in self.list_amigos:
            return 'Nome: ' + str(amigo.nome) + ', '+ 'Email: ' + str(amigo.email_user)

    '''class Minha_conta:
        def __init__(self, email, senha):
            self.email = email
            self.senha = senha

        def set_senha(self, nova_senha):
            self.senha = nova_senha'''


