import psycopg2
import psycopg2.extras
from url import URL

class UrlDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, site: URL):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO url(url, nome) VALUES (%s, %s)', (site.url, site.nome))
        cursor.close()
        self.conexao.commit()

    def buscar(self, nome):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM url WHERE nome LIKE %(%s)%', (nome,))
        for tupla in cursor.fetchall():
            return self.__montar_objeto_site(tupla)
        cursor.close()

    def listar(self):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT nome FROM url')
        lista = list()
        for tupla in cursor.fetchall():
            lista.append(tupla['nome'])
        cursor.close()
        return lista

    def listar_nome(self,nome):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM url WHERE nome LIKE (%s)", (nome,))
        lista=list()
        for tupla in cursor.fetchall():
            lista.append(self.__montar_objeto_site(tupla))
        cursor.close()
        return lista

    def __montar_objeto_site(self, tupla):
        return URL(tupla['url'], tupla['nome'])
