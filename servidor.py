import socket
from _thread import *
import pickle
from jogo import Jogo

#Trabalho referente a disciplina de redes - Ciência da Computação - Mackenzie.

TCP_IP = "YOUR IPV4 ADRESS"
TCP_PORTA = 3214
TAMANHO_BUFFER = 4096

# Criação de socket TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((TCP_IP, TCP_PORTA))

#Define limite de conexões simultâneas
servidor.listen(2)
print("Servidor disponivel")

def thread_cliente(conn, jogador, IdJogo):
    global IDs
    conn.send(str.encode(str(jogador)))
    while True:
        try:
            msg = conn.recv(TAMANHO_BUFFER).decode()
            if IdJogo in Jogos:
                Jogo = Jogos[IdJogo]
                if msg:
                    if msg == "0":
                        Jogo.resetarJogo()
                    elif msg != "1":
                        Jogo.Jogada(jogador, msg)
                    conn.sendall(pickle.dumps(Jogo))
                else:
                    break
            else:
                break
        except:
            break

    try:
        del Jogos[IdJogo]
    except:
        pass

    IDs -= 1
    conn.close() 

Jogos = {}
IDs = 0

while True:
    conn, addr = servidor.accept()
    print("Cliente ", addr, "conectado")

    key = 0
    IDs += 1
    IDJogo = (IDs - 1) // 2

    if IDs % 2 == 1: #Cria um novo jogo e deixa o jogador na tela de espera
        Jogos[IDJogo] = Jogo(IDJogo)
        print("Criando novo jogo...")
        
    else: #Segundo jogador entra e inicia o jogo
        Jogos[IDJogo].pronto = 1
        key = 1

    start_new_thread(thread_cliente, (conn, key, IDJogo))
