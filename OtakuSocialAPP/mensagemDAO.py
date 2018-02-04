import psycopg2
import psycopg2.extras
from mensagem import Mensagem

class MensagemDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def enviar(self, mensagem: Mensagem):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO mensagem(texto, email_o, email_d, data) VALUES (%s, %s, %s, %s)', (mensagem.texto, mensagem.email_o, mensagem.email_d, mensagem.data))
        cursor.close()
        self.conexao.commit()

    def nomes_conversas(self, email):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT DISTINCT usuario.nome FROM mensagem, usuario WHERE email_o=(%s) AND email_d=usuario.email OR email_d=(%s) AND email_o=usuario.email", (email,email))
        nomes=list()
        for nome in cursor.fetchall():
            nomes.append(nome)
        cursor.close()
        return nomes

    def conversa(self, email_o, email_d):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT m.email_o, m.texto, m.email_d FROM mensagem as m WHERE m.email_o=(%s) and m.email_d=(%s) OR m.email_d=(%s) AND m.email_o=(%s) ORDER BY data', (email_o, email_d, email_o, email_d))
        conversa=list()
        for tupla in cursor.fetchall():
            conversa.append([tupla])
        cursor.close()
        return conversa

    def buscar_mesagem(self, email, palavra):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM mensagem WHERE email_o=(%s) AND texto LIKE '%(%s)%'", (email, palavra))
        cursor.close()

    def apagar_conversa(self, email_o, email_d):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM mensagem WHERE email_o=(%s) AND email_d=(%s)", (email_o, email_d,))
        cursor.close()
        self.conexao.commit()

    def apagar_todas_conversas(self, email):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM mensagem WHERE email_o=(%s)", (email,))
        cursor.close()
        self.conexao.commit()
