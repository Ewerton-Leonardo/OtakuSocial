class Publicacao:
    def __init__(self, email_user, texto, local='', email_amigo=''):
        self.email_user=email_user
        self.texto=texto
        self.local=local
        self.comentarios=list()
        self.marcar_amigo=email_amigo
        self.publi=['Texto: ' + str(texto), 'Local: ' + str(local), 'Amigo: ' + str(email_amigo)]
        self.dados_publi=dict()
