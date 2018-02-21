import psycopg2
import psycopg2.extras
from datetime import *
from evento import Evento

class EventoDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, evento: Evento):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO evento(nome, tema, local, data, hora_ini, hora_fim) VALUES (%s, %s, %s, %s, %s, %s)', (evento.nome, evento.tema, evento.local, evento.data, evento.hora_ini, evento.hora_fim))
        cursor.close()
        self.conexao.commit()

    def listar(self):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM evento WHERE data >= (%s) ORDER BY data', (datetime.today(),))
        lista = list()
        for tupla in cursor.fetchall():
            lista.append(self.__montar_objeto_evento(tupla))
        cursor.close()
        return lista

    def listar_passados(self):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM evento WHERE data <= (%s) ORDER BY data DESC', (datetime.today(),))
        lista = list()
        for tupla in cursor.fetchall():
            lista.append(self.__montar_objeto_evento(tupla))
        cursor.close()
        return lista



    def __montar_objeto_evento(self, tupla):
        return Evento(tupla['nome'], tupla['tema'], tupla['local'], tupla['data'], tupla['hora_ini'], tupla['hora_fim'])
