import pickle
import socket
from jogo import Jogo
import pygame
import webbrowser

#Referencias: para botoes utilizando PNG: https://github.com/russs123/pygame_tutorials/tree/main/Button
#Trabalho referente a disciplina de redes - Ciência da Computação - Mackenzie.

class TCP_IP:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCP_IP = "192.168.1.17"
        self.PORTA = 3214
        self.bind = (self.TCP_IP, self.PORTA)
        self.conectar = self.connect()

    def getJogador(self):
        return self.conectar

    def connect(self):
        try:
            self.cliente.connect(self.bind)
            return self.cliente.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.cliente.send(str.encode(data))
            return pickle.loads(self.cliente.recv(4096))
        except socket.error:
            pass

pygame.font.init()
pygame.mixer.init()
width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cliente")

musicaMenu = pygame.mixer.music.load('./audios/musica_menu.mp3')
selectJogar = pygame.mixer.Sound('./audios/select_jogar.mp3')
selectSair = pygame.mixer.Sound('./audios/select_sair.mp3')
selectJogada = pygame.mixer.Sound('./audios/select_jogada.mp3')
somPerdeu = pygame.mixer.Sound('./audios/perdeu.mp3')
somGanhou = pygame.mixer.Sound('./audios/ganhou.mp3')

from img import *

class ButtonPNG():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()


		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#desenha botao
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
        
def format_texto(texto):
    font = pygame.font.SysFont("montserrat", 50, bold=True, italic=False)
    text = font.render(texto, True, (255, 255, 255))
    return text

