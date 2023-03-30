#Trabalho referente a disciplina de redes - Ciência da Computação - Mackenzie.

class Jogo:
    def __init__(self, id):
        #Número do Jogo
        self.id = id

        #Boolean para afirmar de jogadores já selecionaram o movimento
        self.MovP1 = 0
        self.MovP2 = 0

        #Define se o jogo pode ser iniciado
        self.pronto = 0

        #Guardar as jogadas
        self.jogadas = [None, None]

    def Conectado(self):
        return self.pronto

    def Jogada(self, player, jogada):
        self.jogadas[player] = jogada
        if player == 0:
            self.MovP1 = 1
        else:
            self.MovP2 = 1

    def SalvarJogada(self, p):  # Guarda a jogada no vetor jogadas
        return self.jogadas[p]

    def DoisJogaram(self):
        return (self.MovP1 == 1) and (self.MovP2 == 1)

    def vencedor(self):
        j1 = self.jogadas[0]
        j2 = self.jogadas[1]

        if (j1 == "Pedra" and j2 == "Tesoura") or (j1 == "Papel" and j2 == "Pedra") or (j1 == "Tesoura" and j2 == "Papel"):
            vencedor = 0
            
        elif (j1 == "Tesoura" and j2 == "Pedra") or (j1 == "Papel" and j2 == "Tesoura") or (j1 == "Pedra" and j2 == "Papel"):
            vencedor = 1

        else:
            vencedor = 2

        return vencedor
        
    def resetarJogo(self):
        self.MovP1 = 0
        self.MovP2 = 0