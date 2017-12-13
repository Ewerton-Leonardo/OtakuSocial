import psycopg2

conn = psycopg2.connect(host="localhost", database="otakusocial", user="postgres", password="ewerton")

cur = conn.cursor()

from usuario import Usuario
from usuarioDAO import usuarioDAO

class Sistema:
    def __init__(self):
        self.dic_dados_login = {}
        self.list_user  = list()
        conexao = psycopg2.connect(host="localhost", database="otakusocial", user="postgres", password="ewerton")
        self.usuarioDAO = usuarioDAO(conexao)

    def cadastrar_usuario(self, email, senha, nome,data_nascimento,profissao):
        self.dic_dados_login[email] = [senha]
        user = Usuario(nome,email,data_nascimento,profissao)
        self.usuarioDAO.inserir(user)
        cur.execute("INSERT INTO login(email, senha) VALUES (%s, %s)", (email, senha))
        conn.commit()

    def fazer_login(self, email, senha):
        cursor = self.usuarioDAO.conexao.cursor()
        cursor.execute('SELECT * FROM login')
        for tupla in cursor.fetchall():
            print(tupla[0], tupla[1])
            if str(tupla[0]) == str(email):
                if str(tupla[1]) == senha:
                    print('Usuário logado!')
                    self.menu_feed(email)
                else:
                    return False

            else:
                return False


    def menu_inicial(self):
        print('OtakuSocial')
        print('Menu Inicial')
        print('1 - Cadastrar usuário')
        print('2 - Fazer login')
        print('0 - Sair')
        opcao = int(input('Digite a opção:'))

        while opcao != 0:

            if opcao == 1:
                email = input('Digite seu e-mail:')
                for email1 in self.dic_dados_login.keys():
                    if email1 == email:
                        print('E-mail já cadastrado')
                        return opcao
                senha = input('Digite sua senha:')
                senha1 = input('Digite sua senha novamente:')
                if senha != senha1:
                    print('As senhas não conferem')
                    senha = input('Digite sua senha: ')
                    senha1 = input('Digite sua senha novamente: ')

                nome = input('Digite seu primeiro nome: ')
                data_nascimento = input('Digite sua data de nascimento, formato(DD/MM/AAAA): ')
                profissao = input('Digite sua profissão (opcional): ')
                self.cadastrar_usuario( email, senha, nome,data_nascimento,profissao)
                print('Usuário cadastrado com sucesso!')
            if opcao == 2:
                email = input('Digite seu e-mail: ')
                senha = input('Digite sua senha: ')
                cursor = self.usuarioDAO.conexao.cursor()
            cursor.execute('SELECT * FROM login')
            for tupla in cursor.fetchall():
                if str(tupla[0]) == str(email):
                    if str(tupla[1]) == senha:
                        self.menu_feed(email, senha)

            print('OtakuSocial')
            print('Menu Inicial')
            print('1 - Cadastrar usuário')
            print('2 - Fazer login')
            print('0 - Sair')
            opcao = int(input('Digite a opção: '))


        return opcao

    def menu_feed(self, email, senha):
        self.email=email
        self.user = self.buscar_usuario(email)
        print('FEED')
        print('1 - Publicar')
        print('2 - Adicionar amigo')
        print('3 - Buscar email de seu amigo')
        print('4 - Mudar profissão')
        print('5 - Listar minhas informações')
        print('6 - Desfazer amizade')
        print('7 - Listar amigos')
        print('8 - Alterar sua senha')
        print('9 - Sair')

        opcao1 = int(input('Digite a opção (feed): '))

        while opcao1 != 0:


            if opcao1 == 1:
                texto=input('Texto: ')
                local=input('Local: ')
                amigo=input('Amigo: ')
                self.user.publicar(texto,local,amigo)
                print(self.user.publicacoes)

            if opcao1 == 2:
                email_amigo=input('Digite o email da pessoa que deseja adicionar: ')
                self.usuarioDAO.inserir_amigo(self.email, email_amigo)

            if opcao1 == 3:
                nome_amigo = input('Digite o nome do seu amigo: ')
                print(self.usuarioDAO.buscar_amigo(nome_amigo))

            if opcao1 == 4:
                nova_profissao = input('Digite sua nova profissão: ')
                self.user.set_profissao(nova_profissao)
                self.usuarioDAO.set_profissao(nova_profissao, self.email)

            if opcao1 == 5:
                print(self.user.listar_dados())

            if opcao1 == 6:
                email_amigo = input('Digite o email do seu amigo: ')
                self.usuarioDAO.desfazer_amizade(self.email, email_amigo)

            if opcao1 == 7:
                print(self.usuarioDAO.listar_amigos())

            if opcao1 == 8:
                sua_senha = input('Digite sua senha: ')
                if sua_senha == senha:
                    n_senha = input('Digite a nova senha: ')
                    n_senha1 = input('Confirme a nova senha: ')
                    if n_senha != n_senha1:
                        print('As senhas não conferem')
                        n_senha = input('Digite a nova senha: ')
                        n_senha1 = input('Confirme a nova senha: ')
                    self.usuarioDAO.set_senha(self.email, n_senha)


            if opcao1 == 9:
                self.menu_inicial()

            print('FEED')
            print('1 - Publicar')
            print('2 - Adicionar amigo')
            print('3 - Buscar email de seu amigo')
            print('4 - Mudar profissão')
            print('5 - Listar minhas informações')
            print('6 - Desfazer amizade')
            print('7 - Listar amigos')
            print('8 - Alterar sua senha')
            print('9 - Sair')
            opcao1 = int(input('Digite a opção (feed): '))
        return opcao1

    def buscar_usuario(self, email):
        return self.usuarioDAO.buscar(email)

