import pygame, random
from menu import Menu

LARGURA_TELA = 640
ALTURA_TELA = 480

BRANCO = (255,255,255)
PRETO = (0,0,0)

class Game():
    def __init__(self):
        self.font = pygame.font.Font("kenvector_future_thin.ttf",50)
        self.menu = Menu(("começar","sobre","sair"),fonte_cor=BRANCO,font_size=50,ttf_font="kenvector_future.ttf")
        self.mostrar_quadro = False
        self.mostrar_menu = True
        self.__bola = Bola(LARGURA_TELA / 2,ALTURA_TELA / 2)
        self.__jogador = Jogador(50,ALTURA_TELA / 2)
        self.__inimigo = Inimigo(LARGURA_TELA - 65,ALTURA_TELA / 2)
        self.__pontuacao_jogador = 0
        self.__pontuacao_inimigo = 0

    #get e set
    def getBola(self):
        return self.__bola
    def setBola(self, bola):
        self.__bola = bola

    def getJogador(self):
        return self.__jogador
    def setJogador(self, jogador):
        self.__jogador = jogador

    def getInimigo(self):
        return self.__inimigo
    def setInimigo(self, inimigo):
        self.__inimigo = inimigo

    def getPontuacaoJogador(self):
        return self.__pontuacao_jogador
    def setPontuacaoJogador(self, pontuacaoJogador):
        self.__pontuacao_jogador = pontuacaoJogador

    def getPontucaoInimigo(self):
        return self.__pontuacao_inimigo
    def setPontuacaoInimigo(self, pontuacaoInimigo):
        self.__pontuacao_inimigo = pontuacaoInimigo

    #Metodos
    def eventos_game(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return True
            self.menu.manipulador_evento(evento)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if self.mostrar_menu and not self.mostrar_quadro:
                        if self.menu.state == 0:
                            self.mostrar_menu = False
                            self.game_init()
                        elif self.menu.state == 1:
                            self.mostrar_quadro = True
                        elif self.menu.state == 2:
                            return True
                elif evento.key == pygame.K_ESCAPE:
                    self.mostrar_menu = True
                    self.mostrar_quadro = False

                elif evento.key == pygame.K_UP:
                    self.getJogador().go_up()
                elif evento.key == pygame.K_DOWN:
                    self.getJogador().go_down()

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    self.getJogador().stop()
            
        return False

    def logica(self):
        if not self.mostrar_menu:
            self.getBola().update()
            self.getJogador().update(self.getBola())
            self.getInimigo().update(self.getBola())
            if self.getBola().rect.x < 0:
                self.getBola().reset()
                self.getJogador().rect.centery = ALTURA_TELA / 2
                self.setPontuacaoInimigo(self.getPontucaoInimigo() + 1)
            elif self.getBola().rect.x > LARGURA_TELA:
                self.getBola().reset()
                self.getJogador().rect.centery = ALTURA_TELA / 2
                self.setPontuacaoJogador(self.getPontuacaoJogador() + 1)

    def game_init(self):
        # Coloca a bola no centro da tela
        self.getBola().rect.centerx = LARGURA_TELA / 2
        self.getBola().rect.centery = ALTURA_TELA / 2
        self.getBola().mudar_x = -5
        self.getBola().mudar_y = 0
        # Define o jogador e o inimigo na posicao inicial
        self.getJogador().rect.centery = ALTURA_TELA / 2
        self.getInimigo().rect.centery = ALTURA_TELA / 2
        self.setPontuacaoJogador(0)
        self.setPontuacaoInimigo(0)

    def exibir_palavras_tela(self,tela):
        tela.fill(PRETO)
        tempo_esperado = False
        if self.mostrar_menu:
            if self.mostrar_quadro:
                self.exibir_mensagem(tela,"Beta Pong 2018")
            else:
                self.menu.mostrar_frame(tela)

        elif self.getPontuacaoJogador() == 1:
            self.exibir_mensagem(tela,"Você ganhou!",BRANCO)
            tempo_esperado = True
            self.setPontuacaoJogador(0)
            self.setPontuacaoInimigo(0)
            self.mostrar_menu = True

        elif self.getPontucaoInimigo() == 1:
            self.exibir_mensagem(tela,"Game Over",BRANCO)
            tempo_esperado = True
            self.setPontuacaoJogador(0)
            self.setPontuacaoInimigo(0)
            self.mostrar_menu = True
        else:
            self.getBola().desenhar(tela)
            self.getJogador().draw(tela)
            self.getInimigo().draw(tela)
            #Linha central do jogo
            for y in range(0,ALTURA_TELA,20):
                pygame.draw.rect(tela,BRANCO, [LARGURA_TELA / 2, y, 10, 10])
            #Placar
            label_pontuacao_jogador = self.font.render(str(self.getPontuacaoJogador()),True,BRANCO)
            tela.blit(label_pontuacao_jogador,(270,10))
            label_pontuacao_inimigo = self.font.render(str(self.getPontucaoInimigo()),True,BRANCO)
            tela.blit(label_pontuacao_inimigo,(350,10))
        pygame.display.flip()
        if tempo_esperado:
            pygame.time.wait(3000)

    def exibir_mensagem(self,tela,mensagem,cor=(255,0,0)):
        label = self.font.render(mensagem,True,cor)
        # Largura e altura
        largura = label.get_width()
        altura = label.get_height()
        # Determinar a pocicao
        pX = (LARGURA_TELA /2) - (largura /2)
        pY = (ALTURA_TELA /2) - (altura /2)
        tela.blit(label,(pX,pY))

class Bola():
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,10,10)
        self.mudar_x = 0
        self.mudar_y = 0

    def update(self):
        if self.rect.top < 0:
            self.mudar_y *= -1
            self.rect.top = 0
        elif self.rect.bottom > ALTURA_TELA:
            self.mudar_y *= -1
            self.rect.bottom = ALTURA_TELA
        self.rect.x += self.mudar_x
        self.rect.y += self.mudar_y

    def reset(self):
        self.rect.x = LARGURA_TELA / 2
        self.rect.y = ALTURA_TELA / 2
        self.mudar_x = -5
        self.mudar_y = random.randint(-3,3)

    def desenhar(self,tela):
        pygame.draw.rect(tela,BRANCO,self.rect)

