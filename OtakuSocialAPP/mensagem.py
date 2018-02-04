from datetime import *
class Mensagem:
    def __init__(self, texto, email_o, email_d):
        self.texto=texto
        self.email_o=email_o
        self.email_d=email_d
        self.data=datetime.today()
