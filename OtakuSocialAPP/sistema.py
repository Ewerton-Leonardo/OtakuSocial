from datetime import *
from excecoes import *
import psycopg2

conn = psycopg2.connect(host="localhost", database="otakusocial", user="postgres", password="ewerton")

cur = conn.cursor()

from publicacaoDAO import publicacaoDAO
from usuario import Usuario
from usuarioDAO import usuarioDAO
from mensagem import Mensagem
from mensagemDAO import MensagemDAO


class Sistema:
    def __init__(self):
        conexao = psycopg2.connect(host="localhost", database="otakusocial", user="postgres", password="ewerton")
        self.usuarioDAO = usuarioDAO(conexao)
        self.publicacaoDAO = publicacaoDAO(conexao)
        self.mensagemDAO = MensagemDAO(conexao)

    def cadastrar_usuario(self, email, senha, nome,data_nascimento,profissao):
        hj = date.today()
        dia, mes, ano = data_nascimento.split('/')
        data_nasc = date(day=int(dia), month=int(mes), year=int(ano))
        idade = ((hj-data_nasc)/365).days
        if self.buscar_usuario(email):
            raise UsuarioExistente('Email do usuário já existe')
        if int(idade) < 12:
            raise IdadeMenorException('Idade menor que 12 anos')
        user = Usuario(nome,email,data_nascimento,profissao)
        self.usuarioDAO.inserir(user)
        cur.execute("INSERT INTO login(email, senha) VALUES (%s, %s)", (email, senha))
        conn.commit()
        return 'Usuário cadastrado com sucesso!'

    def fazer_login(self, email, senha):
        cursor = self.usuarioDAO.conexao.cursor()
        cursor.execute('SELECT * FROM login')
        cursor.execute('SELECT * FROM login')
        for tupla in cursor.fetchall():
            if str(tupla[0]) == str(email):
                if str(tupla[1]) == senha:
                    self.menu_feed(email, senha)
                else:
                    print('Senha incorreta')
            else:
                print('Email incorreto')

    def publicar(self, user, texto):
        publicacao = user.publicar(texto)
        self.publicacaoDAO.inserir(publicacao)
        cursor = self.usuarioDAO.conexao.cursor()
        cursor.execute('SELECT * FROM publicacao')
        for tupla in cursor.fetchall():
            if str(tupla[0]) == str(user.email) and str(tupla[1]) == texto:
                return (user.nome, 'publicou:', tupla[1])


    def menu_inicial(self):
        print('OtakuSocial')
        print('Menu Inicial')
        print('1 - Cadastrar usuário')
        print('2 - Fazer login')
        print('x - Sair')
        opcao = input('Digite a opção:').lower()

        while opcao != 'x':

            if opcao == '1':
                email = input('Digite seu id (Não é necessário ser numérico):')+'@otaku.com'.lower()
                print('Por padrão o término do seu ID é @otaku.com / Seu email: '+ email)
                senha = input('Digite sua senha:')
                senha1 = input('Digite sua senha novamente:')
                if senha != senha1:
                    print('As senhas não conferem')
                    senha = input('Digite sua senha: ')
                    senha1 = input('Digite sua senha novamente: ')

                nome = input('Digite seu nome: ')
                data_nascimento = input('Digite sua data de nascimento, formato(DD/MM/AAAA): ')
                profissao = input('Digite sua profissão (opcional): ')
                try:
                    self.cadastrar_usuario( email, senha, nome,data_nascimento,profissao)
                except UsuarioExistente as ue:
                    print('Não foi possível cadastrar usuário. Erro:', ue)
                except IdadeMenorException as im:
                    print('Não foi possível cadastrar usuário. Erro:', im)
                except ValueError:
                    print('Não foi possível cadastrar usuário. Erro: Data não confere')



            if opcao == '2':
                email = input('Digite seu e-mail: ').lower()
                senha = input('Digite sua senha: ')
                self.fazer_login(email, senha)

            print('OtakuSocial')
            print('Menu Inicial')
            print('1 - Cadastrar usuário')
            print('2 - Fazer login')
            print('x - Sair')
            opcao = input('Digite a opção: ').lower()


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
        print('9 - Excuir conta')
        print('10 - BATE-PAPO')
        print('x - Sair')

        opcao1 = input('Digite a opção (feed): ').lower()

        while opcao1 != 'x':


            if opcao1 == '1':
                texto=input('Texto: ')
                '''local=input('Local: ')
                amigo=input('Email Amigo: ')'''
                print(self.publicar(self.user, texto))

            if opcao1 == '2':
                email_amigo=input('Digite o email da pessoa que deseja adicionar: ').lower()
                self.usuarioDAO.inserir_amigo(self.email, email_amigo)

            if opcao1 == '3':
                nome_amigo = input('Digite o nome do seu amigo: ')
                print(self.usuarioDAO.buscar_amigo(nome_amigo))

            if opcao1 == '4':
                nova_profissao = input('Digite sua nova profissão: ')
                self.user.set_profissao(nova_profissao)
                self.usuarioDAO.set_profissao(nova_profissao, self.email)

            if opcao1 == '5':
                print(self.user.listar_dados())

            if opcao1 == '6':
                email_amigo = input('Digite o email do seu amigo: ').lower()
                self.usuarioDAO.desfazer_amizade(self.email, email_amigo)
                print('Você desfez amizade com '+self.buscar_usuario(email_amigo).nome)

            if opcao1 == '7':
                print(self.usuarioDAO.listar_amigos(self.user.email))

            if opcao1 == '8':
                sua_senha = input('Digite sua senha: ')
                if sua_senha == senha:
                    n_senha = input('Digite a nova senha: ')
                    n_senha1 = input('Confirme a nova senha: ')
                    if n_senha != n_senha1:
                        print('As senhas não conferem')
                        n_senha = input('Digite a nova senha: ')
                        n_senha1 = input('Confirme a nova senha: ')
                    self.usuarioDAO.set_senha(self.email, n_senha)
                    print('Senha alterada com sucesso!')

            if opcao1 == '9':
                senha=input('Por questão de segurança digite sua senha: ')
                cursor = self.usuarioDAO.conexao.cursor()
                cursor.execute('SELECT * FROM login')
                for tupla in cursor.fetchall():
                    if str(tupla[0]) == str(email):
                        if str(tupla[1]) == senha:
                            self.usuarioDAO.excuir_conta(email)
                            print('Usuário excluído')
                            self.menu_inicial()
                        else:
                            print('Senha incorreta')

            if opcao1 == '10':
                print('BATE-PAPO')
                print('1 - Iniciar conversa')
                print('2 - Entrar em conversa')
                print('3 - Buscar mensagem')
                print('4 - Apagar conversa')
                print('5 - Apagar todas conversas')
                print('x - Sair')
                opcao2 = input('Digite sua opção: ').lower()
                while opcao2 != 'x':
                    if opcao2 == '1':
                        email_d=input('Digite o email da pessoa: ')
                        texto = input('Digite a mensagem: ')
                        mensagem = Mensagem(texto, self.email, email_d)
                        self.mensagemDAO.enviar(mensagem)

                    if opcao2 == '2':
                        print('CONVERSAS')
                        for nome in self.mensagemDAO.nomes_conversas(self.email):
                            print(str(nome[0]))
                        nome=input('Digite o nome da pessoa (Para sair digite x): ')
                        if nome == 'x':
                            self.menu_feed(self.user.email, senha)

                        pessoa = self.usuarioDAO.buscar_pelo_nome(nome)
                        if pessoa == False:
                            print('Nome incorreto')
                            opcao2='2'
                            return opcao2

                        conversa = self.mensagemDAO.conversa(self.email, pessoa.email)
                        for tupla in conversa:
                            if str(tupla[0][0]) == str(self.user.email):
                                a='Você'
                                b=pessoa.nome
                                print(a + ':' + str(tupla[0][1]))
                            if str(tupla[0][0]) == str(pessoa.email):
                                a=str(pessoa.nome)
                                b='Você'
                                print(a + ': ' + str(tupla[0][1]))
                        conversar=input('Você deseja continuar conversa? sim ou nao: ').lower()
                        while conversar=='sim':
                            texto = input('Digite a mensagem: ')
                            mensagem = Mensagem(texto, self.email, pessoa.email)
                            self.mensagemDAO.enviar(mensagem)
                            conversar=input('Você deseja continuar conversa? sim ou nao: ')


                    if opcao2 == '3':
                        pass

                    if opcao2 == '4':
                        pass

                    if opcao2 == '5':
                        pass

                return opcao2



            if opcao1 == 'x':
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
            print('9 - Excuir conta')
            print('x - Sair')
            opcao1 = input('Digite a opção (feed): ').lower()
        return opcao1

    def buscar_usuario(self, email):
        return self.usuarioDAO.buscar(email)