class Jogador():
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,50)
        self.__mudar = 0

    #set e get
    def getMudar(self):
        return self.__mudar
    def setMudar(self, mudar):
        self.__mudar = mudar

    #Metodos
    def update(self,bola):
        if self.rect.top <= 0 and self.getMudar() < 0:
            self.setMudar(0)
        elif self.rect.bottom >= ALTURA_TELA and self.getMudar() > 0:
            self.setMudar(0)
        if self.rect.colliderect(bola.rect):
            bola.mudar_y = random.randint(-5,5)
            bola.mudar_x *= -1
            bola.rect.left = self.rect.right
        self.rect.y += self.getMudar()

    def go_up(self):
        self.setMudar(-5)

    def go_down(self):
        self.setMudar(5)

    def stop(self):
        self.setMudar(0)

    def draw(self,tela):
        pygame.draw.rect(tela,BRANCO,self.rect)

class Inimigo():
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,50)

    def update(self,bola):
        if self.rect.centery > bola.rect.centery:
            i = self.rect.centery - bola.rect.centery
            if i <= 4:
                self.rect.centery = bola.rect.centery
            else:
                self.rect.y -= 4
        elif self.rect.centery < bola.rect.centery:
            i = bola.rect.centery - self.rect.centery
            if i <= 4:
                self.rect.centery = bola.rect.centery
            else:
                self.rect.y += 4
        if self.rect.colliderect(bola.rect):
            bola.mudar_x *= -1
            bola.rect.right = self.rect.left

    def draw(self,tela):
        pygame.draw.rect(tela,BRANCO,self.rect)