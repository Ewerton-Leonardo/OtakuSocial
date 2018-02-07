import psycopg2
import psycopg2.extras
class SistemaDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir_login(self, email, senha):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO login(email, senha) VALUES (%s, %s)", (email, senha))
        self.conexao.commit()

    def fazer_login(self, email, senha):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * from login WHERE email=(%s)', (email,))
        for tupla in cursor.fetchall():
            if str(tupla['senha']) == senha:
                return True
            else:
                return False
