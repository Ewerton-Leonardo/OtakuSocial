import psycopg2
import psycopg2.extras
from usuario import Usuario
class usuarioDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, usuario: Usuario):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO usuario(nome, email, data_nascimento, profissao) VALUES (%s, %s, %s, %s)', (usuario.nome, usuario.email, usuario.data_nascimento, usuario.profissao))
        cursor.close()
        self.conexao.commit()

    def inserir_amigo(self, email_user, email_amigo):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * from usuario')
        tupla = cursor.fetchall()
        amigo = None
        for t in tupla:
            if t[1] == email_amigo:
                amigo = t
                cursor.execute('INSERT INTO amigos(email_user, nome, email_amigo, data_nascimento) VALUES (%s, %s, %s, %s)', (email_user, amigo[0], amigo[1], amigo[2]))
        if amigo == None:
            print('Email do amigo incorreto')
        cursor.close()
        self.conexao.commit()

    def buscar(self, email):
        # necessário cursor_factory=psycopg2.extras.DictCursor quando se quer trabalhar com a tupla em formato de dicionário.
        # Ex.: tupla['nm_conta']
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM usuario WHERE email='"+ str(email)+ "'")
        usuario: Usuario = self.__montar_objeto_usuario(cursor.fetchone())
        cursor.close()
        return usuario

    def buscar_amigo(self, nome):
        # necessário cursor_factory=psycopg2.extras.DictCursor quando se quer trabalhar com a tupla em formato de dicionário.
        # Ex.: tupla['nm_conta']
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM amigos WHERE nome like '"+ "%" + str(nome)+ "%" + "'")
        for tupla in cursor.fetchall():
            return 'Email: ' + str(tupla[2])
        cursor.close()

    def listar_amigos(self):
        cursor = self.conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM amigos')
        for tupla in cursor.fetchall():
            print('Nome: ' + str(tupla[1]), 'Email: ' + str(tupla[2]))
        cursor.close()


    def set_profissao(self, nova_profissao, email):
        cursor = self.conexao.cursor()
        cursor.execute("update usuario set profissao = '"+str(nova_profissao)+ "'" + " where email = '"+str(email)+"'")
        cursor.close()
        self.conexao.commit()

    def desfazer_amizade(self, email, email_amigo):
        cursor = self.conexao.cursor()
        cursor.execute("delete from amigos where email_user = '"+str(email)+"' and email_amigo = "+"'"+str(email_amigo)+"'")
        cursor.close()
        self.conexao.commit()

    def set_senha(self, email,  nova_senha):
        cursor = self.conexao.cursor()
        cursor.execute("update login set senha = '"+str(nova_senha)+ "'" + " where email = '"+str(email)+"'")
        cursor.close()
        self.conexao.commit()


    def __montar_objeto_usuario(self, tupla):
        return Usuario(tupla['nome'], tupla['email'], tupla['data_nascimento'], tupla['profissao'])