def JanelaJogada(win, jogo, jogador, placar1, placar2):
    font = pygame.font.SysFont("montserrat", 50, bold=True, italic=False)
    
    if not(jogo.Conectado()): #Esperando jogador
        win.blit(ImgEsperando,pygame.rect.Rect(0,0, 800, 800))

    else:
        win.blit(ImgBG_game,pygame.rect.Rect(0,0, 800, 800))
        win.blit(ImgPedra,pygame.rect.Rect(135, 460, 214, 206))
        win.blit(ImgTesoura,pygame.rect.Rect(318, 460, 194, 194))
        win.blit(ImgPapel,pygame.rect.Rect(490, 469, 174, 175))
        win.blit(pygame.transform.scale(ImgSair,(141,44)),pygame.rect.Rect(620, 700, 80, 60))
        move1 = jogo.SalvarJogada(0)
        move2 = jogo.SalvarJogada(1)

        if jogador == 0:
            win.blit(format_texto(f"{placar1} x {placar2}"), (50, 70))
        else:
            win.blit(format_texto(f"{placar2} x {placar1}"), (50, 70))

        if jogo.DoisJogaram():
            pass

        else:
            if(jogo.MovP1 == 1) and (jogador == 0):
                if(move1 == "Pedra"):
                    win.blit(ImgPedra_escolhido, pygame.rect.Rect(135, 460, 214, 206))
                elif(move1 == "Tesoura"):
                    win.blit(ImgTesoura_Escolhido,pygame.rect.Rect(318, 460, 194, 194))
                elif(move1 == "Papel"):
                    win.blit(ImgPapel_escolhido,pygame.rect.Rect(490, 469, 174, 175))
            elif(jogo.MovP2 == 1) and (jogador == 1):
                if(move2 == "Pedra"):
                    win.blit(ImgPedra_escolhido, pygame.rect.Rect(135, 460, 214, 206))
                elif(move2 == "Tesoura"):
                    win.blit(ImgTesoura_Escolhido,pygame.rect.Rect(318, 460, 194, 194))
                elif(move2 == "Papel"):
                    win.blit(ImgPapel_escolhido,pygame.rect.Rect(490, 469, 174, 175))

            if (jogo.MovP1 == 0) and (jogo.MovP2 == 0):
                win.blit(ImgNao,pygame.rect.Rect(373,250,83,121))

            elif (jogo.MovP1 == 1) and (jogo.MovP2 == 0) and (jogador == 0):
                win.blit(ImgNao,pygame.rect.Rect(373,250,83,121))

            elif (jogo.MovP2 == 1) and (jogo.MovP1 == 0) and (jogador == 1):
                win.blit(ImgNao,pygame.rect.Rect(373,250,83,121))

            else:
                win.blit(ImgEscolhido,pygame.rect.Rect(362,179,136,178))

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    network = TCP_IP()
    player = int(network.getJogador()) 
    pedra_button = ButtonPNG(135, 460,ImgPedra, 1.0) 
    tesoura_button = ButtonPNG(318, 460,ImgTesoura, 1.0)
    papel_button = ButtonPNG(490, 469,ImgPapel, 1.0)
    quitmain_button = ButtonPNG(620,700,ImgSair, 0.3)
    placar1 = 0
    placar2 = 0
    
    while run:
        clock.tick(60)
        try:
            Jogo = network.send("1")
        except:
            run = False
            break

        if Jogo.DoisJogaram():
            JanelaJogada(win, Jogo, player, placar1, placar2) #desenha a tela
            pygame.time.delay(1000)
            try:
                Jogo = network.send("0")
            except:
                print("e\n")
                run = False
                break

            font = pygame.font.SysFont("montserrat", 50, bold=True, italic=False)
            if (Jogo.vencedor() == player):
                text = font.render("Você ganhou!", True, (255, 255, 255))
                somGanhou.play()
                win.blit(ImgGanhou, pygame.rect.Rect(width/2 - ImgGanhou.get_width()/2, 220, 342, 68))
                if player == 0:
                    placar1 += 1     
                else:                  
                    placar2 += 1
    
            elif Jogo.vencedor() == 2:
                text = font.render("Empate!", True, (255, 255, 255))
                win.blit(ImgEmpate, pygame.rect.Rect(width/2 - ImgEmpate.get_width()/2, 200, 140, 168))
                
            else:
                if player == 0:
                    placar2 += 1     
                else:
                    placar1 += 1

                somPerdeu.play()
                win.blit(ImgPerdeu, pygame.rect.Rect(width/2 - ImgPerdeu.get_width()/2, 140, 140, 168))
                text = font.render("Você perdeu...", True, (255, 255, 255))

            win.blit(text, ((width/2 - text.get_width()/2, 350)))
            pygame.display.update()
            pygame.time.delay(3000)

        if quitmain_button.draw(win) and Jogo.Conectado():
                selectSair.play()
                pygame.time.delay(1000)
                run = False
                pygame.quit()

        for event in pygame.event.get():                   
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if pedra_button.draw(win) and Jogo.Conectado():
                if player == 0:
                    if not Jogo.MovP1: 
                        selectJogada.play()
                        network.send("Pedra")
                else:
                    if not Jogo.MovP2:
                        selectJogada.play()
                        network.send("Pedra")

            elif tesoura_button.draw(win) and Jogo.Conectado():
                if player == 0:
                    if not Jogo.MovP1: 
                        selectJogada.play()
                        network.send("Tesoura")
                else:
                    if not Jogo.MovP2:
                        selectJogada.play()
                        network.send("Tesoura")
        
            elif papel_button.draw(win) and Jogo.Conectado():
                if player == 0:
                    if not Jogo.MovP1: 
                        selectJogada.play()
                        network.send("Papel")
                else:
                    if not Jogo.MovP2:
                        selectJogada.play()
                        network.send("Papel")
            
        JanelaJogada(win, Jogo, player, placar1, placar2)

start_button = ButtonPNG(173,243,ImgJogar, 1.0) 
quit_button = ButtonPNG(173,420,ImgSair, 1.0) 
creditos_button = ButtonPNG(645, 644, ImgCreditos, 1.0)
url = "https://github.com/R0chaa/Jokenp-"

def menu_inicial():
    run = True
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(60)
        win.fill((202, 228, 241))
        win.blit(ImgBG_home,pygame.rect.Rect(0, 0, 800, 800))

        if start_button.draw(win):
                selectJogar.play()
                main()

        if quit_button.draw(win):
                selectSair.play()
                pygame.time.delay(1000)
                run = False

        if creditos_button.draw(win):
                selectJogar.play()
                webbrowser.open_new(url)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        
    if run == False:
        pygame.mixer.music.stop()
        pygame.quit()
        return False
    
menu = True
while menu:
    
    menu = menu_inicial()
    if menu == False:
        print("Encerrando")
