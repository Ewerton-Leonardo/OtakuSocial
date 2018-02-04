import psycopg2
import psycopg2.extras
from publicacao import Publicacao

class publicacaoDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, publicacao: Publicacao):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO publicacao(email_user, texto) VALUES (%s, %s)', (publicacao.email_user, publicacao.texto))
        cursor.close()
        self.conexao.commit()

    '''def editar_texto(self, novo_texto):
        cursor = self.conexao.cursor()
        cursor.execute('UPDATE TABLE publicacao SET texto = ))
        cursor.close()
        self.conexao.commit()'''

    def remover(self, numero_publi):
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM publicacao WHERE numero_publi='+ str(numero_publi))
        cursor.close()
        self.conexao.commit()
