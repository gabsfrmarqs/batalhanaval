import random
import time
from pygame import mixer

def Matriz(n):
    matriz_pontos = [""]*n
    i = 0
    while i < len(matriz_pontos):
        vet = ["."]*n
        matriz_pontos[i] = vet
        i+=1
    return matriz_pontos
        
def ImprimeMatriz(lista):
    n = len(lista)
    cont = 0
    x_num = [0]*n
    for i in range(n):
        x_num[i] = i
    linha_x = [' ']+x_num
    for k in range(len(linha_x)):
        print(linha_x[k],end=" ")
    print()
    for i in range(len(lista)):
        print(cont,end=' ')
        for j in range(len(lista[0])):
            print(lista[i][j],end=" ")
        print()
        cont+=1
        
def Barco(barco,M,linha,coluna,orientacao):
    tam = barco[0]
    letra = barco[1]
    if orientacao == False: #horizontal
        i = linha
        barco_adicionado = False
        while barco_adicionado== False:
            j = coluna
            cabe = True
            if (j+tam) < len(M):# barco cabe a matriz
                for g in range(j,j+tam):
                    if M[i][g] != ".": #Há outro barco na
                        cabe = False
            else:
                cabe =False
            if cabe == True:
                for g in range(j,j+tam):
                    M[i][g] = letra
                barco_adicionado = True
            else:
                return barco_adicionado
    elif orientacao == True: #O 
        i = linha
        barco_adicionado = False
        while barco_adicionado== False:
            j = coluna
            cabe = True
            if (j+tam) < len(M):# barco cabe a matriz
                for g in range(j,j+tam):
                    if M[g][i] != ".": #tem outro barco
                        cabe = False
            else:
                cabe = False
            if cabe == True:
                for g in range(j,j+tam):
                    M[g][i] = letra
                barco_adicionado = True
            else:
                return barco_adicionado
    return barco_adicionado

def GeraMatrizRival(M,barcos):
    for i in range(len(barcos)):
        while True:
            orientacao = random.randint(0,1)
            linha = random.randint(0,9)
            coluna = random.randint(0,9)
            verifica_adicionado = Barco(barcos[i],M,linha,coluna,orientacao)
            if verifica_adicionado == True:
                break

def atirar(M,linha,coluna,MJogo):
    i = linha
    j = coluna
    acertou = False
    embarcacao = 'Água'
    if M[i][j] == '.':
        MJogo[i][j] = '~'
        M[i][j] = '~'
    else:
        print(M[i][j])
        if M[i][j] == 'P':
            embarcacao = 'Porta-Aviões'
            letra = 'P'
        elif M[i][j] == 'E':
            embarcacao = 'Encouraçado'
            letra = 'E'
        elif M[i][j] == 'C':
            embarcacao = 'Cruzeiro'
            letra = 'C'
        elif M[i][j] == 'S':
            embarcacao = 'Submarino'
            letra = 'S'
        M[i][j] = letra
        MJogo[i][j] = letra
        acertou = True
    return M,acertou,embarcacao

def verificaJogada(M,linha,coluna):
    i = linha
    j = coluna
    if i >= 10 or j >= 10:
        return False
    elif M[i][j] == '~' or M[i][j] == 'X':
        return False
    else:
        return True

def musica():
    confirma = input("Deseja música de fundo? (S/N):")
    if confirma.lower() == "s":
        mixer.init()
        mixer.music.load("song.ogg")
        mixer.music.set_volume(0.7)
        mixer.music.play(-1)
    else:
        print("Belezinha, divirta-se!")
        
def main():
    musica()
    mixer.init()
    explosao = mixer.Sound('explosão.ogg')
    tada = mixer.Sound('tada.ogg')

    n = 10
    M = Matriz(n)
    M_bot = Matriz(n)
    
    print("Tabuleiro:")
    ImprimeMatriz(M)
    
    #Porta Aviões, Encouraçado, Cruzeiro e Submarino
    barcos= [[5,"P"],[4,"E"],[3,"C"],[2,"S"]]
    
    #A função abaixo gera o tabuleiro. O usuário não enxergará esse tabuleiro
    GeraMatrizRival(M_bot,barcos)
  
    chances = 20
    acertos = 0
    #14 é o número total de coordenadas ocupadas por embarcações.
    while chances != 0 and acertos < 14: 
        print("Insira sua jogada:" )
        print(f"Chances: {chances}")
        try:
            linha = int(input("Linha: "))
            coluna = int(input("Coluna: "))
        except:
            print("Número inválido. Jogue novamente.\n")
        
        permissao = verificaJogada(M,linha,coluna)
        if permissao ==  True:
            M_bot, acertou,embarcacao = atirar(M_bot,linha,coluna,M)
            if acertou == False:
                chances-=1
                #print(f'\nVocê não acertou nada. Shame on you.')
                ImprimeMatriz(M)
                print('Água!')
                print()
            else:
                explosao.play(0)
                print("\nTabuleiro:")
                ImprimeMatriz(M)
                print(f'Você acertou um {embarcacao}!\n')
                acertos+=1
        else:
            print("Número inválido. Jogue novamente.\n")
        
    if chances == 0:
        print("Você perdeu. Shame on you.")
        print("Tabuleiro do jogo: ")
        ImprimeMatriz(M_bot)

    else:
        time.sleep(2)
        print("Você ganhou!")
        tada.play(0)
        time.sleep(3)

    
    print("Obrigado por jogar este jogo de qualidade!")
    for i in range(5,0,-1):
        print(f"Saindo em {i-1} segundos")
        time.sleep(1)

        #caractere especial. Ele apaga a linha anterior no comando, atualizando o timer
        print("\033[A\033[A")

main()
