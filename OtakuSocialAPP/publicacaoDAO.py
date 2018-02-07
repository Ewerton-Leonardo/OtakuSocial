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

    def publicar(self, publicacao: Publicacao):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM publicacao WHERE email_user=(%s) AND texto=(%s)', (publicacao.email_user, publicacao.texto))
        publicacao: Publicacao = self.__montar_objeto_publicacao(cursor.fetchone())
        return publicacao

    def remover(self, numero_publi):
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM publicacao WHERE numero_publi=(%s)',(numero_publi,))
        cursor.close()
        self.conexao.commit()

    def __montar_objeto_publicacao(self, tupla):
        return Publicacao(tupla['texto'], tupla['email_user'])
