import pygame

LARGURA_TELA= 640
ALTURA_TELA = 480

class Menu():
    state = 0
    def __init__(self,itens,fonte_cor=(0,0,0),selecao_cor=(255,0,0),ttf_font=None,font_size=25):
        self.__fonte_cor = fonte_cor
        self.__selecao_cor = selecao_cor
        self.__itens = itens
        self.fonte = pygame.font.Font(ttf_font,font_size)

    #get e set
    def getFonteCor(self):
        return self.__fonte_cor
    def setFonteCor(self, fonteCor):
        self.__fonte_cor = fonteCor

    def getSelecaoCor(self):
        return self.__selecao_cor
    def setSelecaoCor(self, selecaoCor):
        self.__selecao_cor = selecaoCor

    def getItens(self):
        return self.__itens
    def setItens(self, itens):
        self.__itens = itens

    #Metodos
    def mostrar_frame(self,tela):
        for indice, item in enumerate(self.getItens()):
            if self.state == indice:
                label = self.fonte.render(item,True,self.getSelecaoCor())
            else:
                label = self.fonte.render(item,True,self.getFonteCor())
            
            largura = label.get_width()
            altura = label.get_height()
            
            pX = (LARGURA_TELA /2) - (largura /2)
            # altura do bloco de texto
            t_h = len(self.getItens()) * altura
            pY = (ALTURA_TELA /2) - (t_h /2) + (indice * altura)

            tela.blit(label,(pX,pY))
        
    def manipulador_evento(self,evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif evento.key == pygame.K_DOWN:
                if self.state < len(self.getItens()) -1:
                    self.state += 1