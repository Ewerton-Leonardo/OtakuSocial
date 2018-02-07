import psycopg2
import psycopg2.extras
from url import URL

class UrlDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, site: URL):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO url(nome, url) VALUES (%s, %s)', (site.nome, site.url))
        cursor.close()
        self.conexao.commit()

    def buscar(self, nome):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM url WHERE nome LIKE %(%s)%', nome)
        for tupla in cursor.fetchall():
            return self.__montar_objeto_site(tupla)

    def __montar_objeto_site(self, tupla):
        return URL(tupla['nome'], tupla['url'])
