import webbrowser
class URL:
    def __init__(self,url,nome):
        self.url=url
        self.nome=nome

    def abrir(self):
        webbrowser.open(self.url, new=0, autoraise=True)
