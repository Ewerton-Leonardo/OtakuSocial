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
from sistemaDAO import SistemaDAO


class Sistema:
    def __init__(self):
        conexao = psycopg2.connect(host="localhost", database="otakusocial", user="postgres", password="ewerton")
        self.usuarioDAO = usuarioDAO(conexao)
        self.publicacaoDAO = publicacaoDAO(conexao)
        self.mensagemDAO = MensagemDAO(conexao)
        self.sistemaDAO = SistemaDAO(conexao)

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
        self.sistemaDAO.inserir_login(email,senha)
        return 'Usuário cadastrado com sucesso!'

    def fazer_login(self, email, senha):
        if self.sistemaDAO.fazer_login(email, senha) == True:
            self.menu_feed(email, senha)
        else:
            raise SenhaIncorretaException('Senha incorreta')


    def publicar(self, user, texto):
        publicacao = user.publicar(texto)
        self.publicacaoDAO.inserir(publicacao)
        publi = self.publicacaoDAO.publicar(publicacao)
        return user.nome + ' publicou ' + publi.texto

    def buscar_amigo(self, nome_amigo):
        return self.usuarioDAO.buscar_amigo(nome_amigo)

    def conversa(self, pessoa, user):
        conversa = self.mensagemDAO.conversa(user.email, pessoa.email)
        for tupla in conversa:
            if str(tupla[0][0]) == str(user.email):
                a='Você'
                b=pessoa.nome
                print(a + ':' + str(tupla[0][1]))
            if str(tupla[0][0]) == str(pessoa.email):
                a=str(pessoa.nome)
                b='Você'
                print(a + ': ' + str(tupla[0][1]))


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
                    print(self.cadastrar_usuario( email, senha, nome,data_nascimento,profissao))
                except UsuarioExistente as ue:
                    print('Não foi possível cadastrar usuário. Erro:', ue)
                except IdadeMenorException as im:
                    print('Não foi possível cadastrar usuário. Erro:', im)
                except ValueError:
                    print('Não foi possível cadastrar usuário. Erro: Data não confere')



            if opcao == '2':
                email = input('Digite seu e-mail: ').lower()
                senha = input('Digite sua senha: ')
                try:
                    self.fazer_login(email, senha)
                except SenhaIncorretaException as si:
                    print('Não foi possível fazer login. Erro:', si)

            print('OtakuSocial')
            print('Menu Inicial')
            print('1 - Cadastrar usuário')
            print('2 - Fazer login')
            print('x - Sair')
            opcao = input('Digite a opção: ').lower()


        return opcao

    def menu_feed(self, email, senha):
        self.email=email
        self.senha = senha
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
                print('Agora '+str(self.buscar_usuario(email_amigo).nome)+' é seu amigo')

            if opcao1 == '3':
                nome_amigo = input('Digite o nome do seu amigo: ')
                print(self.buscar_amigo(nome_amigo))

            if opcao1 == '4':
                nova_profissao = input('Digite sua nova profissão: ')
                self.user.set_profissao(nova_profissao)
                self.usuarioDAO.set_profissao(nova_profissao, self.email)
                print('Agora sua nova profissao é ' + nova_profissao)

            if opcao1 == '5':
                print(self.usuarioDAO.listar_dados(self.email))

            if opcao1 == '6':
                email_amigo = input('Digite o email do seu amigo: ').lower()
                self.usuarioDAO.desfazer_amizade(self.email, email_amigo)
                print('Você desfez amizade com '+self.buscar_usuario(email_amigo).nome)

            if opcao1 == '7':
                for amigo in self.usuarioDAO.listar_amigos(self.user.email):
                    print(amigo)

            if opcao1 == '8':
                sua_senha = input('Digite sua senha: ')
                if sua_senha == self.senha:
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
                        if str(tupla[1]) == self.senha:
                            self.usuarioDAO.excuir_conta(email)
                            print('Usuário excluído')
                            self.menu_inicial()
                        else:
                            print('Senha incorreta')

            if opcao1 == '10':
                print('BATE-PAPO')
                print('1 - Iniciar conversa')
                print('2 - Entrar em conversa')
                '''print('3 - Buscar mensagem')
                print('4 - Apagar conversa')
                print('5 - Apagar todas conversas')'''
                print('x - Voltar')
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
                            self.menu_feed(self.email, self.senha)

                        pessoa = self.usuarioDAO.buscar_pelo_nome(nome)
                        if pessoa == False:
                            print('Nome incorreto')
                            opcao2='2'
                            return opcao2

                        self.conversa(pessoa, self.user)
                        conversar=input('Você deseja continuar conversa? sim ou nao: ').lower()
                        while conversar=='sim':
                            texto = input('Digite a mensagem: ')
                            mensagem = Mensagem(texto, self.email, pessoa.email)
                            self.mensagemDAO.enviar(mensagem)
                            self.conversa(pessoa, self.user)
                            conversar=input('Você deseja continuar conversa? sim ou nao: ')


                    if opcao2 == '3':
                        pass

                    if opcao2 == '4':
                        pass

                    if opcao2 == '5':
                        pass

                    print('BATE-PAPO')
                    print('1 - Iniciar conversa')
                    print('2 - Entrar em conversa')
                    '''print('3 - Buscar mensagem')
                    print('4 - Apagar conversa')
                    print('5 - Apagar todas conversas')'''
                    print('x - Voltar')
                    opcao2 = input('Digite sua opção: ').lower()
                return self.menu_feed(self.email, self.senha)



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
            print('10 - BATE-PAPO')
            print('x - Sair')
            opcao1 = input('Digite a opção (feed): ').lower()
        return opcao1

    def buscar_usuario(self, email):
        return self.usuarioDAO.buscar(email)


